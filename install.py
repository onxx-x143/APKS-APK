import os
import subprocess
import webbrowser
import time
import sys
from colorama import init, Fore, Style
import pyfiglet
import subprocess

print("Opening GitHub...")
subprocess.run(["am", "start", "-a", "android.intent.action.VIEW", 
                "-d", "https://github.com/onxx-x143", "com.android.chrome"], 
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
               
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    banner = pyfiglet.figlet_format("ONXXEAHH", font="slant")
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.YELLOW + "=" * 61)
    print(Fore.MAGENTA + "          Őńxx APK Tool - Pro Level APK Manager".center(60))
    print(Fore.YELLOW + "=" * 61)
    print(Fore.GREEN + "GitHub: by Onxx-x143".center(60))
    print(Fore.YELLOW + "=" * 61 + "\n")
    
def run_command(cmd, desc):
    print(Fore.CYAN + f"Running: {desc}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(Fore.GREEN + "Success!" + Style.RESET_ALL)
            if result.stdout:
                print(result.stdout[:500])  # Limited output
        else:
            print(Fore.RED + f"Error: {result.stderr}")
    except Exception as e:
        print(Fore.RED + f"Failed: {str(e)}")

def convert_apks_to_apk():
    apks_path = input(Fore.WHITE + "Enter .apks file path: ").strip()
    if not os.path.exists(apks_path):
        print(Fore.RED + "File not found!")
        return
    output_apk = input(Fore.WHITE + "Enter output APK name (e.g. app.apk): ").strip()
    # For .apks to universal APK: rename to zip and extract universal.apk (simple way)
    # Better: use bundletool if from AAB, but for .apks assume user has it
    zip_path = apks_path.replace('.apks', '.zip')
    os.rename(apks_path, zip_path)
    print(Fore.YELLOW + "Extracting universal APK...")
    # Extract (requires unzip or Python zip)
    with open(os.devnull, 'w') as devnull:
        subprocess.call(['unzip', '-o', zip_path, 'universal.apk', '-d', os.path.dirname(apks_path)], stdout=devnull)
    extracted = os.path.join(os.path.dirname(apks_path), 'universal.apk')
    if os.path.exists(extracted):
        os.rename(extracted, output_apk)
        print(Fore.GREEN + f"Converted to {output_apk}")
    else:
        print(Fore.RED + "Extraction failed. Ensure unzip installed.")

def sign_apk():
    apk_path = input(Fore.WHITE + "Enter APK path to sign: ").strip()
    keystore = input(Fore.WHITE + "Enter keystore path (or press Enter for debug): ").strip() or "\~/.android/debug.keystore"
    alias = input(Fore.WHITE + "Key alias (default: androiddebugkey): ") or "androiddebugkey"
    storepass = input(Fore.WHITE + "Store password: ") or "android"
    keypass = input(Fore.WHITE + "Key password: ") or "android"
    signed_apk = apk_path.replace('.apk', '_signed.apk')
    cmd = f'apksigner sign --ks "{keystore}" --ks-key-alias {alias} --ks-pass pass:{storepass} --key-pass pass:{keypass} --out "{signed_apk}" "{apk_path}"'
    run_command(cmd, "APK Signing")

def move_apk():
    apk_path = input(Fore.WHITE + "Enter APK path: ").strip()
    dest_folder = input(Fore.WHITE + "Enter destination folder: ").strip()
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest = os.path.join(dest_folder, os.path.basename(apk_path))
    try:
        os.rename(apk_path, dest)
        print(Fore.GREEN + f"Moved to {dest}")
    except Exception as e:
        print(Fore.RED + f"Move failed: {e}")

def main():
      
    while True:
        show_banner()
        print(Fore.WHITE + "1. Convert APKS → APK")
        print(Fore.WHITE + "2. Sign APK")
        print(Fore.WHITE + "3. Move APK to any folder")
        print(Fore.WHITE + "0. Exit")
        choice = input(Fore.CYAN + "\nChoose option: ").strip()
        
        if choice == '1':
            convert_apks_to_apk()
        elif choice == '2':
            sign_apk()
        elif choice == '3':
            move_apk()
        elif choice == '0':
            print(Fore.GREEN + "Thank you for using Őńxx Tool! Goodbye.")
            break
        else:
            print(Fore.RED + "Invalid option!")
        
        input(Fore.YELLOW + "\nPress Enter to continue...")
        # Screen clear next loop mein ho jayega

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nExited by user.")
