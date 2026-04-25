#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
import socket
import ssl
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import base64
import hashlib
import json
import re
import datetime
import xml.etree.ElementTree as ET

# ─── THƯ VIỆN BÊN NGOÀI ───────────────────────────────────────────────────────
try:
    import requests
except ImportError:
    print("[-] Thiếu 'requests'. Cài: pip install requests")
    sys.exit(1)

try:
    import yt_dlp
except ImportError:
    print("[-] Thiếu 'yt-dlp'. Cài: pip install yt-dlp")
    sys.exit(1)

# Kích hoạt ANSI escape sequence trên Windows
if os.name == 'nt':
    os.system('color')

# ─── COLOR CODES (Giao diện Blood Dragon / Hacker) ────────────────────────────
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ─── UTILS & UI ───────────────────────────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(f"\n{Colors.YELLOW}[!] Nhấn Enter để trở về menu...{Colors.RESET}")

def display_banner():
    clear_screen()
    banner = f"""{Colors.RED}{Colors.BOLD}
    ██████╗ ██╗   ██╗ ██████╗    ███╗   ██╗██╗  ██╗ █████╗ ███╗   ██╗
    ██╔══██╗██║   ██║██╔════╝    ████╗  ██║██║  ██║██╔══██╗████╗  ██║
    ██║  ██║██║   ██║██║         ██╔██╗ ██║███████║███████║██╔██╗ ██║
    ██║  ██║██║   ██║██║         ██║╚██╗██║██╔══██║██╔══██║██║╚██╗██║
    ██████╔╝╚██████╔╝╚██████╗    ██║ ╚████║██║  ██║██║  ██║██║ ╚████║
    ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
         ____  _______     _______ _    _ ______ _____  ______
        |  _ \| ____\ \   / / ____| |  | |  ____|  __ \|  ____|
        | | | |  _|  \ \ / /|  _| | |  | | |__  | |__) | |__|
        | |_| | |___  \ V / | |___| |__| |  __| |  _  /|  __|
        |____/|_____|  \_/  |_____|\____/|_|    |_| \_\|_|
    {Colors.RESET}"""
    print(banner)
    print(f"{Colors.CYAN}\t\t   [ ĐỨC NHÂN - DEVELOPER ]{Colors.RESET}")
    print(f"{Colors.GREEN}\t\t   Ethical Hacking & Dev Tool v4.0{Colors.RESET}\n")

def main_menu():
    display_banner()
    print(f"{Colors.MAGENTA}╔════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.BOLD}{Colors.WHITE}                       MENU CHỨC NĂNG                       {Colors.RESET}{Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}╠════════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[1]{Colors.RESET} 🌐 Network Tools  (Ping, Port Scan, ARP, Info)          {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[2]{Colors.RESET} 📡 WiFi Scanner   (Phân tích mạng không dây chi tiết)   {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[3]{Colors.RESET} 🔬 Advanced Recon (Subdomain, HTTP, DNS, SSL)           {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[4]{Colors.RESET} 👤 OSINT Tools    (Tra cứu Username đa nền tảng)        {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[5]{Colors.RESET} 📥 Media Download (YouTube, TikTok, ...)                {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[6]{Colors.RESET} 🪓 Hacking Tools  (Router, Fuzzing, SQLi, Crack Hash)   {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[7]{Colors.RESET} 🔑 Crypto & IP    (Base64, Hash, GeoIP)                 {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.RED}[0]{Colors.RESET} ❌ Thoát hệ thống                                       {Colors.MAGENTA}║{Colors.RESET}")
    print(f"{Colors.MAGENTA}╚════════════════════════════════════════════════════════════╝{Colors.RESET}")
    choice = input(f"\n{Colors.GREEN}=> Nhập command:{Colors.RESET} ").strip()
    return choice

def print_separator(char='─', width=65, color=Colors.CYAN):
    print(f"{color}{char * width}{Colors.RESET}")

# ─── NETWORK TOOLS ────────────────────────────────────────────────────────────

def ping_host(ip):
    system = platform.system().lower()
    cmd = ["ping", "-n", "1", "-w", "1000", ip] if system == "windows" else ["ping", "-c", "1", "-W", "1", ip]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
        return result.returncode == 0
    except Exception:
        return False

def ping_sweep():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] QUÉT HOST TRONG MẠNG LAN (PING SWEEP){Colors.RESET}")
    subnet = input(f"{Colors.CYAN}Nhập 3 octet đầu của mạng (VD: 192.168.1): {Colors.RESET}").strip()
    if not subnet: return
    if not subnet.endswith('.'): subnet += '.'
    print(f"{Colors.YELLOW}[*] Đang quét dải {subnet}1-254...{Colors.RESET}\n")
    online_hosts = []
    ip_list = [f"{subnet}{i}" for i in range(1, 255)]
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(ping_host, ip): ip for ip in ip_list}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            if future.result():
                online_hosts.append(ip)
                print(f"{Colors.GREEN}[+] Online: {ip}{Colors.RESET}")
    print(f"\n{Colors.CYAN}[*] TỔNG KẾT: {len(online_hosts)} thiết bị đang online.{Colors.RESET}")

