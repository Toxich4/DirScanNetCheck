# DirScanNetCheck

DirScanNetCheck is a Python-based tool designed to scan a directory for files, list their relative paths, and check if they are accessible from a given network URL. The tool also supports various features like specifying HTTP status codes, setting request delays, using cookies, custom headers, and proxy configurations.

## Features

- **Directory Scanning**: List all files in a specified directory (recursively).
- **Network Accessibility Check**: Check if the listed files are accessible from a given network URL.
- **Custom HTTP Status Codes**: Specify which HTTP status codes to look for.
- **Request Delay**: Introduce a delay between requests.
- **Cookie Support**: Include cookies in the requests.
- **Custom Headers**: Add custom HTTP headers to the requests.
- **Proxy Support**: Use an HTTP proxy for the requests.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/DirScanNetCheck.git
    ```
2. Navigate to the project directory:
    ```bash
   cd DirScanNetCheck
    ```
3. Install dependencies:
    ```bash
   pip install -r requirements.txt
    ```

## Usage
```bash
python dir_scan_net_check.py [options]
```

## Options

- **-w, --dir PATH**: Specify the directory to scan. If not provided, the current directory is used.
- **-s, --delay SECONDS**: Set a delay between requests in seconds.
- **-C, --cookie COOKIE**: Use the provided cookie in the requests.
- **-H, --header HEADERS**: Add custom headers to the requests (e.g., --header "Referer: example.com").
- **--proxy HTTPPROXY**: Use an HTTP proxy (e.g., --proxy localhost:8080).
- **--help**: Display help information.

## Examples
# Basic Usage
Scan the current directory and check file accessibility with default settings:
```bash
python dir_scan_net_check.py
```