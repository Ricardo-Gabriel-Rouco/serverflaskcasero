import threading, time
import subprocess
import scapy.all as scapy


def ping_device(ip_addr):
    result = subprocess.run(['ping', '-c', '1', ip_addr], stdout=subprocess.PIPE)
    return result.returncode == 0



def scan_network(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast/arp_request
    answered = scapy.srp(packet, timeout=2, verbose=False)[0]
    devices = []
    for element in answered:
        devices.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return devices



known_devices = set()

def periodic_scan():
    global known_devices
    while True:
        devices = scan_network("192.168.1.0/24")  # Ajusta tu rango de red
        current_set = set(d['mac'] for d in devices)
        new = current_set - known_devices
        if new:
            # Aquí notificas al bot de Telegram
            bot.send_message(chat_id, f"¡Dispositivo(s) desconocido(s) detectado(s): {new}")
        known_devices = current_set
        time.sleep(300)  # 5 minutos

import I2C_LCD_driver
import time

lcd = I2C_LCD_driver.lcd()

lcd.lcd_display_string("Hola Raspberry", 1)  # Línea 1
lcd.lcd_display_string("Red Activa", 2)     # Línea 2
time.sleep(5)
lcd.lcd_clear()

devices = scan_network("192.168.1.0/24")
lcd.lcd_display_string(f"Disp Conect:{len(devices)}", 1)