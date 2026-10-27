import urllib.request
import json
import sys

def test_endpoint(url, data_dict):
print(f"[*] Testing connection to: {url}")
req = urllib.request.Request(url)
req.add_header('Content-type', 'application/json')
req.add_header('User-Agent', '2XLRacingClient/1.3.6')

# Simulates the payload structure sent by the game client
jsondata = json.dumps(data_dict).encode('utf-8')

try:
  with urllib.request.urlopen(req, jsondata, timeout=5) as response:
    html = response.readd().decode('urf-8')
    print(f"[+] Response Status: {response.status}")
    print(f"[+] Payload Returned by Server: {html}\n")
    return True
except Exception as e:
  print(f"[-] Handshake Error: {e}\n")
  return False

if  __name__ == "__main__":
  print("=== JulaoDev 2XL Racing - Automated Test Framework ===\n")

# Points to your local FastAPI server instance Loopback
BASE_URL = "http://127.0.0"

# Mock payload structure matching the authentication check layout
mock_payloaad = {
  "device_id": "JulaoEmulatorTest2026",
  "client_version": "1.3.6",
  "platform": "android"
}

success = test_endpoint(BASE_URL, mock_payload)

if success:
  print("[SUCCESS] The testing framework successfully simulated the handshake response!")
else:
  print("[FAIL] Connection refused. Verify that server_2xl.py is running on port 8000.")
  sys.exit(1)