def grab_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            s.connect((ip, port))
            s.send(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = s.recv(1024).decode(errors='ignore').strip().split('\n')[0]
            return banner if banner else "Unknown Service"
    except Exception:
        return "Unknown Service"

def port_scanner():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] QUÉT CỔNG (PORT SCANNER & BANNER GRABBING){Colors.RESET}")
    target = input(f"{Colors.CYAN}Nhập IP/Domain mục tiêu: {Colors.RESET}").strip()
    if not target: return
    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 8080, 8443]
    print(f"{Colors.YELLOW}[*] Quét {len(ports)} cổng phổ biến trên '{target}'...{Colors.RESET}")
    open_ports = []

    def scan_and_grab(ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    banner = grab_banner(ip, port)
                    return port, banner
        except: pass
        return None

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_port = {executor.submit(scan_and_grab, target, p): p for p in ports}
        for future in as_completed(future_to_port):
            result = future.result()
            if result:
                port, banner = result
                open_ports.append(port)
                print(f"{Colors.GREEN}[+] Port {port:<5} | MỞ | {banner[:50]}{Colors.RESET}")
    if not open_ports:
        print(f"{Colors.RED}[-] Không tìm thấy cổng mở.{Colors.RESET}")

def arp_scanner():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] ARP SCANNER – PHÁT HIỆN THIẾT BỊ TRONG MẠNG LAN{Colors.RESET}")
    print(f"{Colors.RED}[!] Chỉ hoạt động trên mạng bạn sở hữu/có quyền kiểm tra.{Colors.RESET}\n")
    devices = []
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=10)
        for line in result.stdout.splitlines():
            ip_m   = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
            mac_m  = re.search(r'([0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2})', line)
            if ip_m and mac_m:
                ip  = ip_m.group(1)
                mac = mac_m.group(1).replace('-', ':').upper()
                if mac not in ('FF:FF:FF:FF:FF:FF',):
                    devices.append({'ip': ip, 'mac': mac})
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi ARP: {e}{Colors.RESET}"); return

    if not devices:
        print(f"{Colors.RED}[-] Bảng ARP trống. Hãy chạy Ping Sweep trước.{Colors.RESET}"); return

    print(f"{Colors.GREEN}[+] Phát hiện {len(devices)} thiết bị:{Colors.RESET}\n")
    print_separator()
    print(f"{Colors.BOLD}{'#':<4} {'IP Address':<18} {'MAC Address':<20} {'Hostname':<28} Vendor{Colors.RESET}")
    print_separator()

    for i, dev in enumerate(devices, 1):
        ip  = dev['ip']
        mac = dev['mac']
        try:    hostname = socket.gethostbyaddr(ip)[0]
        except: hostname = 'N/A'
        try:
            oui    = mac.replace(':', '')[:6]
            vr     = requests.get(f"https://api.macvendors.com/{oui}", timeout=2)
            vendor = vr.text.strip() if vr.status_code == 200 else 'Unknown'
        except: vendor = 'Unknown'
        print(f"{i:<4} {Colors.CYAN}{ip:<18}{Colors.RESET} {Colors.YELLOW}{mac:<20}{Colors.RESET} {hostname:<28} {vendor}")
        time.sleep(0.35)

    print_separator()
    print(f"{Colors.GREEN}[*] Tổng: {len(devices)} thiết bị.{Colors.RESET}")

def network_info():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] THÔNG TIN MẠNG MÁY TÍNH{Colors.RESET}\n")
    hostname = socket.gethostname()
    try:    local_ip = socket.gethostbyname(hostname)
    except: local_ip = 'N/A'
    try:    pub_ip = requests.get("https://api.ipify.org", timeout=5).text.strip()
    except: pub_ip = 'Không kết nối được'

    print(f"  {Colors.BOLD}Hostname{Colors.RESET}    : {Colors.CYAN}{hostname}{Colors.RESET}")
    print(f"  {Colors.BOLD}IP nội bộ{Colors.RESET}   : {Colors.CYAN}{local_ip}{Colors.RESET}")
    print(f"  {Colors.BOLD}IP công khai{Colors.RESET}: {Colors.RED}{pub_ip}{Colors.RESET}")
    print(f"\n  {Colors.YELLOW}CHI TIẾT INTERFACE:{Colors.RESET}")
    print_separator()
    system = platform.system().lower()
    try:
        if system == 'windows':
            r = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            for line in r.stdout.splitlines():
                for kw in ['IPv4', 'IPv6', 'Physical', 'Subnet', 'Default Gateway', 'DNS Server', 'Description']:
                    if kw in line and ':' in line:
                        k, _, v = line.strip().partition(':')
                        if v.strip():
                            print(f"  {Colors.CYAN}{k.strip():<35}{Colors.RESET}: {v.strip()}")
        else:
            r = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            for line in r.stdout.splitlines():
                if re.match(r'^\d+:', line) or 'inet ' in line or 'link/ether' in line:
                    print(f"  {line.strip()}")
    except Exception as e:
        print(f"  {Colors.RED}[-] Lỗi: {e}{Colors.RESET}")

def network_tools_menu():
    while True:
        clear_screen()
        print(f"{Colors.BLUE}╔══════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BLUE}║{Colors.BOLD}{Colors.WHITE}             🌐 NETWORK TOOLS               {Colors.RESET}{Colors.BLUE}║{Colors.RESET}")
        print(f"{Colors.BLUE}╠══════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.BLUE}║{Colors.RESET} {Colors.CYAN}[1]{Colors.RESET} Ping Sweep (Quét thiết bị online LAN)  {Colors.BLUE}║{Colors.RESET}")
        print(f"{Colors.BLUE}║{Colors.RESET} {Colors.CYAN}[2]{Colors.RESET} Port Scanner & Banner Grabbing         {Colors.BLUE}║{Colors.RESET}")
        print(f"{Colors.BLUE}║{Colors.RESET} {Colors.CYAN}[3]{Colors.RESET} ARP Scanner (MAC + Vendor + Hostname)  {Colors.BLUE}║{Colors.RESET}")
        print(f"{Colors.BLUE}║{Colors.RESET} {Colors.CYAN}[4]{Colors.RESET} Thông tin mạng máy tính                {Colors.BLUE}║{Colors.RESET}")
        print(f"{Colors.BLUE}║{Colors.RESET} {Colors.RED}[0]{Colors.RESET} Quay lại                               {Colors.BLUE}║{Colors.RESET}")
        print(f"{Colors.BLUE}╚══════════════════════════════════════════════╝{Colors.RESET}")
        c = input(f"{Colors.GREEN}=> Lựa chọn:{Colors.RESET} ").strip()
        if   c == '1': ping_sweep(); pause()
        elif c == '2': port_scanner(); pause()
        elif c == '3': arp_scanner(); pause()
        elif c == '4': network_info(); pause()
        elif c == '0': break

