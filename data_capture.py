import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

INTERFACE = "en0"  
DURATION = 15      
OUTPUT_DIR = "./captures/stack_overflow"
SITE = "https://www.stackoverflow.com"
LABEL = "stackoverflow2" 

os.makedirs(OUTPUT_DIR, exist_ok=True)
pcap_path = os.path.join(OUTPUT_DIR, f"{LABEL}.pcap")

print(f"[+] Starting tcpdump on {INTERFACE} to capture traffic to {SITE}")
tcpdump_proc = subprocess.Popen(
    ["sudo", "tcpdump", "-i", INTERFACE, "-w", pcap_path],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(2)  

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

print("[+] Stopping tcpdump...")
tcpdump_proc.terminate()
tcpdump_proc.wait()

print(f"[✓] Done. Capture saved to {pcap_path}")
