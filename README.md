# CodeX-Returns Game Hub v1.0

# Go to the [Releases](https://github.com/CodeX-Returns/Game-Launcher/releases/tag/CodeX) Tab to install the latest version of CodeX

## Overview

CodeX-Returns is a premium terminal-based game launcher that streams games directly from GitHub repositories. It provides a secure, password-protected interface for launching and managing multiple games with a professional UI.

## Features

- Password-protected access system (3 attempts limit)
- Stream games directly from GitHub repositories
- Automatic URL copying to clipboard
- Beautiful terminal UI with progress animations
- Silent server operation (no error spam)
- Support for multiple games with custom ports
- Supports various file types (HTML, CSS, JS, Images, Audio, Video, WASM)

## System Requirements

- Python 3.6 or higher
- Windows, macOS, or Linux
- Internet connection for GitHub access

## Installation

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/CodeX-Returns/launcher.git
cd launcher
```

### Step 2: Install Required Dependencies

Run this command to install all required Python packages:

```bash
pip install colorama requests pyperclip
```

Or install from requirements.txt if available:

```bash
pip install -r requirements.txt
```

### Package Details

- **colorama** - Terminal color and styling support
- **requests** - HTTP library for GitHub file fetching
- **pyperclip** - Clipboard management for URL copying

### Step 3: Verify Installation

Test if everything is installed correctly:

```bash
python CodeX-Returns.py
```

## Usage

### Starting the Application

```bash
python CodeX-Returns.py
```

### Login

1. The application will display a login screen
2. Enter the password: `CodeX`
3. You have 3 attempts before access is denied

### Selecting a Game

1. After login, the main menu will display all available games
2. Enter the number corresponding to the game you want to play (1-8)
3. The launcher will initialize and copy the local URL to your clipboard
4. Paste the URL in your browser to access the game

### Available Games

| Number | Game | Port |
|--------|------|------|
| 1 | 3kh0 | 8001 |
| 2 | Arsenic | 8003 |
| 3 | Eaglercraft | 8004 |
| 4 | GameBoy | 8005 |
| 5 | GN-Math | 8006 |
| 6 | JeoWeb | 8007 |
| 7 | MonkeyGG | 8008 |
| 8 | Selenite | 8009 |

### Stopping a Game

Press `CTRL+C` in the terminal to stop the current game session and return to the main menu.

### Exiting the Application

From the main menu, select option `9` to exit the application.

## Configuration

### Default Password

The default password is: `CodeX`

To change the password, edit the following line in `CodeX-Returns.py`:

```python
PASSWORD = "CodeX"  # Change this to your desired password
```

### GitHub Username

The default GitHub username is: `CodeX-Returns`

To use a different GitHub account, modify:

```python
GITHUB_USERNAME = "CodeX-Returns"  # Change to your username
```

### Adding New Games

To add a new game, add an entry to the GAMES dictionary in `CodeX-Returns.py`:

```python
GAMES = {
    "9": {"name": "YourGame", "repo": "repo-name", "port": 8010, "index_path": "index.html"},
}
```

- `name`: Display name for the game
- `repo`: GitHub repository name
- `port`: Local port number (must be unique)
- `index_path`: Path to the index.html file in the repository

## How It Works

1. User enters password and authenticates
2. Main menu displays available games
3. When a game is selected, the launcher:
   - Starts a local HTTP server on the specified port
   - Fetches game files directly from GitHub on-demand
   - Copies the local URL to clipboard
   - Waits for user input to terminate
4. Files are streamed from GitHub repositories in real-time
5. No files are permanently stored locally (except during runtime)

## Technical Details

### Server Architecture

The application uses Python's built-in HTTP server (`http.server.SimpleHTTPRequestHandler`) to:
- Listen for browser requests on localhost
- Intercept requests and fetch files from GitHub raw content URLs
- Serve files with appropriate content-type headers
- Handle CORS for cross-origin requests

### GitHub Integration

Files are fetched from:
```
https://raw.githubusercontent.com/{USERNAME}/{REPO}/main/{FILE_PATH}
```

This allows streaming of any file type from public GitHub repositories.

### Port Management

Each game runs on a different port to allow multiple instances:
- Games: Ports 8001-8009
- Ensure no other applications are using these ports

## Troubleshooting

### Installation Issues

**Error: pip command not found**
- Ensure Python is properly installed
- Try using `python -m pip install` instead of `pip install`

**Error: ModuleNotFoundError**
- Reinstall dependencies: `pip install --upgrade colorama requests pyperclip`

### Runtime Issues

**Login Loop**
- Verify password is exactly `CodeX`
- Check Caps Lock is off
- You have 3 attempts maximum

**URL Not Copying to Clipboard**
- Pyperclip requires system clipboard access
- On Linux, you may need: `sudo apt-get install xclip`
- Try manually entering the localhost URL shown on screen

**Cannot Connect to Game**
- Check internet connection (needed for GitHub access)
- Verify port is not blocked by firewall
- Ensure port number is not in use by another application
- Check GitHub repository exists and is public

**Server Errors Visible**
- This is normal for connection issues (browser auto-refresh, etc.)
- Errors are suppressed in the UI
- CTRL+C and restart if needed

## Repository Structure

```
CodeX-Returns/
├── CodeX-Returns.py          # Main application file
├── README.md                 # This file
└── requirements.txt          # Python dependencies (optional)
```

## Security Notes

- Password is stored in plaintext in the script - change it for production use
- The application uses public GitHub repositories only
- All connections are HTTP (not HTTPS) on localhost - safe for local use
- No user data is transmitted or stored

## Performance Considerations

- File streaming speed depends on internet connection
- Large files may take time to load on first access
- Subsequent file accesses are faster due to browser caching
- Each game instance runs independently

## Supported File Types

- HTML Documents (.html)
- Stylesheets (.css)
- Scripts (.js)
- Data (.json)
- Images (.png, .jpg, .jpeg, .gif, .svg)
- Audio (.mp3, .wav, .ogg)
- Video (.mp4, .webm)
- WebAssembly (.wasm)
- Icons (.ico)

## Future Updates

Planned features for future versions:
- Game library management
- Custom game configuration UI
- Performance optimization
- Cross-platform improvements
- Additional security features

## Credits

Created by: Ali Zain Hasan
Version: 1.0
Released: 2026

## License

All games are owned by their respective creators.
CodeX-Returns launcher is provided as-is.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed correctly
3. Ensure GitHub repositories exist and are public
4. Check firewall and port settings

---

**Enjoy using CodeX-Returns Game Hub v1.0**
