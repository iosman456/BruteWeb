import socket
import requests
import whois

class NetworkTools:
    @staticmethod
    def get_ip_address(domain):
        try:
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.gaierror:
            return None

    @staticmethod
    def get_domain_info(domain):
        try:
            domain_info = whois.whois(domain)
            return domain_info
        except Exception as e:
            return str(e)

    @staticmethod
    def get_server_info(ip_address):
        try:
            response = requests.get(f"https://ipinfo.io/{ip_address}/json")
            return response.json()
        except requests.RequestException as e:
            return str(e)
