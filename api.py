import requests

def login(username,password):
    url="http://127.0.0.1:8000/login?username=John_alex&password=12345 "
    res = requests.post(url)
    if res.status_code ==200:
       return res.json()
