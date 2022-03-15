import time
import requests
import random
import os, sys
from colorama import Fore
from bs4 import BeautifulSoup
from functools import partial
from urllib.parse import urlencode
from requests.exceptions import Timeout
from unittest.mock import NonCallableMagicMock
from concurrent.futures import ThreadPoolExecutor


#Main
url = 'https://docs.google.com/forms/d/e/1FAIpQLSc8iLMel2C4oeET2iO8rry5WN9WhdRwbRWMJFGVNstI-k7rcg/formResponse' #Only /viewform, Don't use /formResponse
get_forminfo = True
get_status = True
#Mode
mode = 'report' #'spam', 'report'
report_reason = 'HATE_SPEECH' #'random' or 'NUDITY', 'HATE_SPEECH', 'SPAM', 'PERSONAL_INFO'
#Settings
text_name = 'files/list3.txt'
user_agent_name = 'files/user-agents.txt'
loop_count = 40 #10 ~ 100,000
group = 10 #10 ~ 100
#Options
show_text = False
show_proxylog = False
check_ip = True
#Timeout
fixtimeout = True
sleep_time = 2
count_range = 6
timeout = 4 #4s ~ 6s
#Power
thread = 50 #Thread = CPU Core x10
#Proxy(Doesn't work)
proxy = False
proxy_type = 'http' #'http', 'socks5', 'None'
proxy_name = 'proxy/proxy2.txt'
socks5_name = 'files/socks5.txt'
#Error
connection_error = True
#Debug
instant_stop = False


def spam():
    try:
        urls = []
        success = 0
        failed = 0
        phase = 0
        count = 1
        for i in range(loop_count):
            ua = random.choice(open(user_agent_name).readlines())
            proxy = (random.choice(open(proxy_name).readlines())).strip()
            text = random.choice(open(text_name).readlines())
            print(f'--------------------------------------------------------------------------------------')
            headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Connection': 'keep-alive',
                    'content-type': 'application/x-www-form-urlencoded',
                    'user-agent': ua.strip(),
            }
            key = {
                'entry.978817825': text + 'FuckYou',
                'entry.1854205279': text + 'FuckYou',
                'entry.998520063': '114514',
                'entry.864233501': text + 'FuckYou',
            }
            if mode == 'spam':
                main_url = '%s?%s' % (url, urlencode(key))
                for i in range(group):
                    urls.append(main_url)
            elif mode == 'report':
                report()
            if show_proxylog == True:
                log_proxy = proxy
            elif show_proxylog == False:
                log_proxy = 'None'
            t1 = time.time()
            try:
                r = requests.get(main_url, headers=headers, timeout=4)
                try:
                    mapfunc = partial(requests.get, headers=headers, timeout=4)
                    with ThreadPoolExecutor(thread) as executor:
                        results = list(executor.map(mapfunc, urls))
                    t2 = time.time()
                    t3 = t2 - t1
                    if r.status_code == 200:
                        success += len(urls)
                        print(f'{Fore.LIGHTGREEN_EX}Successfully Responsed!{Fore.RESET}')
                        if show_proxylog == True:
                            print(f'Proxy: {Fore.LIGHTMAGENTA_EX}{log_proxy}{Fore.RESET}')
                        print(f'Status: {Fore.GREEN}200, OK{Fore.RESET}')
                        print(f'Success: {Fore.LIGHTCYAN_EX}{success}{Fore.RESET}, Failed: {Fore.RED}{failed}{Fore.RESET}, Phase:{count}')
                        print(f'Time: {t3}')
                        if show_text == True:
                            print(f'Text: {text}')
                        print('--------------------------------------------------------------------------------------')
                    elif r.status_code == 429:
                        failed += len(urls)
                        print(f'{Fore.BLUE}Rate limited{Fore.RESET}')
                        if show_proxylog == True:
                            print(f'Proxy: {Fore.LIGHTMAGENTA_EX}{log_proxy}{Fore.RESET}')
                        print(f'Status: {Fore.RED}429, Too many connections{Fore.RESET}')
                        print(f'Success: {Fore.LIGHTCYAN_EX}{success}{Fore.RESET}, Failed: {Fore.RED}{failed}{Fore.RESET}, Phase:{count}')
                        print(f'Time: {t3}')
                        print('--------------------------------------------------------------------------------------')
                    else:
                        failed += len(urls)
                        print(f'{Fore.RED}Bad Connection{Fore.RESET}')
                        if show_proxylog == True:
                            print(f'Proxy: {Fore.LIGHTMAGENTA_EX}{log_proxy}{Fore.RESET}')
                        print(f'Status: {Fore.RED}{r.status_code}{Fore.RESET}')
                        print(f'Success: {Fore.LIGHTCYAN_EX}{success}{Fore.RESET}, Failed: {Fore.RED}{failed}{Fore.RESET}, Phase:{count}')
                        print('--------------------------------------------------------------------------------------')
                except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                    failed += len(urls)
                    print(f'{Fore.RED}Bad Connection{Fore.RESET}')
                    if show_proxylog == True:
                            print(f'Proxy: {Fore.LIGHTMAGENTA_EX}{log_proxy}{Fore.RESET}')
                    print(f'Status: {Fore.RED}{r.status_code}{Fore.RESET}')
                    print('--------------------------------------------------------------------------------------')
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                failed += len(urls)
                print(f'{Fore.RED}TimeOut{Fore.RESET}')
                print(f'Status: {Fore.RED}{r.status_code}{Fore.RESET}')
                print(f'Success: {Fore.LIGHTCYAN_EX}{success}{Fore.RESET}, Failed:{failed}, Phase:{count}')
                print(f'Time: {t3}')
                print('--------------------------------------------------------------------------------------')
            phase += 1
            count += 1
            if phase == count_range:
                phase = 0
                count = 1
                if fixtimeout == True:
                    print(f'Sleeping....{Fore.LIGHTMAGENTA_EX}{sleep_time}{Fore.RESET}sec....')
                    time.sleep(sleep_time)
    except KeyboardInterrupt:
        s = input('Stop request. Restart now?(y/n) : ')
        if s == 'y':
            spam()
        elif s == 'n':
            sys.exit()

