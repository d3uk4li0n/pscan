#!/usr/bin/python3

import os
import socket
import argparse
from scapy.all import *
from colorama import Fore

## function for syn scan
## TODO add specify source ip
def syn_scan(ip, port, timeout=5):
    pkt = IP(dst=ip)/TCP(dport=port, flags="S")# forged syn packet
    answer = sr1(pkt, timeout=timeout)
    if answer.getlayer(TCP).flags == "SA":
        print(f"port {port} is open")
    if answer.getlayer(TCP).flags == "R":
        print(f"port {port} is closed")

def udp_scan(ip, port, count=1):
    try:
        pkt = send(IP(dst=ip)/TCP(dport=port), count=count)
    except ConnectionResetError:
        print(f"port {port} closed or filtered")
        return 
    print(f"port {port} open")

def ping_host(ip, count=1):
    rsp = os.system(f"ping -c {count} {ip}")
    if rsp == 0:
        print(f"{ip} is up")
    else:
        print(f"{ip} is down")

def scan(ip, port=80, timeout=10):
    hname = get_domain_name(ip)
    if not hname:
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    if s.connect_ex((hname, port)):
        print(f"port: {port} is closed")
    else:
        print("port is open")
        #print(f"unclear response from port {port}")
    s.close()

def get_domain_name(ip):
    try:
        hname = socket.gethostbyaddr(ip)[0]
        return hname
    except socket.error:
        print("Error: could not obtain hostname")
        return ""

if __name__ == "__main__":
    stype = input(f"{Fore.BLUE}[+] Specify scan type: UDP (U), syn (SS), connect scan(S), ping host(P): ")
    if(stype == "P"):
        pcount = int(input(f"{Fore.BLUE}[+] (Optional) specify count (default: 1): "))
    target = str(input(f"{Fore.BLUE}[+] Target IP: "))
    port = int(input(f"{Fore.BLUE}[+] Target port: "))
    timeout = int(input(f"{Fore.BLUE}[+] (Optional) timeout (default: 10): "))
    if(stype == "U"):
        udp_scan(target, port, timeout)
    elif(stype == "SS"):
        syn_scan(target, port, timeout)
    elif(stype == "S"):
        scan(target, port, timeout)
    elif(stype == "P"):
        ping_host(target, pcount)
    else:
        print(f"{Fore.RED}[-] No option selected, exiting...")
        exit()
    '''
    parser = argparse.ArgumentParser(prog="banner grabber", description="Your favorite python port scanner",
                                     epilog="python3 bangrab.py [port] [timeout]")
    parser.add_argument("-t", "--target", help="ip or hostname of the target")
    parser.add_argument("-p", "--port", required=False, help="Select port number (default 80)")
    parser.add_argument("-to", "--timeout", required=False, help="Set timeout (default 10 seconds)")
    parser.add_argument("-r", "--range", nargs=2, default=[i for i in range(21, 81)], required=False, help="Specify range of ports like 21-80")

    parser.print_help()
    args = parser.parse_args()
    '''
    
