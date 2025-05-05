import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

INTERFACE = "en0"
DURATION = 15
OUTPUT_DIR = "./data/raw/cnn"
SITE = "https://www.cnn.com"
LABEL = "cnn_4"

os.makedirs(OUTPUT_DIR, exist_ok=True)
pcap_path = os.path.join(OUTPUT_DIR, f"{LABEL}.pcap")

print(f"[+] Starting tcpdump on {INTERFACE} to capture traffic to {SITE}")
tcpdump_proc = subprocess.Popen(
    ["sudo", "tcpdump", "-i", INTERFACE, "-w", pcap_path],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(3)  # Give tcpdump time to start

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

print(f"[+] Visiting {SITE}")
driver = webdriver.Chrome(options=chrome_options)
try:
    driver.set_page_load_timeout(30)
    driver.get(SITE)
    time.sleep(DURATION)
finally:
    driver.quit()

import signal

print("[+] Stopping tcpdump...")

# Send SIGINT to stop tcpdump cleanly
subprocess.run(["sudo", "kill", "-2", str(tcpdump_proc.pid)])

try:
    tcpdump_proc.wait(timeout=10)  # wait up to 10 seconds
except subprocess.TimeoutExpired:
    print("[!] tcpdump did not stop in time. Forcing termination...")
    subprocess.run(["sudo", "kill", "-9", str(tcpdump_proc.pid)])
    tcpdump_proc.wait()
