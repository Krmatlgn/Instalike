import os
try:
    import requests,colorama,prettytable,webbrowser
except:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install prettytable")
    os.system("pip install webbrowser")
import threading, requests, ctypes, random, json, time, base64, sys, re
from prettytable import PrettyTable
import random
from time import strftime
import webbrowser
from colorama import init, Fore
from urllib.parse import urlparse, unquote, quote
from string import ascii_letters, digits

xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;37m"
whiteb="\033[1;37m"
red="\033[0;31m"
redb="\033[1;31m"
end='\033[0m'

banner="""
 """
for X in banner:
  sys.stdout.write(X)
  sys.stdout.flush() 

class Zefoy:
    

    def get_captcha(self):
        if os.path.exists('session'): self.session.cookies.set("PHPSESSID", open('session',encoding='utf-8').read(), domain='zefoy.com')
        request = self.session.get(self.base_url, headers=self.headers)
        if 'Enter Video URL' in request.text: self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]; return True

        try:
            for x in re.findall(r'<input type="hidden" name="(.*)" value="(.*)">', request.text): self.captcha_[x[0]] = x[1]

            self.captcha_1 = request.text.split('type="text" name="')[1].split('" oninput="this.value=this.value.toLowerCase()"')[0]
            captcha_url = request.text.split('<img src="')[1].split('" onerror="imgOnError()" class="')[0]
            request = self.session.get(f"{self.base_url}{captcha_url}",headers=self.headers)
            open('captcha.png', 'wb').write(request.content)
            print('Captcha solving....')
            return False
        except Exception as e:
            time.sleep(2)
            self.get_captcha()

    def send_captcha(self, new_session = False):
        if new_session: self.session = requests.Session(); os.remove('session'); time.sleep(2)
        if self.get_captcha():
            return (True, 'The session already exists')
        captcha_solve = self.solve_captcha('captcha.png')[1]
        self.captcha_[self.captcha_1] = captcha_solve
        request = self.session.post(self.base_url, headers=self.headers, data=self.captcha_)

        if 'Enter Video URL' in request.text: 
            open('session','w',encoding='utf-8').write(self.session.cookies.get('PHPSESSID'))
            self.video_key = request.text.split('" placeholder="Enter Video URL"')[0].split('name="')[-1]
            return (True,captcha_solve)
        else: return (False,captcha_solve)

    def solve_captcha(self, path_to_file = None, b64 = None, delete_tag = ['\n','\r']):
        if path_to_file: task = path_to_file
        else: open('temp.png','wb').write(base64.b64decode(b64)); task = 'temp.png'
        request = self.session.post('https://api.ocr.space/parse/image?K87899142388957', headers={'apikey':'K87899142388957'}, files={'task':open(task,'rb')}).json()
        solved_text = request['ParsedResults'][0]['ParsedText']
        for x in delete_tag: solved_text = solved_text.replace(x,'')
        return (True, solved_text)

    def get_status_services(self):
        request = self.session.get(self.base_url, headers=self.headers).text
        for x in re.findall(r'<h5 class="card-title">.+</h5>\n.+\n.+', request): self.services[x.split('<h5 class="card-title">')[1].split('<')[0].strip()] = x.split('d-sm-inline-block">')[1].split('</small>')[0].strip()
        for x in re.findall(r'<h5 class="card-title mb-3">.+</h5>\n<form action=".+">', request): self.services_ids[x.split('title mb-3">')[1].split('<')[0].strip()] = x.split('<form action="')[1].split('">')[0].strip()
        return (True,self.services)

    def get_status_service(self, service = None, service_id = None):
        if service: service_id = self.services_ids[service]
        request = self.session.get(f"{self.base_url}{service_id}", headers=self.headers).text
        limit_ = request.split('class="text-muted">Quota: ')[1].split('</small>')[0]
        current_ = request.split('class="text-muted">Used: ')[1].split('</small>')[0]
        end_ = request.split('class="text-muted">Ends: ')[1].split('</small>')[0]
        return (True,{'limit':limit_,'current':current_,'end':end_})

    def increase_view(self, service = None, service_id = None):
        if service: service_id = self.services_ids[service]
        request = self.session.post(f"{self.base_url}{service_id}", headers=self.headers, data=self.captcha_)
        if 'data-href="javascript:void(0)" data-toggle="tooltip"' in request.text: return (True,f'{service} increase view successfully')
        else: return (False,'Captcha incorrect')

    def __init__(self):
        self.session = requests.Session()
        self.services = {}
        self.services_ids = {}
        self.headers = {
            'authority': 'zefoy.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'dnt': '1',
            'x-csrf-token': 'yGd4wJ8QW6vInzzQG2De2x4dSeKysSGbNhK1SflL',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://zefoy.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://zefoy.com/',
            'accept-language': 'en-US,en;q=0.9'
        }
        self.base_url = 'https://zefoy.com/'


if __name__ == '__main__':
    pass
