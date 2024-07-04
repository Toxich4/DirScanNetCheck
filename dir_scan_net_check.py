import os
import sys
import argparse
import requests
from datetime import datetime
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_files_in_directory(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                file_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                if sys.platform == "win32":
                    file_path = file_path.replace('\\', '/')
                file.write(file_path + '\n')

def check_urls_from_file(file_path, base_url, delay, headers, cookies, proxy, status_codes, verify_ssl):
    with open(file_path, 'r', encoding='utf-8') as file:
        paths = file.readlines()

    proxies = {"http": proxy, "https": proxy} if proxy else None

    for path in paths:
        url = base_url.rstrip('/') + '/' + path.strip()
        try:
            response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, allow_redirects=True, timeout=30, verify=verify_ssl)
            current_time = datetime.now().strftime('%H:%M:%S')
            if response.status_code in status_codes:
                size_kb = sum(len(chunk) for chunk in response.iter_content(1024))
                print(f"[{current_time}] {response.status_code} - {size_kb:.0f}KB - {path.strip()}")
            time.sleep(delay)
        except requests.Timeout:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] Server did not respond within 30 seconds. Server might be unavailable.")
            sys.exit(1)
        except requests.RequestException as e:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] Error occurred: {e}")

def get_user_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['yes', 'no', 'y', 'n']:
            return user_input
        else:
            print("Invalid input. Please enter 'yes', 'no', 'y', or 'n'.")

def main():
    parser = argparse.ArgumentParser(description="File Scanner and URL Checker")
    parser.add_argument('-w', '--write', type=str, help="File path to write the directory listing")
    parser.add_argument('-s', '--sleep', type=int, default=0, help="Delay between requests in seconds")
    parser.add_argument('-C', '--cookies', type=str, help="Cookies to use for the requests")
    parser.add_argument('-H', '--headers', action='append', help="Headers to use for the requests")
    parser.add_argument('--proxy', type=str, help="HTTP proxy to use for the requests")
    parser.add_argument('--no-verify', action='store_true', help="Disable SSL certificate verification")
    
    args = parser.parse_args()

    headers = {}
    cookies = {}
    proxy = args.proxy
    verify_ssl = not args.no_verify

    if args.cookies:
        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in args.cookies.split('; ')}

    if args.headers:
        for header in args.headers:
            header_key, header_value = header.split(': ', 1)
            headers[header_key] = header_value

    if args.write:
        output_file = args.write
        if not os.path.isfile(output_file):
            print(f"File {output_file} does not exist.")
            sys.exit(1)
    else:
        current_directory = os.getcwd()
        user_input = input("Do you want to scan the current directory? (yes/no): ").strip().lower()
        if user_input in ['yes', 'y']:
            root_directory = current_directory
        else:
            root_directory = input("Please enter the path to the source code directory: ").strip()

        output_file = "file_paths.txt"
        list_files_in_directory(root_directory, output_file)
        print(f"File paths have been written to {output_file}")

    user_input = input("Do you want to check if these files are accessible from the network? (yes/no): ").strip().lower()
    if user_input in ['yes', 'y']:
        base_url = input("Please enter the host in the format http(s)://host: ").strip()
        status_codes_input = input("Enter HTTP status codes to check (comma-separated, e.g., 200,404): ").strip()
        if status_codes_input:
            status_codes = [int(code.strip()) for code in status_codes_input.split(',')]
        else:
            status_codes = [200]
        check_urls_from_file(output_file, base_url, args.sleep, headers, cookies, proxy, status_codes, verify_ssl)
    else:
        print("Script finished.")

if __name__ == "__main__":
    main()