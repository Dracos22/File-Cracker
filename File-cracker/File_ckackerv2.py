import os
import sys
import argparse
import zipfile
import rarfile
import PyPDF2
from tqdm import tqdm
import hashlib

# ========================== BANNER ========================== #
def banner():
    print("\033[1;36m")
    print("╔══════════════════════════════════════════════════════╗")
    print("║                    FILE CRACKER                      ║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║   > .rar crack      > .zip crack      > .pdf crack   ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("\033[0m")

# ====================== HASH VIEWER ======================== #
def show_hash(file):
    print("[*] SHA256 del archivo:")
    with open(file, "rb") as f:
        file_bytes = f.read()
        print("    ", hashlib.sha256(file_bytes).hexdigest())

# ====================== ZIP CRACKER ======================== #
def crack_zip(file, wordlist, verbose, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(file) as zf:
        for password in tqdm(wordlist, desc="[+] Cracking ZIP..."):
            try:
                if verbose:
                    print(f"[*] Trying: {password}")
                zf.extractall(path=output_dir, pwd=password.encode('utf-8'))
                print(f"\n[✓] Password Found: \033[1;32m{password}\033[0m")
                print(f"[✓] Extracted to: {output_dir}")
                return
            except:
                continue
    print("\n[!] Password not found.")

# ====================== RAR CRACKER ======================== #
def crack_rar(file, wordlist, verbose, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    rf = rarfile.RarFile(file)
    for password in tqdm(wordlist, desc="[+] Cracking RAR..."):
        try:
            if verbose:
                print(f"[*] Trying: {password}")
            rf.extractall(path=output_dir, pwd=password.encode())
            print(f"\n[✓] Password Found: \033[1;32m{password}\033[0m")
            print(f"[✓] Extracted to: {output_dir}")
            return
        except:
            continue
    print("\n[!] Password not found.")

# ====================== PDF CRACKER ======================== #
def crack_pdf(file, wordlist, verbose, output_dir):
    for password in tqdm(wordlist, desc="[+] Cracking PDF..."):
        try:
            with open(file, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if verbose:
                    print(f"[*] Trying: {password}")
                if reader.decrypt(password):
                    print(f"\n[✓] Password Found: \033[1;32m{password}\033[0m")
                    return
        except:
            continue
    print("\n[!] Password not found.")

# ========================= MAIN ============================ #
def main():
    banner()

    parser = argparse.ArgumentParser(description="File Cracker: Fuerza bruta para ZIP, RAR y PDF protegidos con contraseña.")
    parser.add_argument("-r", "--resource", required=True, help="Archivo objetivo (zip, rar, pdf).")
    parser.add_argument("-w", "--wordlist", required=True, help="Archivo de contraseñas.")
    parser.add_argument("-o", "--output", default="cracked_output", help="Ruta de extracción si se encuentra la contraseña.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar contraseñas probadas.")
    parser.add_argument("-H", "--hash", action="store_true", help="Mostrar hash SHA256 del archivo.")
    args = parser.parse_args()

    # Validación
    if not os.path.isfile(args.resource):
        print(f"[!] Archivo no encontrado: {args.resource}")
        sys.exit(1)
    if not os.path.isfile(args.wordlist):
        print(f"[!] Wordlist no encontrada: {args.wordlist}")
        sys.exit(1)

    if args.hash:
        show_hash(args.resource)

    with open(args.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = [line.strip() for line in f]

    if args.resource.endswith(".zip"):
        crack_zip(args.resource, passwords, args.verbose, args.output)
    elif args.resource.endswith(".rar"):
        crack_rar(args.resource, passwords, args.verbose, args.output)
    elif args.resource.endswith(".pdf"):
        crack_pdf(args.resource, passwords, args.verbose, args.output)
    else:
        print("[!] Tipo de archivo no soportado.")
        sys.exit(1)

if __name__ == "__main__":
    main()