# ─── WIFI SCANNER ─────────────────────────────────────────────────────────────
def get_mac_vendor(mac):
    try:
        oui  = mac.replace(':', '').replace('-', '').upper()[:6]
        resp = requests.get(f"https://api.macvendors.com/{oui}", timeout=3)
        return resp.text.strip() if resp.status_code == 200 else 'Unknown'
    except: return 'Unknown'

def signal_to_bars(sig_str):
    try:
        s = str(sig_str).strip()
        if '%' in s:
            pct = int(s.replace('%', ''))
            dbm = round((pct / 2) - 100)
        else:
            dbm = int(s.replace(' dBm', '').replace('dBm', ''))
            pct = max(0, min(100, 2 * (dbm + 100)))
        filled = int(pct / 20)
        bar    = '█' * filled + '░' * (5 - filled)
        if pct >= 75:   quality = f'{Colors.GREEN}Rất tốt{Colors.RESET}  '
        elif pct >= 50: quality = f'{Colors.CYAN}Tốt{Colors.RESET}      '
        elif pct >= 25: quality = f'{Colors.YELLOW}Yếu{Colors.RESET}      '
        else:           quality = f'{Colors.RED}Rất yếu{Colors.RESET}  '
        return f"{bar} {pct:3d}% ({dbm} dBm) [{quality}]"
    except: return str(sig_str)

def security_badge(auth_str):
    s = str(auth_str).upper()
    if 'WPA3' in s: return f'{Colors.GREEN}🔒 WPA3  (Rất an toàn){Colors.RESET}'
    if 'WPA2' in s: return f'{Colors.GREEN}🔒 WPA2  (An toàn){Colors.RESET}'
    if 'WPA'  in s: return f'{Colors.YELLOW}⚠️  WPA   (Yếu, nên nâng cấp){Colors.RESET}'
    if 'WEP'  in s: return f'{Colors.RED}❌ WEP   (Nguy hiểm – dễ crack){Colors.RESET}'
    if 'OPEN' in s or s in ['NONE', '', 'N/A']: return f'{Colors.RED}{Colors.BOLD}❌ OPEN  (Không có mật khẩu!){Colors.RESET}'
    return f'🔒 {auth_str}'

def wifi_scan_windows():
    nets = []
    try:
        r = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                           capture_output=True, text=True, encoding='utf-8', errors='ignore')
        cur = {}
        for line in r.stdout.splitlines():
            l = line.strip()
            if re.match(r'^SSID \d+ ', l) and 'BSSID' not in l:
                if cur: nets.append(cur)
                cur = {'ssid': l.split(':', 1)[1].strip() if ':' in l else '',
                       'bssids': [], 'auth': 'N/A', 'enc': 'N/A', 'type': 'N/A'}
            elif l.startswith('Authentication'):
                cur['auth'] = l.split(':', 1)[1].strip()
            elif l.startswith('Encryption'):
                cur['enc']  = l.split(':', 1)[1].strip()
            elif l.startswith('Network type'):
                cur['type'] = l.split(':', 1)[1].strip()
            elif re.match(r'^BSSID \d+', l):
                parts = l.split(':')
                bssid = ':'.join(parts[1:]).strip() if len(parts) > 1 else 'N/A'
                cur['bssids'].append({'bssid': bssid, 'signal': 'N/A', 'channel': 'N/A', 'radio': 'N/A'})
            elif l.startswith('Signal') and cur.get('bssids'):
                cur['bssids'][-1]['signal']  = l.split(':', 1)[1].strip()
            elif l.startswith('Radio type') and cur.get('bssids'):
                cur['bssids'][-1]['radio']   = l.split(':', 1)[1].strip()
            elif l.startswith('Channel') and cur.get('bssids'):
                cur['bssids'][-1]['channel'] = l.split(':', 1)[1].strip()
        if cur: nets.append(cur)
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi Windows WiFi scan: {e}{Colors.RESET}")
    return nets

