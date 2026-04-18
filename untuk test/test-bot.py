import requests

BOT_TOKEN = "8700160160:AAFc9EpQSOLUce9DUHBWdeurKftLkJbTjeM"
CHAT_ID ='-5280260003'

pesan = "Test dari Python 🚀"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": pesan
})

print(response.status_code)
print(response.text)