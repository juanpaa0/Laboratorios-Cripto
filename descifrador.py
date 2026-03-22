import sys
from scapy.all import rdpcap, ICMP, IP

def extraer_mensaje_de_pcap(archivo_pcap):
    mensaje_extraido = ""
    try:
        # Cargamos los paquetes del archivo de captura
        paquetes = rdpcap(archivo_pcap)
        
        for pkt in paquetes:
            # Filtramos: Debe ser ICMP, de tipo Echo Request (8)
            if pkt.haslayer(ICMP) and pkt[ICMP].type == 8:
                if pkt.haslayer('Raw'):
                    # Extraemos el primer byte del payload (campo Data)
                    payload = pkt['Raw'].load
                    if payload:
                        # Convertimos el primer byte a carácter
                        char = chr(payload[0])
                        mensaje_extraido += char
        
        return mensaje_extraido
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        sys.exit(1)

def descifrar_y_puntuar(texto):
    posibilidades = []
    # Letras frecuentes en español/inglés para el sistema de puntos
    frecuentes = "eaosrn EAOSRN"
    
    for d in range(26):
        intento = ""
        for char in texto:
            if char.isupper():
                intento += chr((ord(char) - d - 65) % 26 + 65)
            elif char.islower():
                intento += chr((ord(char) - d - 97) % 26 + 97)
            else:
                intento += char
        
        # Calcular probabilidad (puntos por letras comunes y espacios)
        puntos = sum(1 for c in intento if c in frecuentes or c == ' ')
        posibilidades.append((d, intento, puntos))
    
    return posibilidades

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Uso: python3 extractor_y_descifrador.py "captura.pcap"')
        sys.exit(1)

    archivo = sys.argv[1]
    print(f"[*] Analizando captura: {archivo}...")
    
    texto_extraido = extraer_mensaje_de_pcap(archivo)
    
    if not texto_extraido:
        print("[-] No se encontraron datos exfiltrados en los paquetes ICMP.")
        sys.exit(1)

    print(f"[+] Texto crudo extraído de ICMP: {texto_extraido}")
    print("-" * 50)

    resultados = descifrar_y_puntuar(texto_extraido)
    mejor_opcion = max(resultados, key=lambda x: x[2])

    print(f"{'Shift':<6} | {'Traducción'}")
    for d, texto, p in resultados:
        if texto == mejor_opcion[1]:
            # Imprime en VERDE la opción más probable
            print(f"\033[92m[{d:02d}]    | {texto} (PROBABLE)\033[0m")
        else:
            print(f"[{d:02d}]    | {texto}")