def wifi_scan_linux():
    nets = []
    try:
        r = subprocess.run(
            ['nmcli', '-t', '-f', 'SSID,BSSID,CHAN,FREQ,SIGNAL,SECURITY,MODE', 'dev', 'wifi', 'list', '--rescan', 'yes'],
            capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            for line in r.stdout.splitlines():
                if not line.strip(): continue
                m = re.match(r'^(.*?):([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}):(.*)$', line)
                if m:
                    ssid    = m.group(1) or '<Hidden>'
                    bssid   = m.group(2)
                    rest    = m.group(3).split(':')
                    chan    = rest[0] if len(rest) > 0 else 'N/A'
                    freq    = rest[1] if len(rest) > 1 else 'N/A'
                    signal  = rest[2] if len(rest) > 2 else 'N/A'
                    security= rest[3] if len(rest) > 3 else 'N/A'
                    mode    = rest[4] if len(rest) > 4 else 'N/A'
                    freq_ghz = f"{float(freq)/1000:.1f} GHz" if freq.isdigit() else freq
                    signal_bar = signal_to_bars(f"{signal}%") if signal.lstrip('-').isdigit() else signal
                    nets.append({'ssid': ssid, 'bssid': bssid, 'channel': chan,
                                 'frequency': freq_ghz, 'signal': signal_bar,
                                 'security': security, 'mode': mode})
            if nets: return nets
    except FileNotFoundError: pass

    try:
        iface_r = subprocess.run(['iwconfig'], capture_output=True, text=True)
        ifaces  = [l.split()[0] for l in iface_r.stdout.splitlines() if 'IEEE 802.11' in l]
        iface   = ifaces[0] if ifaces else 'wlan0'
        r = subprocess.run(['sudo', 'iwlist', iface, 'scan'], capture_output=True, text=True, timeout=15)
        cur = {}
        for line in r.stdout.splitlines():
            l = line.strip()
            if l.startswith('Cell '):
                if cur: nets.append(cur)
                cur = {}
                am = re.search(r'Address: ([0-9A-F:]+)', l)
                cur['bssid'] = am.group(1) if am else 'N/A'
            elif 'ESSID:' in l:
                em = re.search(r'ESSID:"(.*)"', l)
                cur['ssid']  = em.group(1) if em else '<Hidden>'
            elif 'Channel:' in l:
                cm = re.search(r'Channel:(\d+)', l)
                cur['channel'] = cm.group(1) if cm else 'N/A'
            elif 'Frequency:' in l:
                fm = re.search(r'Frequency:([\d.]+) GHz', l)
                cur['frequency'] = (fm.group(1) + ' GHz') if fm else 'N/A'
            elif 'Signal level=' in l:
                sm = re.search(r'Signal level=(-?\d+)', l)
                cur['signal'] = signal_to_bars(sm.group(1)) if sm else 'N/A'
            elif 'Encryption key:' in l:
                cur['enc'] = 'Enabled' if 'on' in l else 'Open'
            elif 'IE: IEEE 802.11i/WPA2' in l:
                cur['security'] = 'WPA2'
            elif 'IE: WPA Version' in l:
                cur.setdefault('security', 'WPA')
        if cur: nets.append(cur)
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi iwlist: {e}{Colors.RESET}")
    return nets

def wifi_scan_macos():
    nets = []
    airport = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
    try:
        r = subprocess.run([airport, '-s'], capture_output=True, text=True, timeout=15)
        lines = r.stdout.splitlines()
        for line in lines[1:]:
            if not line.strip(): continue
            parts = line.split()
            bssid_idx = next((i for i, p in enumerate(parts)
                              if re.match(r'^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$', p)), None)
            if bssid_idx is not None:
                ssid     = ' '.join(parts[:bssid_idx]) or '<Hidden>'
                bssid    = parts[bssid_idx]
                rest     = parts[bssid_idx+1:]
                rssi     = rest[0] if len(rest) > 0 else 'N/A'
                channel  = rest[1] if len(rest) > 1 else 'N/A'
                security = ' '.join(rest[3:]) if len(rest) > 3 else 'N/A'
                nets.append({'ssid': ssid, 'bssid': bssid,
                             'signal': signal_to_bars(rssi),
                             'channel': channel, 'security': security})
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi airport: {e}{Colors.RESET}")
    return nets

def wifi_scanner():
    clear_screen()
    print(f"\n{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}║{Colors.BOLD}{Colors.WHITE}         📡 WIFI SCANNER – FULL SPECTRUM ANALYSIS             {Colors.RESET}{Colors.CYAN}║{Colors.RESET}")
    print(f"{Colors.CYAN}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.RED}[!] Chỉ sử dụng trên mạng bạn sở hữu hoặc có quyền kiểm tra.{Colors.RESET}\n")
    print(f"{Colors.YELLOW}[*] Đang quét... vui lòng đợi.\n{Colors.RESET}")

    sys_name = platform.system().lower()
    if   sys_name == 'windows': nets = wifi_scan_windows()
    elif sys_name == 'linux':   nets = wifi_scan_linux()
    elif sys_name == 'darwin':  nets = wifi_scan_macos()
    else: print(f"{Colors.RED}[-] Hệ điều hành không hỗ trợ.{Colors.RESET}"); return

    if not nets:
        print(f"{Colors.RED}[-] Không tìm thấy mạng WiFi nào.{Colors.RESET}")
        return

    print_separator('═', 65, Colors.MAGENTA)
    print(f"  {Colors.BOLD}Phát hiện {len(nets)} mạng WiFi{Colors.RESET}")
    print_separator('═', 65, Colors.MAGENTA)

    if sys_name == 'windows':
        for i, net in enumerate(nets, 1):
            ssid  = net.get('ssid') or '<Hidden Network>'
            auth  = net.get('auth', 'N/A')
            enc   = net.get('enc',  'N/A')
            ntype = net.get('type', 'N/A')
            badge = security_badge(auth)

            print(f"\n  {Colors.CYAN}[{i:02d}]{Colors.RESET} {Colors.BOLD}SSID{Colors.RESET}        : {Colors.CYAN}{ssid}{Colors.RESET}")
            print(f"       Xác thực    : {auth}")
            print(f"       Mã hóa      : {enc}")
            print(f"       Bảo mật     : {badge}")
            for j, b in enumerate(net.get('bssids', []), 1):
                print(f"       {Colors.YELLOW}──── AP #{j} ────────────────────────────{Colors.RESET}")
                print(f"       BSSID       : {b.get('bssid','N/A')}")
                print(f"       Tín hiệu    : {signal_to_bars(b.get('signal','N/A'))}")
                print(f"       Kênh        : {b.get('channel','N/A')}")
    else:
        for i, net in enumerate(nets, 1):
            ssid     = net.get('ssid') or '<Hidden Network>'
            bssid    = net.get('bssid',    'N/A')
            channel  = net.get('channel',  'N/A')
            freq     = net.get('frequency','N/A')
            sig_disp = net.get('signal',   'N/A')
            security = net.get('security', net.get('enc', net.get('auth', 'N/A')))
            badge    = security_badge(security)

            print(f"\n  {Colors.CYAN}[{i:02d}]{Colors.RESET} {Colors.BOLD}SSID{Colors.RESET}       : {Colors.CYAN}{ssid}{Colors.RESET}")
            print(f"       BSSID      : {bssid}")
            print(f"       Kênh       : {channel}  |  Tần số: {freq}")
            print(f"       Tín hiệu   : {sig_disp}")
            print(f"       Bảo mật    : {badge}")

# ─── ADVANCED RECON ───────────────────────────────────────────────────────────
def extract_subdomains():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] SUBDOMAIN ENUMERATION (VIA CRT.SH){Colors.RESET}")
    domain = input(f"{Colors.CYAN}Nhập Domain (VD: facebook.com): {Colors.RESET}").strip()
    if not domain: return
    print(f"{Colors.YELLOW}[*] Truy vấn certificate database cho '{domain}'...{Colors.RESET}")
    try:
        url  = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            subs = set()
            for entry in data:
                name = entry.get('name_value', '')
                subs.update(name.split('\n') if '\n' in name else [name])
            clean = sorted(s for s in subs if s.endswith(domain))
            for s in clean:
                print(f"{Colors.GREEN}[+]{Colors.RESET} {s}")
            print(f"\n{Colors.CYAN}[*] Tổng cộng: {len(clean)} subdomain.{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] Lỗi API crt.sh (Code: {resp.status_code}){Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi kết nối: {e}{Colors.RESET}")