def report():
    s1 = input('Total report number of times?: ') #50 ~ 10,000
    report_url = url.replace('formResponse', 'submitabuse')
    repors = []
    success_r = 0
    failed_r = 0
    count_r = 1
    phase_r = 0
    for i in range(group):
        repors.append(report_url)
    try:
        for i in range(loop_count):
            ua = random.choice(open(user_agent_name).readlines())
            reason_list = ['NUDITY', 'HATE_SPEECH', 'SPAM', 'PERSONAL_INFO']
            if report_reason == 'random':
                reason = random.choice(reason_list)
            elif report_reason != 'random':
                reason = report_reason
            print('--------------------------------------------------------------------------------------')
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'content-type': 'application/x-www-form-urlencoded',
                'user-agent': ua.strip(),
            }
            data = {
                    'abuseCategory': reason,
            }
            t4 = time.time()
            try:
                r = requests.post(report_url, headers=headers, data=data, timeout=timeout)
                try:
                    mapfunc = partial(requests.post, headers=headers, data=data, timeout=timeout)
                    with ThreadPoolExecutor(thread) as executor:
                        results = list(executor.map(mapfunc, repors))
                    t5 = time.time()
                    t6 = t5 - t4
                    if r.status_code == 200:
                        success_r += len(repors)
                        print(f'{Fore.LIGHTGREEN_EX}Successfully Reported!!{Fore.RESET}')
                        print(f'Status: {Fore.GREEN}200, OK{Fore.RESET}')
                        print(f'Success: {Fore.LIGHTCYAN_EX}{success_r}{Fore.RESET}, Failed: {Fore.RED}{failed_r}{Fore.RESET}, Phase:{count_r}')
                        print(f'Time: {t6}')
                        if show_text == True:
                            print(f'Report Reason: {reason}')
                        print('--------------------------------------------------------------------------------------')
                    elif r.status_code == 429:
                        failed_r += len(repors)
                        print(f'{Fore.BLUE}Rate limited{Fore.RESET}')
                        print(f'Status: {Fore.RED}429, Too many connections{Fore.RESET}')
                        print(f'Success: {Fore.LIGHTCYAN_EX}{success_r}{Fore.RESET}, Failed: {Fore.RED}{failed_r}{Fore.RESET}, Phase:{count_r}')
                        print(f'Time: {t6}')
                        print('--------------------------------------------------------------------------------------')
                    else:
                        failed_r += len(repors)
                        print(f'{Fore.RED}Bad Connection{Fore.RESET}')
                        print(f'Status: {Fore.RED}{r.status_code}{Fore.RESET}')
                        print(f'Success: {Fore.LIGHTCYAN_EX}{success_r}{Fore.RESET}, Failed: {Fore.RED}{failed_r}{Fore.RESET}, Phase:{count_r}')
                        print('--------------------------------------------------------------------------------------')
                except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                    failed_r += len(repors)
                    print(f'{Fore.RED}Bad Connection{Fore.RESET}')
                    print(f'Status: {Fore.RED}{r.status_code}{Fore.RESET}')
                    print('--------------------------------------------------------------------------------------')
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                failed_r += len(repors)
                print(f'TimeOut..')
                print(f'Status: {Fore.RED}{r.status_code}{Fore.RESET}')
                print(f'Success: {Fore.LIGHTCYAN_EX}{success_r}{Fore.RESET}, Failed:{failed_r}, Phase:{count_r}')
                print(f'Time: {t6}')
                print('--------------------------------------------------------------------------------------')
            phase_r += 1
            count_r += 1
            if phase_r == count_range:
                phase_r = 0
                count_r = 1
                if fixtimeout == True:
                    print(f'Sleeping....{Fore.LIGHTMAGENTA_EX}{sleep_time}{Fore.RESET}sec....')
                    time.sleep(sleep_time)
            if success_r > float(s1):
                print(f'Total Report: {Fore.LIGHTYELLOW_EX}{success_r}{Fore.RESET}')
                s = input('Restart Report?(y/n) : ')
                if s == 'y':
                    report()
                elif s == 'n':
                    sys.exit()
    except KeyboardInterrupt:
        s = input('Stop request. Restart now?(y/n) : ')
        if s == 'y':
            report()
        elif s == 'n':
            sys.exit()

