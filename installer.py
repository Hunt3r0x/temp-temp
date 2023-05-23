import os
import subprocess
import sys
from colorama import init, Fore

def golang():
    sys = os.uname().machine
    url = "https://go.dev/dl/go1.20.4.linux-amd64.tar.gz" if sys == "x86_64" else "https://golang.org/dl/go1.17.13.linux-386.tar.gz"
    subprocess.run(f"wget {url} -O golang.tar.gz", shell=True, check=True)
    subprocess.run("sudo tar -C /usr/local -xzf golang.tar.gz", shell=True, check=True)
    subprocess.run("echo 'export GOROOT=/usr/local/go' >> $HOME/.bashrc", shell=True, check=True)
    subprocess.run("echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc", shell=True, check=True)
    subprocess.run("echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> $HOME/.bashrc", shell=True, check=True)
    print(Fore.GREEN + "[+] Golang Installed!" + Fore.RESET)

def findomain():
    subprocess.run("wget https://github.com/Findomain/Findomain/releases/download/8.2.1/findomain-linux.zip -O findomain-linux.zip", shell=True, check=True)
    subprocess.run("unzip findomain-linux.zip", shell=True, check=True)
    if os.path.isfile("./findomain"):
        subprocess.run("sudo mv findomain /usr/local/bin/", shell=True, check=True)
        print(Fore.GREEN + "[+] Findomain Installed!" + Fore.RESET)
    else:
        print(Fore.YELLOW + "[!] Install Findomain manually: https://github.com/Findomain/Findomain/blob/master/docs/INSTALLATION.md" + Fore.RESET)

def subfinder():
    subprocess.run("go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest", shell=True, check=True)
    print(Fore.GREEN + "[+] Subfinder Installed!" + Fore.RESET)

def amass():
    subprocess.run("go install -v github.com/owasp-amass/amass/v3/...@master", shell=True, check=True)
    print(Fore.GREEN + "[+] Amass Installed!" + Fore.RESET)

def assetfinder():
    subprocess.run("go install -v github.com/tomnomnom/assetfinder@latest", shell=True, check=True)
    print(Fore.GREEN + "[+] Assetfinder Installed!" + Fore.RESET)

def chaos_client():
    subprocess.run("go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest", shell=True, check=True)
    print(Fore.GREEN + "[+] chaos-client Installed!" + Fore.RESET)

def anew():
    subprocess.run("go install -v github.com/tomnomnom/anew@latest", shell=True, check=True)
    print(Fore.GREEN + "[+] Anew Installed!" + Fore.RESET)

def install_dependencies():
    dependencies = [
        ("go", golang),
        ("findomain", findomain),
        ("subfinder", subfinder),
        ("amass", amass),
        ("assetfinder", assetfinder),
        ("chaos", chaos_client),
        ("anew", anew)
    ]

    for dependency, installer in dependencies:
        try:
            subprocess.run(f"hash {dependency}", shell=True, check=True)
            print(Fore.YELLOW + f"[!] {dependency.capitalize()} is already installed." + Fore.RESET)
        except subprocess.CalledProcessError:
            print(Fore.GREEN + f"[+] Installing {dependency.capitalize()}!" + Fore.RESET)
            installer()


def print_banner():
    init()  # Initialize Colorama

    banner = r'''
           █████████ ████     ███ ███     ███ ███       ███
           ███       ██ ███   ███ ███     ███ ██ ███   ████
 █████ ███ ███       ███ ███  ███ ███     ███ ███ ███ █ ███
      ███  ███████   ███  ███ ███ ███     ███ ███  ███  ███
    ███    ███       ███   ██ ███ ███     ███ ███   ██  ███
   ███     ███       ███    ██ ██ ███     ███ ███       ███
 █████████ █████████ ███      ███   ██████    ███       ███Installer
    '''

    print(Fore.MAGENTA + banner + Fore.RESET)
    print(Fore.CYAN + "  H1NTR0X01 @71ntr" + Fore.RESET + "\n")
    
    try:
        install_dependencies()
        print(Fore.BLUE + "Installation completed!" + Fore.RESET)
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram interrupted. Exiting..." + Fore.RESET)
        sys.exit(0)

print_banner()
