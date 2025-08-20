from flask import Flask, render_template_string, request
# from telegram import Bot, Update
# from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters
import threading
from functions import scan_network
import time

from sqliteFlask import init_db, insert_device, get_all_devices

known_devices = set()

def periodic_scan():
    
    # Escanea la red y carga los dispositivos guardados
    results = scan_network("192.168.100.1/24")
    devices = get_all_devices()

    # Normalizar la lista de dispositivos guardados a un lookup por mac (minúsculas)
    # devices es una lista de tuplas: (id, ip, mac, name, fecha)
    devices_by_mac = {}
    for d in devices:
        if isinstance(d, tuple) and len(d) >= 4:
            mac = d[2]
            name = d[3]
            ip = d[1]
            devices_by_mac[mac.lower()] = {"mac": mac, "name": name, "ip": ip}
        # Si algún día usas dicts, puedes agregar aquí el soporte

    # Comparar results con devices_by_mac y construir devices_found
    devices_found = []
    for r in results:
        r_mac = r.get("mac") if isinstance(r, dict) else None
        r_ip = r.get("ip") if isinstance(r, dict) else None
        if not r_mac:
            continue
        key = r_mac.lower()
        if key in devices_by_mac:
            stored = devices_by_mac[key]
            name = stored.get("name")
            if not name or str(name).strip() == "":
                name = "Desconocido"
            mac_value = stored.get("mac")
        else:
            name = "Desconocido"
            mac_value = r_mac
        devices_found.append({
            "name": name,
            "mac": mac_value,
            "ip": r_ip
        })
    # print(devices_found)
    return devices_found

def background_scan():
    while True:
        devices_found = periodic_scan()  # Llama a la función que ya tienes
        # Aquí puedes agregar lógica adicional, como actualizar la base o enviar alertas
        print(f"Escaneo periódico: {len(devices_found)} dispositivos encontrados.")
        time.sleep(300)  # Espera 5 minutos antes del próximo escaneo

# Configura tu token y crea el bot
# TELEGRAM_TOKEN = 'TU_TOKEN_AQUI'
# bot = Bot(token=TELEGRAM_TOKEN)
# dispatcher = Dispatcher(bot, None, use_context=True)


# ----- Flask app -----
app = Flask(__name__)

# Interfaz simple accesible por red local
@app.route("/")
def home():
    return render_template_string('''
        <h1>Servidor Flask en Raspberry Pi</h1>
        <form action="/enviar_telegram" method="post">
            <input name="mensaje" placeholder="Mensaje a Telegram">
            <button type="submit">Enviar a Telegram</button>
        </form>
    ''')

@app.route("/scan", methods=["GET"])
def scan_network_route():
    # Escanea la red y carga los dispositivos guardados
    results = scan_network("192.168.100.1/24")
    for r in results:
        if not isinstance(r, dict):
            continue
        ip = r.get("ip")
        mac = r.get("mac")
        if not ip or not mac:
            continue
        insert_device(ip, mac)
    
    devices = get_all_devices()
    # print(devices)


    # Normalizar la lista de dispositivos guardados a un lookup por mac (minúsculas)
    # devices es una lista de tuplas: (id, ip, mac, name, fecha)
    devices_by_mac = {}
    for d in devices:
        if isinstance(d, tuple) and len(d) >= 4:
            mac = d[2]
            name = d[3]
            ip = d[1]
            devices_by_mac[mac.lower()] = {"mac": mac, "name": name, "ip": ip}
        # Si algún día usas dicts, puedes agregar aquí el soporte

    # Comparar results con devices_by_mac y construir devices_found
    devices_found = []
    for r in results:
        r_mac = r.get("mac") if isinstance(r, dict) else None
        r_ip = r.get("ip") if isinstance(r, dict) else None
        if not r_mac:
            continue
        key = r_mac.lower()
        if key in devices_by_mac:
            stored = devices_by_mac[key]
            name = stored.get("name")
            if not name or str(name).strip() == "":
                name = "Desconocido"
            mac_value = stored.get("mac")
        else:
            name = "Desconocido"
            mac_value = r_mac
        devices_found.append({
            "name": name,
            "mac": mac_value,
            "ip": r_ip
        })
    # print(devices_found)
    return devices_found


@app.route("/scan/add", methods=["POST"])
def add_device():
    data = request.get_json()
    print(data)
    name = data["name"]
    mac = data["mac"]
    ip = data["ip"]
    if not mac or not ip:
        return "Faltan campos obligatorios (mac, ip).", 400
    insert_device(ip, mac, name)
    return f"Dispositivo {name} con MAC {mac} añadido."

if __name__ == "__main__":
    # iniciamos la db
    init_db()
    all_devices = get_all_devices()
    for dev in all_devices:
        known_devices.add(dev)
    # Arrancar el bot de Telegram en un thread
    # threading.Thread(target=telegram_polling, daemon=True).start()
    # El servidor Flask escuchará en todas las interfaces de red local
    scan_thread = threading.Thread(target=background_scan, daemon=True)
    scan_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)  # Cambia debug=False en producción