def http_header_analyzer():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] HTTP HEADER ANALYZER & SECURITY CHECKER{Colors.RESET}")
    url = input(f"{Colors.CYAN}Nhập URL (VD: https://example.com): {Colors.RESET}").strip()
    if not url: return
    if not url.startswith("http"): url = "http://" + url
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        print(f"\n{Colors.GREEN}[+] Status Code  : {resp.status_code}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Final URL    : {resp.url}{Colors.RESET}")
        print_separator()
        for k, v in resp.headers.items():
            print(f"  {Colors.CYAN}{k:<40}{Colors.RESET}: {v}")
        print_separator()
        print(f"{Colors.YELLOW}[*] ĐÁNH GIÁ SECURITY HEADERS:{Colors.RESET}")
        checks = [
            ('Strict-Transport-Security', 'HSTS – bảo vệ HTTPS'),
            ('Content-Security-Policy',   'CSP  – ngăn XSS'),
            ('X-Frame-Options',           'Clickjacking protection'),
            ('X-XSS-Protection',          'XSS filter'),
            ('X-Content-Type-Options',    'MIME sniffing protection'),
            ('Referrer-Policy',           'Referrer policy'),
        ]
        score = 0
        for h, desc in checks:
            if h in resp.headers:
                print(f"  {Colors.GREEN}✅ {h:<38} ({desc}){Colors.RESET}")
                score += 1
            else:
                print(f"  {Colors.RED}❌ {h:<38} THIẾU! ({desc}){Colors.RESET}")
        grade = 'A' if score == len(checks) else ('B' if score >= 4 else ('C' if score >= 2 else 'D'))
        
        grade_color = Colors.GREEN if grade in ['A','B'] else Colors.RED
        print(f"\n  {Colors.BOLD}Điểm bảo mật:{Colors.RESET} {score}/{len(checks)}  |  {Colors.BOLD}Hạng:{Colors.RESET} {grade_color}{grade}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi kết nối: {e}{Colors.RESET}")

def dns_lookup():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] DNS LOOKUP – PHÂN TÍCH DNS TOÀN DIỆN{Colors.RESET}")
    domain = input(f"{Colors.CYAN}Nhập domain: {Colors.RESET}").strip()
    if not domain: return
    print(f"\n{Colors.YELLOW}[*] Truy vấn Cloudflare DNS-over-HTTPS cho '{domain}'...{Colors.RESET}\n")
    for rtype, label in [('A','IPv4'), ('AAAA','IPv6'), ('MX','Mail'), ('TXT','TXT'), ('NS','NameServer')]:
        try:
            r = requests.get("https://cloudflare-dns.com/dns-query", params={"name": domain, "type": rtype}, headers={"Accept": "application/dns-json"}, timeout=5)
            answers = r.json().get('Answer', [])
            if answers:
                print(f"  {Colors.MAGENTA}[{label} Records]{Colors.RESET}")
                for a in answers: print(f"    TTL {a.get('TTL','?'):>6}s  →  {Colors.CYAN}{a.get('data','?')}{Colors.RESET}")
        except: pass

def advanced_recon_menu():
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}╔══════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.YELLOW}║{Colors.BOLD}{Colors.WHITE}               🔬 ADVANCED RECON                  {Colors.RESET}{Colors.YELLOW}║{Colors.RESET}")
        print(f"{Colors.YELLOW}╠══════════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.YELLOW}║{Colors.RESET} {Colors.CYAN}[1]{Colors.RESET} Subdomain Enumeration (Crt.sh)             {Colors.YELLOW}║{Colors.RESET}")
        print(f"{Colors.YELLOW}║{Colors.RESET} {Colors.CYAN}[2]{Colors.RESET} HTTP Header Analyzer & Security Check      {Colors.YELLOW}║{Colors.RESET}")
        print(f"{Colors.YELLOW}║{Colors.RESET} {Colors.CYAN}[3]{Colors.RESET} DNS Lookup (Cloudflare DoH)                {Colors.YELLOW}║{Colors.RESET}")
        print(f"{Colors.YELLOW}║{Colors.RESET} {Colors.RED}[0]{Colors.RESET} Quay lại                                   {Colors.YELLOW}║{Colors.RESET}")
        print(f"{Colors.YELLOW}╚══════════════════════════════════════════════════╝{Colors.RESET}")
        c = input(f"{Colors.GREEN}=> Lựa chọn:{Colors.RESET} ").strip()
        if   c == '1': extract_subdomains();    pause()
        elif c == '2': http_header_analyzer();  pause()
        elif c == '3': dns_lookup();            pause()
        elif c == '0': break

# ─── HACKING TOOLS (MỞ RỘNG) ──────────────────────────────────────────────────

def get_default_gateway():
    sys_name = platform.system().lower()
    try:
        if sys_name == 'windows':
            r = subprocess.run(['ipconfig'], capture_output=True, text=True, errors='ignore')
            for line in r.stdout.splitlines():
                if 'Default Gateway' in line or 'Cổng mặc định' in line:
                    return line.split(':')[-1].strip()
        else:
            r = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            for line in r.stdout.splitlines():
                if 'default via' in line:
                    return line.split()[2]
    except: pass
    return None

