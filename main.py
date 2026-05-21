import win32gui
import win32con
import win32api
import time
import threading
import os
import requests
import urllib.parse
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Load environment variables from .env file
load_dotenv()

# Activate color system for Windows
init(autoreset=True)

# --- WHATSAPP SETTINGS (Fetched from .env) ---
YOUR_PHONE_NUMBER = os.getenv("PHONE_NUMBER") 
API_KEY = os.getenv("CALLMEBOT_API_KEY")

# --- MACRO SETTINGS ---
IN_LINE_VALUE = 22.5       
WALKING_VALUE = 1.8        
WALKING_BACK_VALUE = 19.5  
LOOP_VALUE = 9             
LINE_VALUE = 8             

# Key Codes (Virtual Key Codes)
VK_W = 0x57
VK_A = 0x41
VK_S = 0x53
VK_D = 0x44
VK_Z = 0x5A
VK_SPACE = 0x20

# Global States
is_running = False
stop_requested = False
macro_thread = None

def send_whatsapp_notification(message):
    """Sends a silent WhatsApp message in the background via CallMeBot."""
    if not YOUR_PHONE_NUMBER or not API_KEY:
        print(Fore.RED + "[WARNING] WhatsApp credentials missing in .env file! Message not sent.")
        return
    
    # Converts spaces and special characters in the message to URL format
    encoded_message = urllib.parse.quote(message)
    
    url = f"https://api.callmebot.com/whatsapp.php?phone={YOUR_PHONE_NUMBER}&text={encoded_message}&apikey={API_KEY}"
    
    try:
        requests.get(url, timeout=5)
    except Exception:
        pass # Prevent macro from crashing if internet disconnects

def get_minecraft_hwnd():
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "Lunar" in title or "Minecraft" in title:
                hwnds.append(hwnd)
        return True
    
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        return hwnds[0]
    return 0

def send_key_down(hwnd, key):
    scan_code = win32api.MapVirtualKey(key, 0)
    lparam = 0x00000001 | (scan_code << 16)
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, key, lparam)

def send_key_up(hwnd, key):
    scan_code = win32api.MapVirtualKey(key, 0)
    lparam = 0xC0000001 | (scan_code << 16)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, key, lparam)

def hold_key(hwnd, key, duration):
    """Sends continuous key press signals for the duration, similar to Windows."""
    if stop_requested: return
    start_time = time.time()
    
    while time.time() - start_time < duration:
        if stop_requested: break
        send_key_down(hwnd, key)
        time.sleep(0.05) 
        
    send_key_up(hwnd, key)
    time.sleep(0.1)

def multiple_hold_key(hwnd, keys, duration):
    """Sends repeated signals for multiple keys simultaneously."""
    if stop_requested: return
    start_time = time.time()
    
    while time.time() - start_time < duration:
        if stop_requested: break
        for key in keys:
            send_key_down(hwnd, key)
        time.sleep(0.05)
        
    for key in keys:
        send_key_up(hwnd, key)
    time.sleep(0.1)

def release_all_keys(hwnd):
    keys = [VK_W, VK_A, VK_S, VK_D, VK_Z, VK_SPACE]
    for key in keys:
        send_key_up(hwnd, key)
        time.sleep(0.02)

def print_banner():
    """Clears the console and prints a stylized banner."""
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('title Hypixel Background Macro')
    print(Fore.CYAN + Style.BRIGHT + "=========================================")
    print(Fore.MAGENTA + Style.BRIGHT + "  HYPIXEL MACRO v11.0 (WhatsApp Edition)")
    print(Fore.CYAN + Style.BRIGHT + "=========================================")
    print(Fore.YELLOW + Style.BRIGHT + " Commands:")
    print(Fore.GREEN + "   play  " + Fore.WHITE + "-> Starts the macro")
    print(Fore.RED + "   stop  " + Fore.WHITE + "-> Stops the macro")
    print(Fore.LIGHTBLACK_EX + "   exit  " + Fore.WHITE + "-> Closes the program")
    print(Fore.CYAN + Style.BRIGHT + "=========================================\n")

