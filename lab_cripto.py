from Crypto.Cipher import DES, DES3, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii

def ajustar_clave_o_iv(dato_ingresado, tamano_requerido):
    
    dato_bytes = dato_ingresado.encode('utf-8')
    
    if len(dato_bytes) < tamano_requerido:
        bytes_faltantes = tamano_requerido - len(dato_bytes)
        dato_final = dato_bytes + get_random_bytes(bytes_faltantes)
    elif len(dato_bytes) > tamano_requerido:
        dato_final = dato_bytes[:tamano_requerido]
    else:
        dato_final = dato_bytes
        
    return dato_final

def procesar_algoritmo(nombre, modulo, texto, clave_final, iv_final, block_size):
    print(f"\nEjecutando {nombre} ")
    print(f"Clave final utilizada (hex): {binascii.hexlify(clave_final).decode()}")
    print(f"IV final utilizado (hex): {binascii.hexlify(iv_final).decode()}")
    
    # Cifrado
    cifrador = modulo.new(clave_final, modulo.MODE_CBC, iv_final)
    texto_padded = pad(texto.encode('utf-8'), block_size)
    texto_cifrado = cifrador.encrypt(texto_padded)
    print(f"Texto cifrado (hex): {binascii.hexlify(texto_cifrado).decode()}")
    
    # Descifrado
    descifrador = modulo.new(clave_final, modulo.MODE_CBC, iv_final)
    texto_descifrado_padded = descifrador.decrypt(texto_cifrado)
    texto_descifrado = unpad(texto_descifrado_padded, block_size).decode('utf-8')
    print(f"Texto descifrado: {texto_descifrado}")

if __name__ == "__main__":
    print("Laboratorio Cifrado Simetrico")
    
    texto_original = input("Ingrese el texto a cifrar: ")
    
    # DES
    key_des_input = input("\nIngrese la Key para DES: ")
    iv_des_input = input("Ingrese el IV para DES: ")
    key_des = ajustar_clave_o_iv(key_des_input, 8)
    iv_des = ajustar_clave_o_iv(iv_des_input, 8)
    
    # 3DES
    key_3des_input = input("\nIngrese la Key para 3DES: ")
    iv_3des_input = input("Ingrese el IV para 3DES: ")
    key_3des = ajustar_clave_o_iv(key_3des_input, 24)
    iv_3des = ajustar_clave_o_iv(iv_3des_input, 8)
    
    # AES-256
    key_aes_input = input("\nIngrese la Key para AES-256: ")
    iv_aes_input = input("Ingrese el IV para AES-256: ")
    key_aes = ajustar_clave_o_iv(key_aes_input, 32)
    iv_aes = ajustar_clave_o_iv(iv_aes_input, 16)
    
    procesar_algoritmo("DES", DES, texto_original, key_des, iv_des, DES.block_size)
    procesar_algoritmo("3DES", DES3, texto_original, key_3des, iv_3des, DES3.block_size)
    procesar_algoritmo("AES-256", AES, texto_original, key_aes, iv_aes, AES.block_size)