def router_deep_recon():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] ROUTER DEEP RECON – QUÉT THÔNG TIN BỘ ĐỊNH TUYẾN{Colors.RESET}")
    print(f"{Colors.YELLOW}[!] Gửi các gói tin UPnP và HTTP GET để ép router nhả thông tin ẩn.{Colors.RESET}\n")
    
    gw_ip = get_default_gateway()
    if not gw_ip:
        gw_ip = input(f"{Colors.RED}[-] Không tự tìm được Gateway. Nhập thủ công (VD: 192.168.1.1): {Colors.RESET}").strip()
        if not gw_ip: return
    else:
        print(f"{Colors.CYAN}[*] Phát hiện Default Gateway: {gw_ip}{Colors.RESET}")

    mac, vendor = "Unknown", "Unknown"
    try:
        arp_r = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        for line in arp_r.stdout.splitlines():
            if gw_ip in line:
                m = re.search(r'([0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2}[:\-][0-9a-fA-F]{2})', line)
                if m:
                    mac = m.group(1).replace('-', ':').upper()
                    v_res = requests.get(f"https://api.macvendors.com/{mac.replace(':','')[:6]}", timeout=2)
                    if v_res.status_code == 200: vendor = v_res.text.strip()
                    break
    except: pass

    print_separator()
    print(f"  {Colors.BOLD}Gateway IP{Colors.RESET} : {Colors.CYAN}{gw_ip}{Colors.RESET}")
    print(f"  {Colors.BOLD}MAC Address{Colors.RESET}: {Colors.YELLOW}{mac}{Colors.RESET}")
    print(f"  {Colors.BOLD}Nhà SX{Colors.RESET}     : {vendor}")
    print_separator()

    print(f"\n{Colors.CYAN}[*] Đang quét firmware qua HTTP Header...{Colors.RESET}")
    firmware_server = "Không xác định"
    for port, scheme in [(80, 'http'), (443, 'https'), (8080, 'http')]:
        try:
            r = requests.get(f"{scheme}://{gw_ip}:{port}", timeout=2, verify=False, allow_redirects=False)
            if 'Server' in r.headers:
                firmware_server = r.headers['Server']
                print(f"  {Colors.GREEN}[+] Port {port:<4} Server Header: {firmware_server}{Colors.RESET}")
                break
        except: pass

    print(f"\n{Colors.CYAN}[*] Đang khai thác giao thức UPnP/SSDP (Port 1900)...{Colors.RESET}")
    ssdp_request = (
        'M-SEARCH * HTTP/1.1\r\n'
        'HOST: 239.255.255.250:1900\r\n'
        'MAN: "ssdp:discover"\r\n'
        'MX: 2\r\n'
        'ST: upnp:rootdevice\r\n\r\n'
    )
    upnp_info_url = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        sock.sendto(ssdp_request.encode(), ('239.255.255.250', 1900))
        while True:
            data, addr = sock.recvfrom(1024)
            if addr[0] == gw_ip:
                response = data.decode('utf-8', errors='ignore')
                for line in response.splitlines():
                    if line.lower().startswith('location:'):
                        upnp_info_url = line.split(':', 1)[1].strip()
                        break
                if upnp_info_url: break
    except socket.timeout: pass
    except Exception as e: print(f"{Colors.RED}[-] Lỗi SSDP: {e}{Colors.RESET}")

    if upnp_info_url:
        print(f"  {Colors.GREEN}[+] Tìm thấy tệp mô tả thiết bị: {upnp_info_url}{Colors.RESET}")
        try:
            r = requests.get(upnp_info_url, timeout=3)
            root = ET.fromstring(r.text)
            ns = {'ns': 'urn:schemas-upnp-org:device-1-0'}
            device = root.find('ns:device', ns)
            if device is not None:
                print_separator()
                print(f"  {Colors.MAGENTA}[THÔNG TIN PHẦN CỨNG CHI TIẾT (UPnP)]{Colors.RESET}")
                def safe_find(tag):
                    e = device.find(f'ns:{tag}', ns)
                    return e.text if e is not None else "N/A"
                
                print(f"  Model Name        : {Colors.CYAN}{safe_find('modelName')}{Colors.RESET}")
                print(f"  Model Description : {safe_find('modelDescription')}")
                print(f"  Manufacturer      : {safe_find('manufacturer')}")
                print(f"  Friendly Name     : {safe_find('friendlyName')}")
                print(f"  Model Number      : {safe_find('modelNumber')}")
                print(f"  Serial Number     : {safe_find('serialNumber')}")
                print(f"  UDN (Unique ID)   : {Colors.YELLOW}{safe_find('UDN')}{Colors.RESET}")
                print_separator()
        except: print(f"  {Colors.RED}[-] Không thể phân tích tệp XML.{Colors.RESET}")
    else:
        print(f"  {Colors.RED}[-] Router không mở cổng UPnP hoặc đã chặn Multicast.{Colors.RESET}")

def web_dir_fuzzer():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] WEB DIRECTORY FUZZER (Phát hiện thư mục ẩn){Colors.RESET}")
    target = input(f"{Colors.CYAN}Nhập URL (VD: http://example.com): {Colors.RESET}").strip()
    if not target: return
    if not target.endswith('/'): target += '/'
    
    payloads = [
        "admin", "login", "wp-admin", "wp-login.php", "backup", "db", 
        "config.php", "phpmyadmin", ".git", ".env", "test", "api", 
        "dashboard", "robots.txt", "sitemap.xml", "old", "administrator", "setup"
    ]
    print(f"{Colors.YELLOW}[*] Đang Fuzzing {len(payloads)} endpoints trên '{target}'...\n{Colors.RESET}")
    
    def check_path(path):
        url = target + path
        try:
            r = requests.get(url, timeout=3, allow_redirects=False)
            if r.status_code in [200, 301, 302, 401, 403]:
                color = Colors.GREEN if r.status_code == 200 else Colors.YELLOW
                return f"{color}[+] {r.status_code} | {url}{Colors.RESET}"
        except: pass
        return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_path, p): p for p in payloads}
        for future in as_completed(futures):
            res = future.result()
            if res: print(res)
    print(f"\n{Colors.CYAN}[*] Quét hoàn tất.{Colors.RESET}")

