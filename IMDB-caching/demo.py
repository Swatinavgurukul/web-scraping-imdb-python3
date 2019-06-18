import requests
data = requests.get("https://honored-dirigible.glitch.me/session")
print(data.text)