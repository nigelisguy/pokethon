import requests

url = "https://pokethon-api.onrender.com/config"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    print("FULL DATA:", data)

    status = data.get("status")
    maintenance = data.get("maintenance")
    commands = data.get("commands")
    version = data.get("version")

    print("\n--- API VALUES ---")
    print("Status:", status)
    print("Maintenance:", maintenance)
    print("Version:", version)
    print("Commands:", commands)

except requests.exceptions.RequestException as e:
    print("Request failed:", e)

except ValueError:
    print("Response is not valid JSON. Raw output:")
    print(response.text)