#informationgathering
import sys
import requests
import socket
import json

if len(sys.argv) < 2:
    print("usage: " + sys.argv[0] + " <url>")
    sys.exit(0)

url = sys.argv[1]

try:
    # Fetch headers from the URL
    req = requests.get("https://" + url)
    print("\n" + str(req.headers))
    
    # Get the IP address of the URL
    gethostby = socket.gethostbyname(url)
    print("The IP of " + url + " is " + gethostby + "\n")
    
    # Fetch IP information
    req_ = requests.get("https://ipinfo.io/" + gethostby + "/json")
    resp = json.loads(req_.text)
    
    # Print location and region
    if 'loc' in resp:
        print("Location: " + resp["loc"])
    else:
        print("Location information not available.")
    
    if 'region' in resp:
        print("Region: " + resp["region"])
    else:
        print("Region information not available.")
        
except requests.RequestException as e:
    print(f"Error fetching data from URL: {e}")
except socket.gaierror as e:
    print(f"Error getting IP address: {e}")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON response: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
