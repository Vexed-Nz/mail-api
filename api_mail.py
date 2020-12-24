import requests
import random, string
from json import loads
from time import sleep
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Main Api Settings
url = 'https://api.mail.tm/'

def headers():
    headers = {
        "User-Agent": UserAgent().random,
        "content-type": "application/ld+json",
        "accept": "application/ld+json",
        "Connection": "keep-alive",
    }
    return headers

def collectinfo(token):
  headers = {
    "User-Agent": UserAgent().random,
    "content-type": "application/ld+json",
    "accept": "application/ld+json",
    "Connection": "keep-alive",
    "authorization": f"Bearer {token}",
  }
  return headers

# Gets List Of Domains
for x in range(10):
  sleep(0.5)
  domain = requests.get(url+f'domains?page={x+1}', headers=headers()).text
  parsed = loads(domain)
  try:
    if parsed["hydra:member"][0]["domain"]:
      print(f'[+] Found Domain at Page {x+1} = {parsed["hydra:member"][0]["domain"]}')
      break
  except:
    print(f'No Domain Found at Page {x+1}')
    if x+1 == 10:
      print("[-] No Domains Found Exiting...")
      exit()

# Create Email Account
ranum = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

email = f'{ranum}@{parsed["hydra:member"][0]["domain"]}'
payload = '{"address":'+f'"{email}"'+',"password":"alt_token"}'
response = requests.post('https://api.mail.tm/accounts', headers=headers(), data=payload)
print(response.json()['address'])
idacc = response.json()['id']

# Get Token and account id
response = requests.post('https://api.mail.tm/authentication_token', headers=headers(), data=payload)
token = response.json()['token']

# Get Account Info
r = requests.get(url+'accounts/'+idacc, headers=collectinfo(token))
info = r.text
print(loads(info))

# Get Messages
# r = requests.get(url+'messages?page=1', headers=collectinfo(token))
# messageid = loads(r.text)['hydra:member'][0]['id']

# View Messages
# r = requests.get(url+f'messages/{messageid}', headers=collectinfo(token))
# messageinfo = str(loads(r.text)['html']).replace("['", "").replace("']", "")

# You Can Customize and Parse html
# soup = BeautifulSoup(messageinfo, 'html.parser')
# for link in soup.find_all('a'):
#     print(link.get('href'))

# Delete Account
r = requests.delete(url+f'accounts/{idacc}', headers=collectinfo(token))
print(f'[+] {r} - Account resource deleted')