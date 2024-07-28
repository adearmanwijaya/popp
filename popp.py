import requests
import json
from datetime import datetime, timedelta
import time
from colorama import init, Fore, Style
from urllib.parse import parse_qs, urlparse, unquote

init(autoreset=True)

# Define color variables
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT

headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://planet.popp.club',
    'Pragma': 'no-cache',
    'Referer': 'https://planet.popp.club/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'accept': 'application/json',
    'content-type': 'application/json;charset=utf-8',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows'
}

# Function to get the token bearer
def get_token(init_data):
    url = 'https://moon.popp.club/pass/login'
    data = json.dumps({"initData": init_data})
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] == '00':
            return response_json.get('data', {}).get('token')
        else:
            print(f"{RED}Error: {response_json.get('msg', 'Unknown error')}", flush=True)
            return None
    except (requests.RequestException, ValueError) as e:
        print(f"{RED}Error getting token: {e}", flush=True)
        return None

# Function to check data
def check_data(token):
    url = 'https://moon.popp.club/moon/asset'
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('data', {})
    except (requests.RequestException, ValueError) as e:
        print(f"{RED}Error checking data: {e}", flush=True)
        return {}

def check_ghalibie(token):
    url = 'https://moon.popp.club/moon/sign/in'
    headers['Authorization'] = token
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] == '00':
            print(f"{GREEN}Check-in: {response_json['msg']}", flush=True)
            return True
        elif response_json['code'] == '400' and response_json['msg'] == 'Checked in today.':
            print(f"{RED}Check-in: Already checked in today.", flush=True)
            return False
        else:
            print(f"{RED}Error: {response_json.get('msg', 'Unknown error')}", flush=True)
            return False
    except (requests.RequestException, ValueError) as e:
        print(f"{RED}Error checking ghalibie: {e}", flush=True)
        return None
    

def explore_planet(token, planet_id):
    url = f'https://moon.popp.club/moon/explorer?plantId={planet_id}'
    headers['Authorization'] = token
    try:
        print(f"\r{YELLOW}Planet ID: {planet_id} Exploring...", flush=True)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] == '00':
            reward = response_json.get('data', {})
            amount = reward.get('amount', 0)
            award = reward.get('award', 'Unknown')
            print(f"\r{GREEN}Planet ID: {planet_id} | Explored | Reward: {amount} {award}", flush=True)
        else:
            print(f"\r{RED}Error exploring planet {planet_id}: {response_json.get('msg', 'Unknown error')}", flush=True)
    except (requests.RequestException, ValueError) as e:
        print(f"\r{RED}Error exploring planet {planet_id}: {e}", flush=True)

def get_planets_ghalibie(token):
    url = 'https://moon.popp.club/moon/planets'
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] == '00':
            planets = response_json.get('data', [])
            if not planets:
                print(f"\r{RED}Planets: No planets found.", flush=True)
            else:
                print(f"\r{GREEN}Planets: You have {len(planets)} planets.", flush=True)
                for planet in planets:
                    planet_id = planet['id']
                    explore_planet(token, planet_id)
        else:
            print(f"\r{RED}Error: {response_json.get('msg', 'Unknown error')}", flush=True)
    except (requests.RequestException, ValueError) as e:
        print(f"\r{RED}Error getting planets: {e}", flush=True)


def claim_farming(token):
    url = 'https://moon.popp.club/moon/claim/farming'
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] == '00':
            print(f"{GREEN}Farming claimed successfully.", flush=True)
        else:
            print(f"{RED}Error claiming farming: {response_json.get('msg', 'Unknown error')}", flush=True)
    except (requests.RequestException, ValueError) as e:
        print(f"{RED}Error claiming farming: {e}", flush=True)

def start_farming(token):
    url = 'https://moon.popp.club/moon/farming'
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        # print(response_json)
        if response_json['code'] == '00':
            print(f"{GREEN}Farming started successfully.", flush=True)
        elif response_json['code'] == '400' and response_json['msg'] == 'Farming already!':
            print(f"{YELLOW}Farming already in progress.", flush=True)
        else:
            print(f"{RED}Error starting farming: {response_json.get('msg', 'Unknown error')}", flush=True)
    except (requests.RequestException, ValueError) as e:
        print(f"{RED}Error starting farming: {e}", flush=True)

