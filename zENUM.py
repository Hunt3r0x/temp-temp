import argparse
import json
import os
import subprocess
import sys
import time

def print_banner():
    banner = r'''
           █████████ ████     ███ ███     ███ ███       ███
           ███       ██ ███   ███ ███     ███ ██ ███   ████
 █████ ███ ███       ███ ███  ███ ███     ███ ███ ███ █ ███
      ███  ███████   ███  ███ ███ ███     ███ ███  ███  ███
    ███    ███       ███   ██ ███ ███     ███ ███   ██  ███
   ███     ███       ███    ██ ██ ███     ███ ███       ███
 █████████ █████████ ███      ███   ██████    ███       ███Runner v0.1
    '''
    print(banner)
    print("BY H1NTR0X01 @71ntr\n")
    print("Starting Enumerating && Monitoring!")
    
print_banner()

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output.decode().strip()}")
        return ""

def get_subdomains_wayback(domain):
    print(f"[*] Running WayBackMachine for {domain}")
    command = f'curl -sk "http://web.archive.org/cdx/search/cdx?url=*.{domain}&output=txt&fl=original&collapse=urlkey&page=" | awk -F/ \'{{gsub(/:.*/, "", $3); print $3}}\' >> output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_crt(domain):
    print(f"[*] Running crt.sh for {domain}")
    command = f'curl -sk "https://crt.sh/?q=%.{domain}&output=json" | tr \',\' \'\\n\' | awk -F\'"\' \'/name_value/ {{gsub(/\\*\\./, "", $4); gsub(/\\\\n/, "\\n",$4);print $4}}\' >> output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_bufferover(domain):
    print(f"[*] Running BufferOver for {domain}")
    command = f'curl -s "https://dns.bufferover.run/dns?q=.{domain}" | grep {domain} | awk -F, \'{{gsub("\\"\\"", "", $2); print $2}}\' >> output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_findomain(domain):
    print(f"[*] Running Findomain for {domain}")
    command = f'findomain --target {domain} --unique-output output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_subfinder(domain):
    print(f"[*] Running SubFinder for {domain}")
    command = f'subfinder -all -silent -d {domain} >> output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_amass(domain):
    print(f"[*] Running Amass for {domain}")
    command = f'amass enum -passive -norecursive -noalts -d {domain} >> output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_assetfinder(domain):
    print(f"[*] Running AssetFinder for {domain}")
    command = f'assetfinder --subs-only {domain} >> output/{domain}/subdomains.txt'
    run_command(command)

def get_subdomains_chaos(domain):
    print(f"[*] Running chaos for {domain}")
    command = f'chaos -d -silent -key QcKOBtkZG5xVSHIWegOY5IzGqA2i3YNUJ5IrsBlaMA3ZwBRfdmza01S8tOEcV5JR {domain} >> output/{domain}/subdomains.txt'
    run_command(command)

def compare_results(domain, previous_file):
    current_file = f'output/{domain}/subdomains.txt'

    sorted_current_file = f'output/{domain}/subdomains_sorted.txt'
    sorted_previous_file = f'output/{domain}/subdomains_previous_sorted.txt'

    # Sort the current and previous files
    run_command(f"sort -u {current_file} > {sorted_current_file}")
    run_command(f"sort -u {previous_file} > {sorted_previous_file}")

    # Compare the sorted files
    command = f"comm -13 {sorted_previous_file} {sorted_current_file} >> output/{domain}/diff.txt"
    run_command(command)

    with open(f'output/{domain}/diff.txt') as diff_file:
        diff_output = diff_file.read().strip()

    if diff_output:
        print(f"[*] New subdomains found for {domain}:")
        print(diff_output)
        save_new_subdomains(diff_output, current_file)
        send_notification(f"New subdomains found for {domain}:\n{diff_output}")
        os.replace(current_file, previous_file)
    else:
        os.remove(current_file)
        print("[*] No new subdomains found.")

    # Clean up the sorted files
    os.remove(sorted_current_file)
    os.remove(sorted_previous_file)

def save_new_subdomains(new_subdomains, current_file):
    with open(current_file, "a") as file:
        file.write(new_subdomains)

def send_notification(message):
    with open("config.json") as config_file:
        config = json.load(config_file)
        discord_webhook_url = config["discord_webhook_url"]
        telegram_token = config["telegram_token"]
        telegram_chat_id = config["telegram_chat_id"]

        if discord_webhook_url:
            send_discord_notification(discord_webhook_url, message)

        if telegram_token and telegram_chat_id:
            send_telegram_notification(telegram_token, telegram_chat_id, message)

def send_discord_notification(webhook_url, message):
    command = f'curl -X POST -H "Content-Type: application/json" -d \'{{"content": "{message}"}}\' {webhook_url}'
    run_command(command)

def send_telegram_notification(token, chat_id, message):
    command = f'curl -X POST -H "Content-Type: application/json" -d \'{{"chat_id": "{chat_id}", "text": "{message}"}}\' https://api.telegram.org/bot{token}/sendMessage'
    run_command(command)

def main(domain, sleep_duration, run_continuously):
    if not domain:
        print("Please provide a target domain using the -d/--domain argument.")
        return

    print(f"[*] Running subdomain enumeration for {domain}")

    if not os.path.exists(f"output/{domain}"):
        os.makedirs(f"output/{domain}")

    previous_file = f'output/{domain}/subdomains.txt'

    try:
        while True:
            get_subdomains_wayback(domain)
            get_subdomains_crt(domain)
            get_subdomains_bufferover(domain)
            get_subdomains_chaos(domain)
            get_subdomains_subfinder(domain)
            get_subdomains_amass(domain)
            get_subdomains_assetfinder(domain)
            # get_subdomains_findomain(domain)
            compare_results(domain, previous_file)

            if not run_continuously:
                break

            print(f"[*] Sleeping for {sleep_duration} seconds")
            time.sleep(sleep_duration)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)


def parse_arguments():
    parser = argparse.ArgumentParser(description="zENUM subdomain enumeration and monitoring tool")
    parser.add_argument("-d", "--domain", help="The target domain")
    parser.add_argument("-s", "--sleep", type=int, default=300, help="Sleep duration between scans in seconds")
    parser.add_argument("-c", "--continuous", action="store_true", help="Run continuously without pauses")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    sleep_duration = args.sleep
    continuous_run = args.continuous

    main(args.domain, sleep_duration, continuous_run)
