import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for char in texto:
        if char.isupper():
            resultado += chr((ord(char) + desplazamiento - 65) % 26 + 65)
        elif char.islower():
            resultado += chr((ord(char) + desplazamiento - 97) % 26 + 97)
        else:
            resultado += char
    return resultado

if __name__ == "__main__":
    # Verificamos que se pasen los argumentos correctos
    # sys.argv[0] es el nombre del script
    # sys.argv[1] es el texto
    # sys.argv[2] es el desplazamiento
    if len(sys.argv) != 3:
        print("Uso: python nombre_archivo.py \"texto a cifrar\" desplazamiento")
        sys.exit(1)

    texto_input = sys.argv[1]
    
    try:
        desplazamiento_input = int(sys.argv[2])
        resultado = cifrado_cesar(texto_input, desplazamiento_input)
        print(resultado)
    except ValueError:
        print("Error: El desplazamiento debe ser un número entero.")