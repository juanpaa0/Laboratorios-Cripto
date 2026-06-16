import requests
import time

start_time = time.time()
for i in range(1, 100):
    url = f"http://localhost:3000/api/users?id={i}"
    respuesta = requests.get(url)
    if "admin" in respuesta.text:
        print(f"Encontrado! ID: {i} -> {respuesta.text}")
        break
print(f"Tiempo demorado: {time.time() - start_time} segundos")