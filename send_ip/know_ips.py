#python3 -m pip install requests

import socket
import requests

def get_internal_ip():
    try:
        # Conecta a un destino ficticio solo para que el SO elija la interfaz adecuada
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception as e:
        return f"Error obteniendo IP interna: {e}"

def get_external_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip")
    except Exception as e:
        return f"Error obteniendo IP externa: {e}"

if __name__ == "__main__":
    print("IP interna :", get_internal_ip())
    print("IP externa :", get_external_ip())