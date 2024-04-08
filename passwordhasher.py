from passlib.hash import mysql323, mysql41, mssql2000, mssql2005, postgres_md5, oracle10, oracle11
import binascii
import hashlib
import pyfiglet
import time
import os

# ANSI escape color codes
g = "\033[92m"  # green color code
r = "\033[91m"  # red color code
y = "\033[93m"  # yellow color code
rc = "\033[0m"  # Reset Color Code

banner = pyfiglet.figlet_format("HashJet")

# Apply ANSI escape codes to the banner text
colored_banner = g + banner + rc

# Print the colored banner
print(colored_banner)
print(f"{y}[*] Password Hash Cracker & MAC Spoofer{rc}")
print(f"{y}[*] By Roshan Bhatia. IG/@2kwattz{rc}")
time.sleep(1)
print(f"\n[*] Press 1 to generate Password Hash {rc}")
print(f"[*] Press 2 to crack Password Hash {rc}")
print(f"[*] Press 3 to generate hashes for SQL Server {rc}")
print(f"[*] Press 4 to spoof your Mac Address (For Linux Users Only!) {rc}")

try:
    user_response = int(input())
except ValueError:
    print(f"{r}[*] Please Enter A Valid Number")

if user_response == 1:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f" {g} [*] Enter Your Password To Generate Hash {rc} \n")
    print("We Ain't Gonna Store Your Password So Chill\n")
    user_password = input()
    time.sleep(1)
    
    # Default Encoding
    utf_password = user_password.encode("UTF-8")
    base64_password = binascii.b2a_base64(utf_password)
    hex_password = binascii.b2a_hex(utf_password)

    print(f"{g}[*] Performing Default Hashing{rc}\nBase64 Password : {base64_password} \nHEX Password {hex_password}")
    time.sleep(1)
    hashing_algorithms = ['md5','sha1','sha224','sha3_224','sha256','sha3_256','sha512','sha3_512']
    for hashing_algorithm in hashing_algorithms:
        password_hash = hashlib.new(hashing_algorithm,utf_password).hexdigest()
        print(f" Hashing Algorithm : {hashing_algorithm} Password Hash : {password_hash} ")

elif user_response == 3:

    # SQL Hacking functions
    pass

