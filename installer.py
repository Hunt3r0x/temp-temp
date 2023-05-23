import os
import subprocess

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def golang():
    sys = os.uname().machine
    url = "https://go.dev/dl/go1.20.4.linux-amd64.tar.gz" if sys == "x86_64" else "https://golang.org/dl/go1.17.13.linux-386.tar.gz"
    subprocess.run(f"wget {url} -O golang.tar.gz", shell=True, check=True)
    subprocess.run("sudo tar -C /usr/local -xzf golang.tar.gz", shell=True, check=True)
    subprocess.run("echo 'export GOROOT=/usr/local/go' >> $HOME/.bashrc", shell=True, check=True)
    subprocess.run("echo 'export GOPATH=$HOME/go' >> $HOME/.bashrc", shell=True, check=True)
    subprocess.run("echo 'export PATH=$PATH:$GOROOT/bin:$GOPATH/bin' >> $HOME/.bashrc", shell=True, check=True)
    print_colored("[+] Golang Installed!", "32")

def findomain():
    subprocess.run("wget https://github.com/Findomain/Findomain/releases/download/8.2.1/findomain-linux.zip -O findomain-linux.zip", shell=True, check=True)
    subprocess.run("unzip findomain-linux.zip", shell=True, check=True)
    if os.path.isfile("./findomain"):
        subprocess.run("sudo mv findomain /usr/local/bin/", shell=True, check=True)
        print_colored("[+] Findomain Installed!", "32")
    else:
        print_colored("[!] Install Findomain manually: https://github.com/Findomain/Findomain/blob/master/docs/INSTALLATION.md", "31")

def subfinder():
    subprocess.run("go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest", shell=True, check=True)
    print_colored("[+] Subfinder Installed!", "32")

def amass():
    subprocess.run("go install -v github.com/owasp-amass/amass/v3/...@master", shell=True, check=True)
    print_colored("[+] Amass Installed!", "32")

def assetfinder():
    subprocess.run("go install -v github.com/tomnomnom/assetfinder@latest", shell=True, check=True)
    print_colored("[+] Assetfinder Installed!", "32")

def chaos_client():
    subprocess.run("go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest", shell=True, check=True)
    print_colored("[+] chaos-client Installed!", "32")

# def httprobe():
#     subprocess.run("go install -v github.com/tomnomnom/httprobe@latest", shell=True, check=True)
#     print_colored("[+] Httprobe Installed!", "32")

# def parallel():
#     subprocess.run("sudo apt-get install parallel -y", shell=True, check=True)
#     print_colored("[+] Parallel Installed!", "32")

def anew():
    subprocess.run("go install -v github.com/tomnomnom/anew@latest", shell=True, check=True)
    print_colored("[+] Anew Installed!", "32")


def install_dependencies():
    dependencies = [
        ("go", golang),
        ("findomain", findomain),
        ("subfinder", subfinder),
        ("amass", amass),
        ("assetfinder", assetfinder),
        ("chaos", chaos_client),
        # ("httprobe", httprobe),
        # ("parallel", parallel),
        ("anew", anew)
    ]

    for dependency, installer in dependencies:
        try:
            subprocess.run(f"hash {dependency}", shell=True, check=True)
            print_colored(f"[!] {dependency.capitalize()} is already installed.", "33")
        except subprocess.CalledProcessError:
            print_colored(f"[+] Installing {dependency.capitalize()}!", "32")
            installer()

def print_banner():
    banner = r'''
           █████████ ████     ███ ███     ███ ███       ███
           ███       ██ ███   ███ ███     ███ ██ ███   ████
 █████ ███ ███       ███ ███  ███ ███     ███ ███ ███ █ ███
      ███  ███████   ███  ███ ███ ███     ███ ███  ███  ███
    ███    ███       ███   ██ ███ ███     ███ ███   ██  ███
   ███     ███       ███    ██ ██ ███     ███ ███       ███
 █████████ █████████ ███      ███   ██████    ███       ███Installer
    '''
    print_colored(banner, "95")
    print_colored("  H1NTR0X01 @71ntr", "96")
    print_colored("", "34")
    install_dependencies()
    print_colored("Installation completed!", "34")
print_banner()