def sql_injection_scanner():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] SQL INJECTION VULNERABILITY SCANNER (Basic){Colors.RESET}")
    print(f"{Colors.RED}[!] Chỉ quét trên hệ thống được phép (VD: testphp.vulnweb.com).{Colors.RESET}")
    
    url = input(f"{Colors.CYAN}Nhập URL có tham số (VD: http://site.com/page.php?id=1): {Colors.RESET}").strip()
    if not url or "?" not in url:
        print(f"{Colors.RED}[-] URL không hợp lệ hoặc thiếu tham số GET.{Colors.RESET}")
        return

    payloads = ["'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1"]
    errors = ["syntax error", "mysql_fetch", "maria", "ora-", "postgresql", "sql syntax"]
    
    print(f"{Colors.YELLOW}[*] Đang thử chèn payload SQLi vào URL...{Colors.RESET}\n")
    vuln_found = False
    
    for payload in payloads:
        test_url = url + payload
        try:
            r = requests.get(test_url, timeout=5)
            for err in errors:
                if err.lower() in r.text.lower():
                    print(f"{Colors.RED}{Colors.BOLD}[!] PHÁT HIỆN LỖ HỔNG SQL INJECTION!{Colors.RESET}")
                    print(f"  {Colors.GREEN}Payload thành công:{Colors.RESET} {payload}")
                    print(f"  {Colors.GREEN}URL Test:{Colors.RESET} {test_url}")
                    print(f"  {Colors.YELLOW}Dấu hiệu:{Colors.RESET} Trả về lỗi Database ({err})")
                    vuln_found = True
                    break
            if vuln_found: break
        except Exception as e:
            print(f"{Colors.RED}[-] Lỗi kết nối: {e}{Colors.RESET}")
            
    if not vuln_found:
        print(f"{Colors.GREEN}[+] Không phát hiện dấu hiệu SQLi cơ bản trên tham số này.{Colors.RESET}")

def email_extractor():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] WEB EMAIL EXTRACTOR (Trích xuất Email từ Website){Colors.RESET}")
    url = input(f"{Colors.CYAN}Nhập URL mục tiêu (VD: https://example.com/contact): {Colors.RESET}").strip()
    if not url: return
    if not url.startswith("http"): url = "http://" + url
    
    print(f"{Colors.YELLOW}[*] Đang cào dữ liệu từ '{url}'...{Colors.RESET}")
    try:
        r = requests.get(url, timeout=10)
        # Regex tìm email
        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text))
        
        if emails:
            print(f"\n{Colors.GREEN}[+] TÌM THẤY {len(emails)} ĐỊA CHỈ EMAIL:{Colors.RESET}")
            for mail in emails:
                print(f"  -> {Colors.CYAN}{mail}{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}[-] Không tìm thấy email nào trên trang này.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi kết nối hoặc URL không hợp lệ: {e}{Colors.RESET}")

def md5_hash_cracker():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] ONLINE MD5 HASH CRACKER (via Nitrxgen API){Colors.RESET}")
    hash_val = input(f"{Colors.CYAN}Nhập chuỗi MD5 cần giải mã: {Colors.RESET}").strip()
    if len(hash_val) != 32:
        print(f"{Colors.RED}[-] Đây không phải là mã MD5 hợp lệ (phải đủ 32 ký tự).{Colors.RESET}")
        return
        
    print(f"{Colors.YELLOW}[*] Đang tra cứu trên Database với hơn 1000 tỷ Hashes...{Colors.RESET}")
    try:
        r = requests.get(f"https://www.nitrxgen.net/md5db/{hash_val}", timeout=5)
        if r.text:
            print(f"\n{Colors.GREEN}{Colors.BOLD}[+] CRACK THÀNH CÔNG!{Colors.RESET}")
            print(f"  Hash: {Colors.CYAN}{hash_val}{Colors.RESET}")
            print(f"  Text: {Colors.RED}{Colors.BOLD}{r.text}{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}[-] Không tìm thấy plaintext cho Hash này trong Database.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Lỗi kết nối API: {e}{Colors.RESET}")

def hacking_tools_menu():
    while True:
        clear_screen()
        print(f"{Colors.RED}╔════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.BOLD}{Colors.WHITE}                  🪓 HACKING & RECON TOOLS                  {Colors.RESET}{Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}╠════════════════════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.RESET} {Colors.CYAN}[1]{Colors.RESET} 📡 Router Deep Recon (Ép Router nhả Info)              {Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.RESET} {Colors.CYAN}[2]{Colors.RESET} 🔍 Web Directory Fuzzer (Tìm thư mục/path ẩn)          {Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.RESET} {Colors.CYAN}[3]{Colors.RESET} 💉 SQL Injection Scanner (Kiểm tra lỗi DB)             {Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.RESET} {Colors.CYAN}[4]{Colors.RESET} 📧 Web Email Extractor (Cào Email từ trang web)        {Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.RESET} {Colors.CYAN}[5]{Colors.RESET} 🔓 MD5 Hash Cracker (Online Database cực khủng)        {Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}║{Colors.RESET} {Colors.RED}[0]{Colors.RESET} ◀  Quay lại menu chính                                 {Colors.RED}║{Colors.RESET}")
        print(f"{Colors.RED}╚════════════════════════════════════════════════════════════╝{Colors.RESET}")
        c = input(f"{Colors.GREEN}=> Lựa chọn:{Colors.RESET} ").strip()
        if   c == '1': router_deep_recon(); pause()
        elif c == '2': web_dir_fuzzer();    pause()
        elif c == '3': sql_injection_scanner(); pause()
        elif c == '4': email_extractor(); pause()
        elif c == '5': md5_hash_cracker(); pause()
        elif c == '0': break
