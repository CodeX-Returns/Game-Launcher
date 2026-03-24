import http.server
import socketserver
import os
import sys
import time
import pyperclip
import logging
from colorama import Fore, Back, Style, init
from functools import lru_cache
import threading
from github import Github
import base64

init(autoreset=True)
logging.disable(logging.CRITICAL)

GITHUB_USERNAME = "CodeX-Returns"
PASSWORD = "CodeX"
GITHUB_TOKEN = "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"  # PASTE YOUR TOKEN HERE

GAMES = {
    "1": {"name": "3kh0", "repo": "3kh0", "port": 8001, "index_path": "index.html", "branch": "main"},
    "2": {"name": "Arsenic", "repo": "Arsenic", "port": 8003, "index_path": "index.html", "branch": "main"},
    "3": {"name": "Eaglercraft", "repo": "Eaglercraft", "port": 8004, "index_path": "index.html", "branch": "main"},
    "4": {"name": "GameBoy", "repo": "GameBoy", "port": 8005, "index_path": "index.html", "branch": "master"},
    "5": {"name": "GN-Math", "repo": "GN-Math", "port": 8006, "index_path": "index.html", "branch": "main"},
    "6": {"name": "JeoWeb", "repo": "JeoWeb", "port": 8007, "index_path": "index.html", "branch": "main"},
    "7": {"name": "MonkeyGG", "repo": "MonkeyGG", "port": 8008, "index_path": "index.html", "branch": "main"},
    "8": {"name": "Selenite", "repo": "Selenite", "port": 8009, "index_path": "index.html", "branch": "main"},
}

FAST_CACHE = {}
CACHE_SIZE = 0
MAX_CACHE = 300 * 1024 * 1024  # 300MB cache

# Initialize GitHub connection once
try:
    if GITHUB_TOKEN and GITHUB_TOKEN != "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":
        gh = Github(GITHUB_TOKEN)
    else:
        gh = Github()
except Exception as e:
    gh = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_progress_bar(duration=2):
    width = 40
    for i in range(width + 1):
        percent = (i / width) * 100
        bar = "█" * i + "░" * (width - i)
        sys.stdout.write(f"\r  {Fore.RED}[{bar}] {Fore.LIGHTRED_EX}{percent:.0f}%{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(duration / width)
    print()

def copy_to_clipboard(text):
    try:
        pyperclip.copy(text)
        return True
    except:
        return False

@lru_cache(maxsize=512)
def get_mime_type(filename):
    """Get MIME type"""
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.mjs': 'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml; charset=utf-8',
        '.ico': 'image/x-icon',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.m4a': 'audio/mp4',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.wasm': 'application/wasm',
        '.gz': 'application/gzip',
        '.ttf': 'font/ttf',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.eot': 'application/vnd.ms-fontobject',
        '.txt': 'text/plain; charset=utf-8',
        '.xml': 'application/xml; charset=utf-8',
        '.map': 'application/json',
        '.zip': 'application/zip',
        '.pdf': 'application/pdf',
        '.swf': 'application/x-shockwave-flash',
    }
    return mime_types.get(ext, 'application/octet-stream')

def add_to_cache(key, content):
    """Add to fast cache with LRU eviction"""
    global CACHE_SIZE
    content_size = len(content)
    
    while CACHE_SIZE + content_size > MAX_CACHE and FAST_CACHE:
        oldest_key = next(iter(FAST_CACHE))
        CACHE_SIZE -= len(FAST_CACHE[oldest_key])
        del FAST_CACHE[oldest_key]
    
    FAST_CACHE[key] = content
    CACHE_SIZE += content_size

def get_from_cache(key):
    """Get from cache"""
    return FAST_CACHE.get(key)

def fetch_github_file_pygithub(repo_name, path, branch="main"):
    """Fetch file using PyGithub - MUCH FASTER"""
    cache_key = f"{repo_name}:{path}"
    cached = get_from_cache(cache_key)
    if cached:
        return cached
    
    try:
        if gh is None:
            return None
        
        # Get repository
        repo = gh.get_user(GITHUB_USERNAME).get_repo(repo_name)
        
        # Clean path
        if not path or path == '/':
            path = 'index.html'
        path = path.lstrip('/')
        
        try:
            # Get file content
            file_content = repo.get_contents(path, ref=branch)
            
            # Decode if base64
            if file_content.encoding == 'base64':
                content = base64.b64decode(file_content.content)
            else:
                content = file_content.content.encode('utf-8')
            
            # Cache it
            if len(content) < 100 * 1024 * 1024:  # Cache if < 100MB
                add_to_cache(cache_key, content)
            
            return content
        except Exception as e:
            return None
    except Exception as e:
        return None