def macro_loop():
    global is_running, stop_requested
    hwnd = get_minecraft_hwnd()
    
    if hwnd == 0:
        print(Fore.RED + Style.BRIGHT + "\n[ERROR] Minecraft/Lunar not found! Open the game and then type 'play'.")
        is_running = False
        return

    print(Fore.GREEN + Style.BRIGHT + f"\n[SUCCESS] Minecraft found (HWND: {hwnd}). Entering the farm...")
    send_whatsapp_notification("🚀 Macro Started!\nBoss, I'm heading down to the fields, letting you know.")

    for loop_idx in range(LOOP_VALUE):
        if stop_requested: break
        print(Fore.MAGENTA + f"\n--- Loop {loop_idx + 1} / {LOOP_VALUE} Started ---")
        
        for i in range(1, LINE_VALUE + 1):
            if stop_requested: break
            print(Fore.CYAN + f"[*] Row: {i} processing...")
            
            # STEP 1: Move Right to Left
            multiple_hold_key(hwnd, [VK_Z, VK_W, VK_A], IN_LINE_VALUE) 
            if stop_requested: break
            
            # STEP 2: Row Transition (First W+Space simultaneously for a bit, then just W)
            multiple_hold_key(hwnd, [VK_SPACE, VK_W], 0.8)  
            hold_key(hwnd, VK_W, WALKING_VALUE)             
            time.sleep(0.5)
            
            # STEP 3: Move Left to Right
            multiple_hold_key(hwnd, [VK_Z, VK_W, VK_D], IN_LINE_VALUE) 
            if stop_requested: break
            
            # STEP 4: Next Row Transition Check
            if i != LINE_VALUE:
                # Requested W+Space logic added here as well
                multiple_hold_key(hwnd, [VK_SPACE, VK_W], 0.8)
                hold_key(hwnd, VK_W, WALKING_VALUE)
                time.sleep(0.5)
            else:
                # Return from the last row back to the start
                print(Fore.YELLOW + Style.BRIGHT + "Returning...")
                time.sleep(0.5)
                hold_key(hwnd, VK_A, 0.35)
                multiple_hold_key(hwnd, [VK_SPACE, VK_S], 0.8)
                hold_key(hwnd, VK_S, WALKING_BACK_VALUE)
                hold_key(hwnd, VK_D, 0.6)

    release_all_keys(hwnd)
    is_running = False
    
    if stop_requested:
        print(Fore.YELLOW + Style.BRIGHT + "\n[INFO] Macro stopped manually.")
        send_whatsapp_notification("🛑 Macro Stopped!\nYou terminated the process manually.")
    else:
        print(Fore.GREEN + Style.BRIGHT + "\n[INFO] Macro successfully completed its task. The whole farm is done!")
        send_whatsapp_notification("✅ Task Completed!\nFinished the whole farm, awaiting your next order, boss.")

def main():
    global is_running, stop_requested, macro_thread
    print_banner()

    while True:
        cmd = input(Fore.WHITE + Style.BRIGHT + "Command > " + Fore.RESET).strip().lower()

        if cmd == "play":
            if not is_running:
                is_running = True
                stop_requested = False
                macro_thread = threading.Thread(target=macro_loop, daemon=True)
                macro_thread.start()
            else:
                print(Fore.YELLOW + "Macro is already running ffs, chill!")
                
        elif cmd == "stop":
            if is_running:
                print(Fore.RED + "Stopping... Clearing keys...")
                stop_requested = True
                hwnd = get_minecraft_hwnd()
                if hwnd != 0: release_all_keys(hwnd)
            else:
                print(Fore.YELLOW + "Macro is already not running.")
                
        elif cmd in ["exit", "quit"]:
            stop_requested = True
            hwnd = get_minecraft_hwnd()
            if hwnd != 0: release_all_keys(hwnd)
            print(Fore.CYAN + "Peace out bro, exiting...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Invalid command! Please type 'play', 'stop' or 'exit'.")

if __name__ == "__main__":
    main()