# ─── OSINT TOOLS & MEDIA ──────────────────────────────────────────────────────
def osint_username():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] TRA CỨU USERNAME (ADVANCED OSINT){Colors.RESET}")
    username = input(f"{Colors.CYAN}Nhập username: {Colors.RESET}").strip()
    if not username: return
    headers  = {"User-Agent": "Mozilla/5.0"}
    
    platforms = [
        ("GitHub", "https://github.com/{}"),
        ("TikTok", "https://www.tiktok.com/@{}"),
        ("YouTube", "https://www.youtube.com/@{}"),
        ("Instagram", "https://www.instagram.com/{}/"),
        ("Reddit", "https://www.reddit.com/user/{}/"),
        ("Twitch", "https://www.twitch.tv/{}"),
        ("Steam", "https://steamcommunity.com/id/{}"),
        ("Twitter (X)", "https://twitter.com/{}"),
        ("Pinterest", "https://www.pinterest.com/{}/"),
        ("SoundCloud", "https://soundcloud.com/{}"),
        ("Linktree", "https://linktr.ee/{}"),
        ("HackerOne", "https://hackerone.com/{}"),
        ("TryHackMe", "https://tryhackme.com/p/{}"),
        ("Spotify", "https://open.spotify.com/user/{}"),
        ("Pastebin", "https://pastebin.com/u/{}"),
        ("Roblox", "https://www.roblox.com/user.aspx?username={}"),
        ("Vimeo", "https://vimeo.com/{}")
    ]
    
    print(f"\n{Colors.YELLOW}[*] Quét '{username}' trên {len(platforms)} nền tảng...{Colors.RESET}\n")
    
    def check_platform(name, url_tpl):
        url = url_tpl.format(username)
        try:
            r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            if r.status_code == 200: 
                print(f"{Colors.GREEN}[+] {name:<12}:{Colors.RESET} FOUND – {Colors.CYAN}{url}{Colors.RESET}")
            else: 
                print(f"{Colors.RED}[-] {name:<12}:{Colors.RESET} Not Found")
        except: 
            print(f"{Colors.YELLOW}[?] {name:<12}:{Colors.RESET} Timeout/Error")

    with ThreadPoolExecutor(max_workers=10) as executor:
        for name, url_tpl in platforms:
            executor.submit(check_platform, name, url_tpl)

def media_downloader():
    clear_screen()
    print(f"\n{Colors.GREEN}[+] TRÌNH TẢI MEDIA ĐA NỀN TẢNG (YT-DLP){Colors.RESET}")
    url = input(f"{Colors.CYAN}Nhập URL video/audio: {Colors.RESET}").strip()
    if not url: return
    opts = {'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}
    try:
        print(f"{Colors.YELLOW}[*] Đang tiến hành tải xuống...{Colors.RESET}")
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
        print(f"{Colors.GREEN}[+] Hoàn tất!{Colors.RESET}")
    except Exception as e: 
        print(f"{Colors.RED}[-] Lỗi: {e}{Colors.RESET}")

# ─── CRYPTOGRAPHY & IP ────────────────────────────────────────────────────────
def crypto_ip_menu():
    while True:
        clear_screen()
        print(f"{Colors.MAGENTA}╔══════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.MAGENTA}║{Colors.BOLD}{Colors.WHITE}          🔑 CRYPTOGRAPHY & IP GEOLOCATION        {Colors.RESET}{Colors.MAGENTA}║{Colors.RESET}")
        print(f"{Colors.MAGENTA}╠══════════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[1]{Colors.RESET} Mã hóa / Giải mã Base64                    {Colors.MAGENTA}║{Colors.RESET}")
        print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.CYAN}[2]{Colors.RESET} Truy xuất vị trí IP (GeoIP)                {Colors.MAGENTA}║{Colors.RESET}")
        print(f"{Colors.MAGENTA}║{Colors.RESET} {Colors.RED}[0]{Colors.RESET} Quay lại                                   {Colors.MAGENTA}║{Colors.RESET}")
        print(f"{Colors.MAGENTA}╚══════════════════════════════════════════════════╝{Colors.RESET}")
        c = input(f"{Colors.GREEN}=> Lựa chọn:{Colors.RESET} ").strip()
        if c == '1':
            txt = input(f"\n{Colors.CYAN}Nhập văn bản: {Colors.RESET}")
            print(f"{Colors.GREEN}[+] Encode : {Colors.YELLOW}{base64.b64encode(txt.encode()).decode()}{Colors.RESET}")
            try: print(f"{Colors.GREEN}[+] Decode : {Colors.YELLOW}{base64.b64decode(txt.encode()).decode()}{Colors.RESET}")
            except: pass
            pause()
        elif c == '2':
            ip = input(f"\n{Colors.CYAN}Nhập IP (bỏ trống = IP hiện tại): {Colors.RESET}").strip()
            if not ip:
                try: ip = requests.get("https://api.ipify.org", timeout=5).text
                except: pass
            try:
                d = requests.get(f"http://ip-api.com/json/{ip}").json()
                if d['status'] == 'success':
                    print(f"\n  {Colors.BOLD}IP{Colors.RESET}        : {Colors.CYAN}{ip}{Colors.RESET}")
                    print(f"  {Colors.BOLD}Quốc gia{Colors.RESET}  : {d['country']} ({d['countryCode']})")
                    print(f"  {Colors.BOLD}Thành phố{Colors.RESET} : {d['city']}")
                    print(f"  {Colors.BOLD}ISP{Colors.RESET}       : {d['isp']}")
                    print(f"  {Colors.BOLD}Tọa độ{Colors.RESET}    : {d['lat']}, {d['lon']}")
            except: pass
            pause()
        elif c == '0': break

# ─── MAIN FLOW ────────────────────────────────────────────────────────────────
def main():
    while True:
        try:
            choice = main_menu()
            if   choice == '1': network_tools_menu()
            elif choice == '2': wifi_scanner(); pause()
            elif choice == '3': advanced_recon_menu()
            elif choice == '4': osint_username(); pause()
            elif choice == '5': media_downloader(); pause()
            elif choice == '6': hacking_tools_menu()
            elif choice == '7': crypto_ip_menu()
            elif choice == '0':
                clear_screen()
                print(f"{Colors.RED}[*] Thoát... Hacking is not a crime, it's an art. Tạm biệt!{Colors.RESET}")
                sys.exit(0)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Ctrl+C – Đang thoát...{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}[!] Lỗi: {e}{Colors.RESET}")
            pause()

if __name__ == "__main__":
    main()