class FastGitHubHandler(http.server.SimpleHTTPRequestHandler):
    repo_name = None
    index_path = None
    branch = "main"
    
    def do_GET(self):
        try:
            # Parse the request path
            file_path = self.path.split('?')[0].split('#')[0]
            
            # Handle root
            if file_path == '/' or file_path == '':
                request_file = self.index_path
            else:
                request_file = file_path.lstrip('/')
            
            # Try to fetch the file using PyGithub
            content = fetch_github_file_pygithub(self.repo_name, request_file, self.branch)
            
            if content is not None:
                content_type = get_mime_type(request_file)
                
                try:
                    self.send_response(200)
                    self.send_header("Content-type", content_type)
                    self.send_header("Content-Length", str(len(content)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Cache-Control", "public, max-age=31536000")
                    self.send_header("Connection", "keep-alive")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.end_headers()
                    self.wfile.write(content)
                except Exception as e:
                    pass
            else:
                try:
                    self.send_error(404)
                except:
                    pass
        except Exception as e:
            try:
                self.send_error(500)
            except:
                pass

    def log_message(self, format, *args):
        pass

def start_server(repo_name, index_path, port, branch="main"):
    """Start the HTTP server"""
    FastGitHubHandler.repo_name = repo_name
    FastGitHubHandler.index_path = index_path
    FastGitHubHandler.branch = branch
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", port), FastGitHubHandler)
        httpd.timeout = 5
        
        while True:
            try:
                httpd.handle_request()
            except KeyboardInterrupt:
                break
            except Exception as e:
                continue
    except Exception as e:
        pass

def show_login_screen():
    clear()
    print("\n")
    print(f"{Fore.RED}===============================================================")
    print(f"                                                               ")
    print(f"        {Fore.LIGHTRED_EX}CODEX-RETURNS LOGIN SYSTEM{Fore.RED}                        ")
    print(f"                                                               ")
    print(f"        {Fore.WHITE}Secure Access Required{Fore.RED}                              ")
    print(f"                                                               ")
    print(f"==============================================================={Style.RESET_ALL}\n")
    
    attempts = 3
    while attempts > 0:
        print(f"  {Fore.LIGHTRED_EX}Enter Password ({attempts} attempts left):")
        password_input = input(f"  {Fore.RED}>> {Style.RESET_ALL}")
        
        if password_input == PASSWORD:
            clear()
            print("\n")
            print(f"{Fore.GREEN}===============================================================")
            print(f"                                                               ")
            print(f"            {Fore.LIGHTGREEN_EX}ACCESS GRANTED{Fore.GREEN}                              ")
            print(f"                                                               ")
            print(f"        {Fore.WHITE}Welcome to CodeX-Returns{Fore.GREEN}                           ")
            print(f"                                                               ")
            print(f"==============================================================={Style.RESET_ALL}\n")
            time.sleep(1.5)
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"  {Fore.RED}X Incorrect Password. Try again.{Style.RESET_ALL}\n")
                time.sleep(1)
                clear()
                print("\n")
                print(f"{Fore.RED}===============================================================")
                print(f"                                                               ")
                print(f"        {Fore.LIGHTRED_EX}CODEX-RETURNS LOGIN SYSTEM{Fore.RED}                        ")
                print(f"                                                               ")
                print(f"        {Fore.WHITE}Secure Access Required{Fore.RED}                              ")
                print(f"                                                               ")
                print(f"==============================================================={Style.RESET_ALL}\n")
            else:
                print(f"\n  {Fore.RED}X ACCESS DENIED - Maximum attempts exceeded.{Style.RESET_ALL}\n")
                time.sleep(2)
                sys.exit()
    return False

def show_splash_screen():
    clear()
    logo = f"""
    {Fore.RED}     ▄████████  ▄██████▄  ████████▄     ▄████████  ▀████    ▐████▀ 
    {Fore.LIGHTRED_EX}    ███    ███ ███    ███ ███    ███   ███    ███    ███▌   ████▀  
    {Fore.RED}    ███    █▀  ███    ███ ███    ███   ███    █▀      ███  ▐███    
    {Fore.LIGHTRED_EX}   ▄███▄▄▄     ███    ███ ███    ███  ▄███▄▄▄          ▀███▄███▀     
    {Fore.RED}  ▀▀███▀▀▀     ███    ███ ███    ███ ▀▀███▀▀▀          ▄███▀██▄      
    {Fore.LIGHTRED_EX}    ███    █▄  ███    ███ ███    ███   ███    █▄      ███  ▐███    
    {Fore.RED}    ███    ███ ███    ███ ███    ███   ███    ███    ███▌   ████▀  
    {Fore.LIGHTRED_EX}    ██████████  ▀██████▀  ████████▀    ██████████  ▄████    ▐████▀ 
    """
    print(logo)
    print(f"        {Fore.WHITE}--- THE PREMIUM GAME HUB BY ALI ZAIN HASAN ---{Style.RESET_ALL}\n")
    time.sleep(1.5)

def display_menu():
    clear()
    print("\n")
    print(f"{Fore.RED}===============================================================")
    print(f"  {Fore.LIGHTRED_EX}CODEX-RETURNS v3.0{Fore.RED}  |  {Fore.WHITE}Premium Game Hub{Fore.RED}             ")
    print(f"  {Fore.YELLOW}Cache: {CACHE_SIZE / (1024*1024):.1f}MB / 300MB")
    if gh:
        print(f"  {Fore.GREEN}✓ PyGithub API Connected (5000 req/hr)")
    print(f"{Fore.RED}==============================================================={Style.RESET_ALL}\n")
    
    print(f"  {Fore.RED}[ AVAILABLE GAMES ]\n")
    
    games_list = [
        ("1", "3kh0", 8001),
        ("2", "Arsenic", 8003),
        ("3", "Eaglercraft", 8004),
        ("4", "GameBoy", 8005),
        ("5", "GN-Math", 8006),
        ("6", "JeoWeb", 8007),
        ("7", "MonkeyGG", 8008),
        ("8", "Selenite", 8009),
    ]
    
    for num, name, port in games_list:
        print(f"  {Fore.LIGHTRED_EX}[{num}]{Fore.WHITE}  {name:<18}  {Fore.RED}|  Port: {Fore.LIGHTRED_EX}{port}")
    
    print(f"\n  {Fore.LIGHTRED_EX}[9]{Fore.WHITE}  Exit System\n")

def launch_game(game_info):
    clear()
    print("\n")
    print(f"  {Fore.LIGHTRED_EX}[*]{Fore.WHITE} INITIALIZING: {game_info['name']}")
    print(f"  {Fore.RED}[*]{Fore.WHITE} Starting PyGithub-powered server...{Style.RESET_ALL}")
    animate_progress_bar(1.2)
    
    server_thread = threading.Thread(
        target=start_server, 
        args=(game_info["repo"], game_info["index_path"], game_info["port"], game_info.get("branch", "main")), 
        daemon=True
    )
    server_thread.start()
    
    time.sleep(0.8)
    print(f"  {Fore.GREEN}[OK]{Fore.WHITE} Local Server established on port {game_info['port']}")
    print(f"  {Fore.GREEN}[OK]{Fore.WHITE} PyGithub API streaming enabled")
    
    time.sleep(0.8)
    
    url = f"http://localhost:{game_info['port']}"
    if copy_to_clipboard(url):
        print(f"  {Fore.GREEN}[OK]{Fore.WHITE} URL copied to clipboard!")
    else:
        print(f"  {Fore.YELLOW}[!]{Fore.WHITE} Could not copy to clipboard")
    
    time.sleep(1)
    
    clear()
    print("\n")
    print(f"{Fore.RED}===============================================================")
    print(f"  {Fore.GREEN}SESSION ACTIVE{Fore.RED}                                         ")
    print(f"{Fore.RED}===============================================================")
    print(f"                                                               ")
    print(f"  {Fore.WHITE}GAME:{Fore.RED}    {Fore.LIGHTRED_EX}{game_info['name']:<48}")
    print(f"  {Fore.WHITE}STATUS:{Fore.RED}  {Fore.GREEN}PyGithub Streaming{Fore.RED:<24}")
    print(f"                                                               ")
    print(f"  {Fore.LIGHTGREEN_EX}URL:{Fore.RED}      {Fore.WHITE}http://localhost:{game_info['port']:<39}")
    print(f"  {Fore.YELLOW}HINT:{Fore.RED}     Paste the URL in your browser              ")
    print(f"                                                               ")
    print(f"{Fore.RED}===============================================================")
    print(f"                                                               ")
    print(f"  Press CTRL+C to Terminate and Return to Hub                 ")
    print(f"                                                               ")
    print(f"==============================================================={Style.RESET_ALL}\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n  {Fore.YELLOW}[!]{Fore.WHITE} Terminating server...")
        time.sleep(0.8)

def main():
    if not show_login_screen():
        return
    
    show_splash_screen()
    
    while True:
        display_menu()
        choice = input(f"{Fore.LIGHTRED_EX}System@CodeX:~${Style.RESET_ALL} ").strip()
        
        if choice == "9":
            clear()
            print("\n")
            print(f"  {Fore.RED}[*] Shutting down systems... Goodbye.{Style.RESET_ALL}\n")
            time.sleep(1)
            sys.exit()
        elif choice in GAMES:
            launch_game(GAMES[choice])
        else:
            print(f"  {Fore.RED}X Invalid Command.{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == "__main__":
    main()