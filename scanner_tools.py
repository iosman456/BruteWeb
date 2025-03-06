import subprocess

class ScannerTools:
    @staticmethod
    def nmap_scan(ip_address):
        print(f"Running nmap scan on {ip_address}")
        result = subprocess.run(["nmap", "-sV", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        if result.returncode != 0:
            print("nmap scan completed with errors.")
        else:
            print("nmap scan completed successfully.")

    @staticmethod
    def nikto_scan(url):
        print(f"Running nikto scan on {url}")
        result = subprocess.run(["nikto", "-h", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        if result.returncode != 0:
            print("nikto scan completed with errors.")
        else:
            print("nikto scan completed successfully.")

    @staticmethod
    def wpscan(url):
        print(f"Running wpscan on {url}")
        result = subprocess.run(["wpscan", "--url", url, "--disable-tls-checks"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        if result.returncode != 0:
            print("wpscan completed with errors.")
        else:
            print("wpscan completed successfully.")

    @staticmethod
    def sqlmap_scan(url):
        print(f"Running sqlmap on {url}")
        result = subprocess.run(["sqlmap", "-u", url, "--batch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        if result.returncode != 0:
            print("sqlmap scan completed with errors.")
        else:
            print("sqlmap scan completed successfully.")
