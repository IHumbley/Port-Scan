"""
Programmer: Matin
Github: https://github.com/MrHumbley
"""

import re
from os.path import isfile
import nmap  # pip install python-nmap
import colorama
# from colorama import just_fix_windows_console
# just_fix_windows_console()

# nmap_search_path=[r"C:\Program Files (x86)\Nmap\nmap.exe", ]
nm = nmap.PortScanner()


def ip_lists(path):
    ipv4_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ipv4_addresses = []
    if isfile(path):
        with open(file, "r", encoding="UTF-8") as fi:
            reads = fi.read()
            ipv4_addresses = re.findall(ipv4_regex, reads)
    return ipv4_addresses


def check_rdp(ip, p):
    print(colorama.Fore.CYAN + f"\n\n[Info] Scanning {ip} and ports range {p} start")
    nm.scan(hosts=f'{ip}', ports=f'{p}')
    out = ""
    print(nm.all_hosts())
    for host in nm.all_hosts():
        print(colorama.Fore.CYAN + f"[Info] Start cheking {host}")
        if nm[host].state() == 'up':
            for port in nm[host]['tcp']:
                if nm[host]['tcp'][port]['state'] == 'open':
                    out = f'{host}:{port}'
                    print(colorama.Fore.GREEN + f'[+] {host}:{port} is open')
                    return out  # break all
                else:
                    print(colorama.Fore.RED + f"[-] {host} with port {port} is not open")
            return out
        else:
            print(colorama.Fore.RED + f"[-] {host} is down")
            return out
    print(colorama.Fore.RED + f"[-] {ip} is not find")
    return out


if __name__ == '__main__':
    print(colorama.Fore.CYAN, end='')
    file = input(r"[Info] Enter IPs File Path (example: C://User/Desktop/IP_Range.txt): ")
    print(colorama.Fore.CYAN, end='')
    start_range = input(r"""
Tip:
    1) if u want scan port from N until M enter: N-M
    2) if you want scan port N and M and K and ..., enter: N, M, K,...    
[Info] Now Enter Your Ports Do You Want Scan: """)

    output = ""
    print(colorama.Fore.CYAN + "\n\n[Info] Making for true open ports file")
    f = open("true_hosts.txt", "w", encoding="UTF-8")
    ipl = ip_lists(file)

    if ipl:
        for i in ipl:
            check = check_rdp(i, start_range)
            if check:
                output += f"{check}\n"
                f.write(output)
        f.close()
        print(colorama.Fore.CYAN + "[Info] Done !")
    else:
        print(colorama.Fore.RED + "[-] The file is not any ipv4")