def check_ipinfo():
    data = requests.get("http://ipinfo.io/json").json()
    ip = data['ip']
    if ip == '106.181.72.186' or '192.168.100.105':
        print(f'Your IP: {Fore.LIGHTRED_EX}{ip}{Fore.RESET}, VPN: {Fore.LIGHTRED_EX}False{Fore.RESET}')
        print(f'{Fore.LIGHTYELLOW_EX}Worning: Please be careful about speed and number of times.{Fore.RESET}')
    else:
        print(f'Your IP: {Fore.LIGHTGREEN_EX}{ip}{Fore.RESET}, VPN: {Fore.LIGHTMAGENTA_EX}True{Fore.RESET}')
        print(f'{Fore.LIGHTGREEN_EX}Success: VPN is True. Enjoy raiding life!{Fore.RESET}')

def set():
    os.system('clear')
    print('----------------------------------------------------------------------------------------------------')
    print(f'URL: {url}')
    if mode == 'spam':
        print(f'Mode: {Fore.LIGHTRED_EX}Spam{Fore.RESET}')
    elif mode == 'report':
        print(f'Mode: {Fore.LIGHTRED_EX}Report{Fore.RESET}')
    if proxy == True:
        if proxy_type == 'http':
            print(f'Proxy type: {Fore.LIGHTGREEN_EX}HTTP/s{Fore.RESET}')
        elif proxy_type == 'socks5':
            print(f'Proxy type: {Fore.LIGHTBLUE_EX}Socks5{Fore.RESET}')
    print(f'Group: {group}')
    if get_forminfo == True:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        try:
            title = soup.find(class_="F9yp7e ikZYwf G4EHhc").text
            entry = soup.find(class_="HoXoMd D1wxyf G4EHhc").text
            ent = entry.replace('*', '(必須)')
        except AttributeError:
            title = 'None'
            ent = 'None'
        if check_ip == True:
            check_ipinfo()
        if get_status == True:
            sts = requests.get(url)
            if sts.status_code == 200:
                print(f'Status: {Fore.LIGHTGREEN_EX}200, OK{Fore.RESET}')
            elif sts.status_code == 429:
                print(f'Status: {Fore.LIGHTRED_EX}429, Please change VPN.{Fore.RESET}')
                sys.exit()
            else:
                print(f'Status: {Fore.LIGHTRED_EX}{sts}{Fore.RESET}')
                sys.exit()
        elif get_status == False:
            print('Status: None')
        print('┌---------------------------------------------------------------------┐')
        print(f'├ FormTitle: {title}')                                               
        print(f'├ First Question: {ent}')
        print('└---------------------------------------------------------------------┘')        
    if instant_stop == True:
        sys.exit()
    spam()

set()