import requests

content = requests.get("https://fm-forum.ru/search.php?action=search&keywords=&author=dianagureev")

print(content.text)