def claim_farming_invite(ghalibie):
    url = 'https://moon.popp.club/moon/claim/invite'
    headers['Authorization'] = ghalibie
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if response_json['code'] == '00':
            print(f"{GREEN}Invite claimed successfully.", flush=True)
        else:
            print(f"{RED}Error claiming invite: {response_json.get('msg', 'Unknown error')}", flush=True)
    except (requests.RequestException, ValueError) as e:
        print(f"{RED}Error claiming invite: {e}", flush=True)

# Function to format time
def format_time(seconds):
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if hours > 0:
        parts.append(f"{hours} hours")
    if minutes > 0 or (hours > 0 and seconds > 0):
        parts.append(f"{minutes} minutes")
    if seconds > 0:
        parts.append(f"{seconds} seconds")
    return ' '.join(parts) if parts else "0 seconds"

# Function to format the farming time left
def format_farming_time_left(farming_time_left):
    total_seconds = int(farming_time_left.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hours {minutes} minutes {seconds} seconds"

def process_line(init_data, line, line_number):
    token = get_token(init_data)
    if not token:
        print(f"\r{RED}Skipping line {line_number} due to token error.", flush=True)
        return

    data = check_data(token)
    if not data:
        print(f"\r{RED}Skipping line {line_number} due to data error.", flush=True)
        return
    
    # Extract first_name from the query string
    query_params = parse_qs(line)
    user_info_str = query_params.get('user', [None])[0]
    
    if user_info_str:
        user_info = json.loads(unquote(user_info_str))
        first_name = user_info.get('first_name', 'Unknown')
    else:
        first_name = 'Unknown'
    
    # Format SD value to remove numbers after the first dot
    sd = int(data.get('sd', 0))
    probe = data.get('probe', 'N/A')
    formatted_time = format_time(data.get('time', 0))  # Renamed variable
    farming_end_time = datetime.fromtimestamp(data.get('farmingEndTime', 0) / 1000)
    now = datetime.now()
    farming_time_left = farming_end_time - now
    if farming_time_left.total_seconds() < 0:
        farming_time_left = timedelta(seconds=0)
    frozen_invite_sd = data.get('frozenInviteSd', 0) / 1000
    
    print(f"\r{CYAN}=== Akun ke {line_number} | {first_name} ===", flush=True)
    print(f"\r{GREEN}SD: {sd}", flush=True)
    print(f"\r{YELLOW}Probe: {probe}", flush=True)
    print(f"\r{YELLOW}Farming Time: {formatted_time}", flush=True)  # Updated print statement
    print(f"\r{CYAN}Farming SD: Claim in {format_farming_time_left(farming_time_left)}", flush=True)
    print(f"\r{CYAN}Farming Reff: {frozen_invite_sd:.3f}", flush=True)
    check_ghalibie(token)
    time.sleep(2)
    get_planets_ghalibie(token)
    
    if farming_time_left.total_seconds() <= 0:
        # print(f"\r{YELLOW}Farming can be claimed.", flush=True)
        claim_farming(token)
        time.sleep(2)
        start_farming(token)
    if frozen_invite_sd > 0:
        time.sleep(2)
        # print(f"\r{YELLOW}Invite can be claimed.", flush=True)
        claim_farming_invite(token)
# Main function
def main():
    print_welcome_message()
    while True:
        try:
            with open('query.txt', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError as e:
            print(f"\r{RED}Error reading file: {e}", flush=True)
            break
        
        for line_number, line in enumerate(lines, start=1):
            process_line(line.strip(), line.strip(), line_number)
        
        animated_loading(100)
def print_welcome_message():
    print(Fore.RED + Style.BRIGHT + "█▀▀ " + Fore.YELLOW + "█░█ " + Fore.RED + "▄▀█ " + Fore.YELLOW + "█░░ " + Fore.RED + "█ " + Fore.YELLOW + "█▄▄ " + Fore.RED + "█ " + Fore.YELLOW + "█▀▀")
    print(Fore.YELLOW + "█▄█ " + Fore.RED + "█▀█ " + Fore.YELLOW + "█▀█ " + Fore.RED + "█▄▄ " + Fore.YELLOW + "█ " + Fore.RED + "█▄█ " + Fore.YELLOW + "█ " + Fore.RED + "██▄")
    print(Fore.CYAN + Style.BRIGHT + "\nPopp Planet BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearmanwijaya/popp")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.YELLOW + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA / BINANCE ID 248613229")
    print(Fore.YELLOW + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu looping berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    

if __name__ == "__main__":
    main()