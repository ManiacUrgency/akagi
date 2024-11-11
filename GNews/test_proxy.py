import requests

# Define the proxy server (replace with your proxy)
proxies = {
    'http': 'http://133.18.234.13:80',
    'https': 'http://133.18.234.13:80'
}

# Test the proxy by making a request
try:
    response = requests.get('http://google.com', proxies=proxies, timeout=10)
    print("Proxy is working. Status code:", response.status_code)
except requests.exceptions.RequestException as e:
    print("Proxy is not working:", e)
