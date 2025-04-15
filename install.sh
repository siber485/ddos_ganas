#!/bin/bash
pkg update && pkg upgrade -y
pkg install python -y
cp ddos_ganas.py /data/data/com.termux/files/usr/bin/ddos
chmod +x /data/data/com.termux/files/usr/bin/ddos
echo "Install selesai! Sekarang tinggal ketik: ddos"
