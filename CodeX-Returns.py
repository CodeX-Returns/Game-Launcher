import requests
import webbrowser
import http.server
import socketserver
import threading
import os
import sys
import time
import pyperclip
import logging
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Suppress all server logging
logging.disable(logging.CRITICAL)

# Configuration
GITHUB_USERNAME = "CodeX-Returns"
PASSWORD = "CodeX"

GAMES = {
    "1": {"name": "3kh0", "repo": "3kh0", "port": 8001, "index_path": "index.html"},
    "2": {"name": "Arsenic", "repo": "Arsenic", "port": 8003, "index_path": "public/index.html"},
    "3": {"name": "Eaglercraft", "repo": "Eaglercraft", "port": 8004, "index_path": "index.html"},
    "4": {"name": "GameBoy", "repo": "GameBoy", "port": 8005, "index_path": "index.html"},
    "5": {"name": "GN-Math", "repo": "GN-Math", "port": 8006, "index_path": "index.html"},
    "6": {"name": "JeoWeb", "repo": "JeoWeb", "port": 8007, "index_path": "index.html"},
    "7": {"name": "MonkeyGG", "repo": "MonkeyGG", "port": 8008, "index_path": "index.html"},
    "8": {"name": "Selenite", "repo": "Selenite", "port": 8009, "index_path": "index.html"},
}

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

# --- SERVER LOGIC ---

class SilentHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    repo_name = None
    index_path = None
    
    def do_GET(self):
        file_path = self.path.split('?')[0]
        request_file = self.index_path if file_path == "/" else file_path.lstrip("/")
        url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{self.repo_name}/main/{request_file}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                if request_file.endswith(".html"):
                    content_type = "text/html; charset=utf-8"
                elif request_file.endswith(".css"):
                    content_type = "text/css"
                elif request_file.endswith(".js"):
                    content_type = "application/javascript"
                elif request_file.endswith(".json"):
                    content_type = "application/json"
                elif request_file.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
                    ext = request_file.split('.')[-1]
                    content_type = f"image/{ext if ext != 'svg' else 'svg+xml'}"
                elif request_file.endswith((".mp3", ".wav", ".ogg")):
                    content_type = f"audio/{request_file.split('.')[-1]}"
                elif request_file.endswith((".mp4", ".webm")):
                    content_type = f"video/{request_file.split('.')[-1]}"
                elif request_file.endswith(".ico"):
                    content_type = "image/x-icon"
                elif request_file.endswith(".wasm"):
                    content_type = "application/wasm"
                else:
                    content_type = "application/octet-stream"
                
                try:
                    self.send_response(200)
                    self.send_header("Content-type", content_type)
                    self.send_header("Content-Length", len(response.content))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(response.content)
                except:
                    pass
        except:
            try:
                self.send_error(404)
            except:
                pass

    def log_message(self, format, *args):
        pass

def start_server(repo_name, index_path, port):
    SilentHTTPRequestHandler.repo_name = repo_name
    SilentHTTPRequestHandler.index_path = index_path
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", port), SilentHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except:
        pass

# --- AUTHENTICATION ---

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

# --- SCREENS ---

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
    print(f"  {Fore.LIGHTRED_EX}CODEX-RETURNS v2.0{Fore.RED}  |  {Fore.WHITE}Premium Game Hub{Fore.RED}             ")
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
    print(f"  {Fore.RED}[*]{Fore.WHITE} Connecting to GitHub Repository...{Style.RESET_ALL}")
    animate_progress_bar(1.5)
    
    # Start server
    server_thread = threading.Thread(
        target=start_server, 
        args=(game_info["repo"], game_info["index_path"], game_info["port"]), 
        daemon=True
    )
    server_thread.start()
    
    time.sleep(0.8)
    print(f"  {Fore.GREEN}[OK]{Fore.WHITE} Local Server established on port {game_info['port']}")
    print(f"  {Fore.GREEN}[OK]{Fore.WHITE} Streaming from {GITHUB_USERNAME}")
    
    time.sleep(0.8)
    
    # Copy URL to clipboard
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
    print(f"  {Fore.WHITE}STATUS:{Fore.RED}  {Fore.GREEN}Streaming from {GITHUB_USERNAME:<39}")
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
    # Authentication
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