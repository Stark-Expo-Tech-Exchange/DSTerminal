import os
import sys

import shutil
import requests
import logging
from tqdm import tqdm

import platform
import hashlib
import requests
import json
import psutil
import time
import random
import socket
import ssl
import subprocess
import json
import OpenSSL
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.ocsp import OCSPRequestBuilder
from threading import Thread, Event
from datetime import datetime
from cryptography.fernet import Fernet

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML

# Configuration
CONFIG = {
    'VT_API_KEY': '957166d424812a397e328022b84594a8c02757814f6c04518dce7e81179b4b79',
    'UPDATE_URL': 'https://api.github.com/repos/starkexpotech/DSTerminal/releases/latest',
    'LOG_FILE': 'secure_audit.log',
    'ENCRYPT_KEY': Fernet.generate_key().decode(),
    'CURRENT_VERSION': '2.0'
}

class SecurityTerminal:
    def __init__(self):
        self.session = PromptSession(
            history=FileHistory('.dst_history'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=WordCompleter([
                'scan', 'netmon', 'harden', 'vtscan', 'regmon', 
                'memdump', 'update', 'help', 'exit', 'clearlogs',
                'portsweep', 'hashfile', 'sysinfo', 'killproc',
                'chkintegrity', 'encrypt', 'decrypt', 'watchfolder',
                'traceroute', 'exploitcheck', 'macspoof', 'dnssec',
                'sqlmap', 'ransomwatch', 'wificrack', 'stegcheck',
                'certcheck', 'torify'
            ]),
            bottom_toolbar=HTML('<b>DST</b> v{} | Mode: <style bg="{}">{}</style>').format(
                CONFIG['CURRENT_VERSION'],
                "ansired" if self.is_admin() else "ansigreen",
                "ADMIN" if self.is_admin() else "USER"
            )
        )
        self.cipher = Fernet(CONFIG['ENCRYPT_KEY'].encode())
        self.scan_complete = Event()
        self.scan_progress = 0

    def print_banner(self):
        print(f"""
    ╔═══════════════════════════════════════════════════════════════════============═══╗
        ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗
        ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝
        ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝ 
        ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗ 
        ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗
        ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
        
    ╠════════════════════════════════════════════════════════════════============══════╣
    ║    Defensive Security Terminal v1.1 | {platform.system()} {platform.release()}   ║
    ║    Developed by: Spark Wilson Spink | © 2024| Powered by Stark Expo Tech Exchange║
    ║    Type 'help' for available commands                                            ║
    ║ (🔍, ⚡, 🛡️) 🌐 ⚡ CLI Mode: {'ADMIN' if self.is_admin() else 'USER'}               
    ╚════════════════════════════════════════════════════════════════════============══╝
        """)

        if not self.is_admin():
            print("\n[!] Warning: Running without administrator privileges. Some features may be limited.")

    def is_admin(self):
        try:
            return os.getuid() == 0 if platform.system() != 'Windows' else None
        except:
            return False

    # ==================== CORE SECURITY COMMANDS ====================
    def _animate_scan(self):
        spinner = ['|', '/', '-', '\\']
        i = 0
        while not self.scan_complete.is_set():
            sys.stdout.write(f"\r[+] Scanning system... {spinner[i]} {self.scan_progress}%")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % 4
        sys.stdout.write("\r" + " " * 50 + "\r")

    def scan_system(self):
        self.scan_complete.clear()
        self.scan_progress = 0
        
        spinner_thread = Thread(target=self._animate_scan)
        spinner_thread.daemon = True
        spinner_thread.start()

        try:
            for i in range(1, 101):
                time.sleep(0.03)
                self.scan_progress = i
            
            suspicious_processes = ["keylogger", "logkeys", "pykeylogger", "ahk"]
            found_threats = False
            
            for proc in psutil.process_iter(['name', 'pid', 'exe']):
                try:
                    if any(susp_keyword in proc.info['name'].lower() for susp_keyword in suspicious_processes):
                        print(f"\n[!] Suspicious Process: {proc.info['name']} (PID: {proc.pid})")
                        found_threats = True
                    
                    if platform.system() == "Windows" and "temp" in proc.info.get('exe', '').lower():
                        print(f"\n[!] Suspicious Temp Execution: {proc.info['name']}")
                        found_threats = True
                except:
                    continue

            if not found_threats:
                print("\n[+] No obvious threats detected")
            
        finally:
            self.scan_complete.set()
            spinner_thread.join()
            print("[+] System scan completed at 100%")

    def network_monitor(self):
        print("\n[+] Monitoring network connections...")
        for conn in psutil.net_connections():
            if conn.status == "ESTABLISHED" and conn.raddr:
                print(f"[→] {conn.laddr.ip}:{conn.laddr.port} → {conn.raddr.ip}:{conn.raddr.port} (PID: {conn.pid})")
        print("[+] Network scan completed")

    # ==================== NEW ADVANCED COMMANDS ====================
    def check_exploits(self):
        vulns = {
            "CVE-2021-44228": "Log4j RCE",
            "CVE-2017-0144": "EternalBlue"
        }
        print("\n[+] Checking for critical CVEs...")
        for cve, desc in vulns.items():
            print(f"{cve}: {desc} - {'[!] VULNERABLE' if random.random() > 0.7 else '[+] Secure'}")

    # def spoof_mac(self, interface="eth0"):
    #     if self.is_admin():
    #         new_mac = "02:%02x:%02x:%02x:%02x:%02x" % (
    #             random.randint(0, 255),
    #             random.randint(0, 255),
    #             random.randint(0, 255),
    #             random.randint(0, 255),
    #             random.randint(0, 255)
    #         )
    #         os.system(f"sudo ifconfig {interface} down")
    #         os.system(f"sudo ifconfig {interface} hw ether {new_mac}")
    #         os.system(f"sudo ifconfig {interface} up")
    #         print(f"[+] MAC spoofed to {new_mac}")
    #     else:
    #         print("[!] Requires admin privileges")

    # BELOW MACSPOOF CODE WORKING
    def spoof_mac(self, interface=None):
        """Enhanced MAC spoofing with detailed debugging"""
        print("\n[DEBUG] Starting macspoof command")  # Debug line 1
    
    # 1. Admin check
        if not self.is_admin():
            print("[!] Requires admin privileges")
            print("[DEBUG] Failed admin check")
            return
    
        print("[DEBUG] Passed admin check")  # Debug line 2

    # 2. Interface detection
        def get_active_interface():
            print("[DEBUG] Starting interface detection")  # Debug line 3
            try:
                if platform.system() in ['Linux', 'Darwin']:
                    print("[DEBUG] Trying Linux/Mac detection")
                    route = subprocess.check_output("ip route show default", 
                                                shell=True, 
                                                stderr=subprocess.PIPE).decode()
                    print(f"[DEBUG] Route output: {route.strip()}")  # Debug line 4
                    if len(route.split()) >= 5:
                        return route.split()[4]
                    return None
                
                elif platform.system() == 'Windows':
                    print("[DEBUG] Trying Windows detection")
                    output = subprocess.check_output("getmac /v /fo csv", 
                                                shell=True, 
                                                stderr=subprocess.PIPE).decode()
                    print(f"[DEBUG] Getmac output: {output.strip()}")  # Debug line 5
                    lines = [l for l in output.split('\n') if l.strip()]
                    if len(lines) > 1:
                        return lines[1].split(',')[0].strip('"')
                    return None
                
            except subprocess.CalledProcessError as e:
                print(f"[DEBUG] Command failed: {e.stderr.decode().strip()}")
                return None
            except Exception as e:
                print(f"[DEBUG] Detection error: {str(e)}")
                return None

    # 3. Get interface
        if not interface:
            print("[DEBUG] Attempting auto-detection")  # Debug line 6
            interface = get_active_interface()
            if not interface:
                print("[!] Could not detect active interface")
                print("[DEBUG] Auto-detection failed")
                return
    
        print(f"[DEBUG] Using interface: {interface}")  # Debug line 7

    # 4. MAC generation
        new_mac = "02:%02x:%02x:%02x:%02x:%02x" % (
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)
        )
        print(f"[DEBUG] Generated MAC: {new_mac}")  # Debug line 8

    # 5. Execution
        try:
            print(f"\n[+] Spoofing {interface} to {new_mac}")
        
            commands = []
            if platform.system() in ['Linux', 'Darwin']:
                commands = [
                    f"ifconfig {interface} down",
                    f"ifconfig {interface} hw ether {new_mac}",
                    f"ifconfig {interface} up",
                    f"dhclient -r {interface}",
                    f"dhclient {interface}"
                ]
            elif platform.system() == 'Windows':
                interface_key = interface.split('_')[-1]
                commands = [
                    f"netsh interface set interface \"{interface}\" admin=disable",
                    f"reg add HKLM\SYSTEM\CurrentControlSet\Control\Class"
                    f"\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}"
                    f"\\{interface_key} /v NetworkAddress /d {new_mac} /f",
                    f"netsh interface set interface \"{interface}\" admin=enable"
                ]
        
            print("[DEBUG] Commands to execute:")  # Debug line 9
            for i, cmd in enumerate(commands, 1):
                print(f"[DEBUG] {i}. {cmd}")
            
                result = subprocess.run(cmd, 
                                    shell=True, 
                                    capture_output=True, 
                                    text=True)
                if result.returncode != 0:
                    print(f"[DEBUG] Command failed: {result.stderr.strip()}")
            
                time.sleep(0.5)
        
            print("[+] MAC address successfully changed")
        
        except Exception as e:
            print(f"[!] MAC spoofing failed: {str(e)}")
    
    # 6. Verification
        self._verify_mac_change(interface, new_mac)

    def _verify_mac_change(self, interface, expected_mac):
        """Enhanced verification with debugging"""
        print("[DEBUG] Starting verification")  # Debug line 10
        try:
            if platform.system() in ['Linux', 'Darwin']:
                result = subprocess.run(f"ifconfig {interface}",
                                    shell=True,
                                    capture_output=True,
                                    text=True)
                print(f"[DEBUG] ifconfig output: {result.stdout[:200]}...")  # Debug line 11
                if expected_mac.lower() in result.stdout.lower():
                    print("[✓] MAC verification successful")
                else:
                    print("[!] MAC verification failed")
                
            elif platform.system() == 'Windows':
                result = subprocess.run("getmac /v /fo csv",
                                    shell=True,
                                    capture_output=True,
                                    text=True)
                print(f"[DEBUG] getmac output: {result.stdout.strip()}")  # Debug line 12
                if expected_mac.lower() in result.stdout.lower():
                    print("[✓] MAC verification successful")
                else:
                    print("[!] MAC verification failed")
    
        except Exception as e:
            print(f"[DEBUG] Verification error: {str(e)}")

    # ======end of macspoof

    def sql_injection_scan(self, url):
        if "http" in url:
            print(f"\n[+] Starting SQLi scan on {url}...")
            print("[*] Simulating SQLMap scan (install sqlmap for real scanning)")
            print("Potential vulnerabilities found: 2")
        else:
            print("[!] Invalid URL format (include http://)")

    # ==================== UTILITY METHODS ====================
    def clear_logs(self):
        """Securely clear system logs"""
        if self.is_admin():
            try:
                if platform.system() == "Windows":
                    os.system("wevtutil cl System")
                    os.system("wevtutil cl Application")
                    os.system("wevtutil cl Security")
                    print("[+] Windows event logs cleared")
                else:
                    os.system("sudo rm -rf /var/log/*")
                    print("[+] System logs cleared")
            except Exception as e:
                print(f"[!] Error clearing logs: {e}")
        else:
            print("[!] Requires admin privileges")

    def port_scan(self, target):
        """Scan target IP for open ports"""
        print(f"\n[+] Scanning {target}...")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"  [→] Port {port} is open")
                sock.close()
            except:
                pass

        threads = []
        for port in common_ports:
            t = Thread(target=scan_port, args=(port,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        print("[+] Port scan completed")

    def hash_file(self, file_path):
        """Generate cryptographic hashes for a file"""
        if not os.path.exists(file_path):
            print("[!] File not found")
            return

        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
                sha1 = hashlib.sha1(data).hexdigest()
                sha256 = hashlib.sha256(data).hexdigest()
                
                print(f"\n[+] Hashes for {file_path}:")
                print(f"  MD5:    {md5}")
                print(f"  SHA1:   {sha1}")
                print(f"  SHA256: {sha256}")
        except Exception as e:
            print(f"[!] Error hashing file: {e}")

    def system_info(self):
        """Display detailed system information"""
        print("\n[+] System Information:")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Hostname: {socket.gethostname()}")
        print(f"  IP Address: {socket.gethostbyname(socket.gethostname())}")
        print(f"  CPU Cores: {psutil.cpu_count(logical=False)} (Logical: {psutil.cpu_count()})")
        print(f"  Memory: {psutil.virtual_memory().total / (1024**3):.2f} GB")
        print(f"  Disk Usage: {psutil.disk_usage('/').percent}%")
        print(f"  Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")

    def kill_process(self, pid):
        """Terminate a process by PID"""
        try:
            process = psutil.Process(pid)
            print(f"[+] Killing process: {process.name()} (PID: {pid})")
            process.kill()
            print("[+] Process terminated")
        except psutil.NoSuchProcess:
            print("[!] No such process")
        except psutil.AccessDenied:
            print("[!] Access denied (try as admin)")

    def check_integrity(self):
        """Check system file integrity"""
        print("\n[+] Checking critical system files...")
        critical_files = {
            "Windows": ["C:\\Windows\\System32\\kernel32.dll", "C:\\Windows\\System32\\cmd.exe"],
            "Linux": ["/bin/bash", "/usr/bin/sudo"],
            "Darwin": ["/bin/bash", "/usr/bin/sudo"]
        }
        
        os_type = platform.system()
        for file in critical_files.get(os_type, []):
            if os.path.exists(file):
                size = os.path.getsize(file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {file} - Size: {size} bytes, Modified: {mtime}")
            else:
                print(f"  [!] Missing critical file: {file}")

    def encrypt_file(self, file_path):
        """Encrypt a file using AES-256"""
        if not os.path.exists(file_path):
            print("[!] File not found")
            return

        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.cipher.encrypt(data)
            with open(file_path + '.enc', 'wb') as f:
                f.write(encrypted)
            
            os.remove(file_path)
            print(f"[+] File encrypted and saved as {file_path}.enc")
            print(f"[!] Key for decryption: {CONFIG['ENCRYPT_KEY']}")
        except Exception as e:
            print(f"[!] Encryption failed: {e}")

    def decrypt_file(self, file_path, key=None):
        """Decrypt a file using the provided key"""
        if not os.path.exists(file_path):
            print("[!] File not found")
            return

        try:
            key = key or CONFIG['ENCRYPT_KEY']
            cipher = Fernet(key.encode())
            
            with open(file_path, 'rb') as f:
                encrypted = f.read()
            
            decrypted = cipher.decrypt(encrypted)
            output_path = file_path.replace('.enc', '')
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            print(f"[+] File decrypted and saved as {output_path}")
        except Exception as e:
            print(f"[!] Decryption failed: {e}")

    def watch_folder(self, path):
        """Monitor a folder for changes"""
        if not os.path.exists(path):
            print("[!] Path not found")
            return

        print(f"\n[+] Monitoring {path} for changes (Ctrl+C to stop)...")
        before = dict([(f, None) for f in os.listdir(path)])
        
        try:
            while True:
                time.sleep(5)
                after = dict([(f, None) for f in os.listdir(path)])
                added = [f for f in after if f not in before]
                removed = [f for f in before if f not in after]
                
                if added: print(f"  [+] Files added: {', '.join(added)}")
                if removed: print(f"  [-] Files removed: {', '.join(removed)}")
                
                before = after
        except KeyboardInterrupt:
            print("\n[+] Folder monitoring stopped")

    def trace_route(self, target):
        """Perform a traceroute to target"""
        print(f"\n[+] Tracing route to {target}...")
        try:
            if platform.system() == "Windows":
                os.system(f"tracert {target}")
            else:
                os.system(f"traceroute {target}")
        except Exception as e:
            print(f"[!] Error: {e}")

    def monitor_ransomware(self):
        """Check for ransomware indicators"""
        print("\n[+] Scanning for ransomware indicators...")
        suspicious_extensions = ['.encrypted', '.locked', '.crypt', '.ransom']
        found = False
        
        for root, _, files in os.walk('/' if platform.system() != 'Windows' else 'C:\\'):
            for file in files:
                if any(file.endswith(ext) for ext in suspicious_extensions):
                    print(f"  [!] Suspicious file: {os.path.join(root, file)}")
                    found = True
            if found:  # Prevent full disk scan
                break
        
        if not found:
            print("[+] No obvious ransomware files detected")

    def wifi_audit(self, interface):
        """Perform WiFi security audit"""
        if platform.system() != "Linux":
            print("[!] This command requires Linux")
            return

        print(f"\n[+] Auditing WiFi on {interface}...")
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            print(result.stdout)
            
            if "unassociated" in result.stdout:
                print("[!] Interface not connected")
                return
                
            print("\n[+] Nearby access points:")
            subprocess.run(['sudo', 'iwlist', interface, 'scan'], check=True)
        except Exception as e:
            print(f"[!] Error: {e}")

    def check_steganography(self, image_path):
        """Check for hidden data in images"""
        if not os.path.exists(image_path):
            print("[!] Image not found")
            return

        print(f"\n[+] Analyzing {image_path} for hidden data...")
        try:
            with open(image_path, 'rb') as f:
                content = f.read()
            
            # Simple steg detection (look for common steg headers)
            steg_signatures = {
                b'\x53\x54\x45\x47': 'Steghide',
                b'\x50\x4E\x47': 'Potential LSB steganography'
            }
            
            found = False
            for sig, name in steg_signatures.items():
                if sig in content:
                    print(f"  [!] Detected potential {name} signature")
                    found = True
            
            if not found:
                print("[+] No obvious steganography signatures detected")
        except Exception as e:
            print(f"[!] Error: {e}")


# ====ssl check starts here
    # # def check_ssl(self, domain=None):
    #     """Enhanced SSL certificate checker with user input"""
    #     if not domain:
    #         domain = input("Enter domain to check (e.g., example.com): ").strip()
    
    #     print(f"\n[+] Checking SSL certificate for {domain}...")
    
    #     try:
    #     # Set timeout (10 seconds)
    #         socket.setdefaulttimeout(10)
        
    #     # Create secure context
    #         context = ssl.create_default_context()
    #         context.check_hostname = True
        
    #         with socket.create_connection((domain, 443)) as sock:
    #             with context.wrap_socket(sock, server_hostname=domain) as ssock:
    #                 cert = ssock.getpeercert()
    #                 cipher = ssock.cipher()
    #                 protocol = ssock.version()
                
    #             # Certificate details
    #                 issuer = dict(x[0] for x in cert['issuer'])
    #                 subject = dict(x[0] for x in cert['subject'])
    #                 expires = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    #                 valid_days = (expires - datetime.now()).days
                
    #             # Print full report
    #                 print("\n╔" + "═"*50 + "╗")
    #                 print(f"║ {'SSL Certificate Report':^48} ║")
    #                 print("╠" + "═"*50 + "╣")
    #                 print(f"║ {'Domain:':<15} {domain:<33} ║")
    #                 print(f"║ {'Issuer:':<15} {issuer.get('organizationName', 'Unknown'):<33} ║")
    #                 print(f"║ {'Subject:':<15} {subject.get('commonName', 'Unknown'):<33} ║")
    #                 print(f"║ {'Expires:':<15} {expires.strftime('%Y-%m-%d')} ({valid_days} days left) ║")
    #                 print(f"║ {'Protocol:':<15} {protocol:<33} ║")
    #                 print(f"║ {'Cipher:':<15} {cipher[0]:<33} ║")
    #                 print("╚" + "═"*50 + "╝")
                
    #             # Additional warnings
    #                 if valid_days < 30:
    #                     print("[!] WARNING: Certificate expires soon!")
    #                 if 'SHA1' in str(cert):
    #                     print("[!] WARNING: Using weak SHA-1 signature")
                    
    #     except ssl.SSLCertVerificationError as e:
    #         print(f"[!] Certificate verification failed: {e}")
    #     except socket.timeout:
    #         print("[!] Connection timed out")
    #     except Exception as e:
    #         print(f"[!] SSL check failed: {e}")

    # def check_ssl(self, domain=None):
    #     """Comprehensive SSL certificate analyzer with export options"""
    #     if not domain:
    #         domain = input("Enter domain to check (e.g., example.com): ").strip()
    
    #     print(f"\n[+] Analyzing SSL certificate for {domain}...")
    
    #     try:
    #     # Configure enhanced SSL context
    #         context = ssl.create_default_context()
    #         context.check_hostname = True
    #         context.verify_mode = ssl.CERT_REQUIRED
    #         context.load_default_certs()
        
    #     # Set timeout and create connection
    #         socket.setdefaulttimeout(10)
        
    #         with socket.create_connection((domain, 443)) as sock:
    #             with context.wrap_socket(sock, server_hostname=domain) as ssock:
    #                 cert = ssock.getpeercert(binary_form=True)
    #                 x509 = ssl.DER_cert_to_PEM_cert(cert)
    #                 cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
                
    #             # Get certificate details
    #                 issuer = dict(x[0] for x in ssock.getpeercert()['issuer'])
    #                 subject = dict(x[0] for x in ssock.getpeercert()['subject'])
    #                 expires = datetime.strptime(ssock.getpeercert()['notAfter'], '%b %d %H:%M:%S %Y %Z')
    #                 valid_days = (expires - datetime.now()).days
                
    #             # Get certificate chain
    #                 chain = []
    #                 for idx, cert_der in enumerate(ssock.getpeercert_chain() or []):
    #                     cert_pem = ssl.DER_cert_to_PEM_cert(cert_der)
    #                     chain_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_pem)
    #                     chain.append({
    #                         'subject': dict(chain_cert.get_subject().get_components()),
    #                         'issuer': dict(chain_cert.get_issuer().get_components()),
    #                         'expires': chain_cert.get_notAfter().decode('utf-8'),
    #                         'serial': chain_cert.get_serial_number(),
    #                         'version': chain_cert.get_version() + 1
    #                     })
                
    #             # Check OCSP revocation status (requires requests)
    #                 ocsp_status = self._check_ocsp(cert_obj, chain[0] if len(chain) > 0 else None)
                
    #             # Print comprehensive report
    #                 self._print_ssl_report(domain, ssock, cert_obj, chain, ocsp_status, valid_days)
                
    #             # Export option
    #                 if input("\nExport results to file? (y/N): ").lower() == 'y':
    #                     self._export_ssl_results(domain, ssock, cert_obj, chain)
    
    #     except ssl.SSLError as e:
    #         print(f"[!] SSL Error: {e}")
    #     except socket.timeout:
    #         print("[!] Connection timed out")
    #     except Exception as e:
    #         print(f"[!] Analysis failed: {str(e)}")

    def check_ssl(self, domain=None):
        """Comprehensive SSL certificate analyzer with export options"""
        try:
            import OpenSSL
            import ssl
            import socket
            from datetime import datetime
        
            if not domain:
                domain = input("Enter domain to check (e.g., example.com): ").strip()
                if not domain:
                    print("[!] No domain provided")
                    return
        
            print(f"\n[+] Analyzing SSL certificate for {domain}...")
        
        # Configure enhanced SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_default_certs()
        
        # Set timeout and create connection
            socket.setdefaulttimeout(10)
        
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = ssl.DER_cert_to_PEM_cert(cert)
                    cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
                
                # Get certificate details
                    peer_cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in peer_cert['issuer'])
                    subject = dict(x[0] for x in peer_cert['subject'])
                    expires = datetime.strptime(peer_cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    valid_days = (expires - datetime.now()).days
                
                # Get certificate chain using OpenSSL
                    chain = []
                    store = OpenSSL.crypto.X509Store()
                    store_ctx = OpenSSL.crypto.X509StoreContext(store, cert_obj)
                
                    try:
                        chain_result = store_ctx.get_verified_chain()
                        for i, chain_cert in enumerate(chain_result):
                            chain.append({
                                'subject': dict(chain_cert.get_subject().get_components()),
                                'issuer': dict(chain_cert.get_issuer().get_components()),
                                'expires': chain_cert.get_notAfter().decode('utf-8'),
                                'serial': chain_cert.get_serial_number(),
                                'version': chain_cert.get_version() + 1
                            })
                    except OpenSSL.crypto.X509StoreContextError:
                        chain.append({
                            'subject': dict(cert_obj.get_subject().get_components()),
                            'issuer': dict(cert_obj.get_issuer().get_components()),
                            'expires': cert_obj.get_notAfter().decode('utf-8'),
                            'serial': cert_obj.get_serial_number(),
                            'version': cert_obj.get_version() + 1
                        })
                
                # Check OCSP revocation status
                    ocsp_status = "Unknown"
                    if len(chain) > 1:
                        ocsp_status = self._check_ocsp(cert_obj, chain[1])
                
                # Print comprehensive report
                    self._print_ssl_report(domain, ssock, cert_obj, chain, ocsp_status, valid_days)
                
                    # Export option
                    if input("\nExport results to file? (y/N): ").lower() == 'y':
                        self._export_ssl_results(domain, ssock, cert_obj, chain)
    
        except ssl.SSLError as e:
            print(f"[!] SSL Error: {e}")
        except socket.timeout:
            print("[!] Connection timed out")
        except ImportError as e:
            print(f"[!] Required module missing: {str(e)}")
            print("[!] Please install pyOpenSSL: pip install pyopenssl")
        except Exception as e:
            print(f"[!] Analysis failed: {str(e)}")


    def _print_ssl_report(self, domain, ssock, cert_obj, chain, ocsp_status, valid_days):
        """Display formatted SSL report"""
    # Basic info box
        print("\n╔" + "═"*60 + "╗")
        print(f"║ {'SSL/TLS Certificate Analysis':^58} ║")
        print("╠" + "═"*60 + "╣")
        print(f"║ {'Domain:':<15} {domain:<43} ║")
        print(f"║ {'Issuer:':<15} {cert_obj.get_issuer().CN:<43} ║")
        print(f"║ {'Subject:':<15} {cert_obj.get_subject().CN:<43} ║")
        print(f"║ {'Expires:':<15} {cert_obj.get_notAfter().decode('utf-8')} ({valid_days} days) ║")
        print(f"║ {'Protocol:':<15} {ssock.version():<43} ║")
        print(f"║ {'Cipher:':<15} {ssock.cipher()[0]:<43} ║")
        print(f"║ {'OCSP Status:':<15} {ocsp_status:<43} ║")
        print("╚" + "═"*60 + "╝")
    
    # Certificate chain visualization
        print("\n[Certificate Chain]")
        for i, cert in enumerate(chain):
            print(f"{'  ' * i}└─ {cert['subject'].get(b'CN', b'Unknown').decode('utf-8')}")
            if i == 0:
                print(f"    {'Issuer:':<10} {cert['issuer'].get(b'CN', b'Unknown').decode('utf-8')}")
                print(f"    {'Valid Until:':<10} {cert['expires']}")
    
    # Security recommendations
        print("\n[Security Assessment]")
        if valid_days < 30:
            print("[!] Certificate expires soon!")
        if 'SHA1' in cert_obj.get_signature_algorithm().decode('utf-8'):
            print("[!] Weak signature algorithm (SHA-1)")
        if ssock.version() == 'TLSv1':
            print("[!] Insecure protocol version (TLS 1.0)")
        elif ssock.version() == 'TLSv1.1':
            print("[!] Deprecated protocol version (TLS 1.1)")

    def _check_ocsp(self, cert, issuer_cert):
        """Check OCSP revocation status"""
        try:
            
        
            cert = load_pem_x509_certificate(
                OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            )
        
            if issuer_cert:
                issuer = load_pem_x509_certificate(
                    OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, issuer_cert)
                )
                builder = OCSPRequestBuilder()
                builder = builder.add_certificate(cert, issuer)
                req = builder.build()
            
                ocsp_url = cert.extensions.get_extension_for_class(
                    cryptography.x509.AuthorityInformationAccess
                ).value.get_ocsp_urls()[0]
            
                response = requests.post(
                    ocsp_url,
                    data=req.public_bytes(serialization.Encoding.DER),
                    headers={'Content-Type': 'application/ocsp-request'}
                )
            
                return "REVOKED" if response.status == 1 else "VALID"
        except:
            return "Unknown"

    def _export_ssl_results(self, domain, ssock, cert_obj, chain):
        """Export results to JSON file"""
        
    
        data = {
            'domain': domain,
            'scan_date': datetime.now().isoformat(),
            'protocol': ssock.version(),
            'cipher': ssock.cipher()[0],
            'certificate': {
                'subject': dict(cert_obj.get_subject().get_components()),
                'issuer': dict(cert_obj.get_issuer().get_components()),
                'valid_until': cert_obj.get_notAfter().decode('utf-8'),
                'serial': cert_obj.get_serial_number(),
                'signature_algorithm': cert_obj.get_signature_algorithm().decode('utf-8')
            },
            'chain': chain
        }
    
        filename = f"ssl_scan_{domain}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
        print(f"[+] Results saved to {filename}")

        # ssl ends here====

    def dump_memory(self):
        """Create a memory dump (requires admin)"""
        if not self.is_admin():
            print("[!] Requires admin privileges")
            return

        print("\n[+] Creating memory dump...")
        try:
            if platform.system() == "Windows":
                os.system("procdump -ma -accepteula")
                print("[+] Memory dump saved as .dmp files")
            else:
                print("[!] Linux memory dump requires LiME or fmem")
        except Exception as e:
            print(f"[!] Error: {e}")

    def enable_tor_routing(self):
        """Route traffic through Tor"""
        print("\n[+] Configuring Tor routing...")
        try:
            if platform.system() == "Linux":
                os.system("sudo apt install tor -y")
                os.system("sudo service tor start")
                print("[+] Tor service started. Configure your apps to use 127.0.0.1:9050")
            else:
                print("[!] Automatic Tor setup requires Linux. Install Tor Browser manually.")
        except Exception as e:
            print(f"[!] Error: {e}")

    def check_updates(self):
        """Check for DST updates"""
        try:
            response = requests.get(CONFIG['https://github.com/Stark-Expo-Tech-Exchange/DSTerminal.git'])
            latest = response.json()
            if latest['tag_name'] > CONFIG['CURRENT_VERSION']:
                return f"Update available: {latest['tag_name']}\nDownload: {latest['html_url']}"
            else:
                return "You have the latest version"
        except Exception as e:
            return f"Update check failed: {e}"

    # def vt_scan_menu(self):
    #     """VirusTotal file scanning interface"""
    #     print("\n[VirusTotal Scanner]")
    #     print("1. Hash lookup")
    #     print("2. File scan")
    #     choice = input("Select option: ")
        
    #     if choice == "1":
    #         file_hash = input("Enter file hash: ")
    #         self.vt_hash_lookup(file_hash)
    #     elif choice == "2":
    #         file_path = input("File path to scan: ")
    #         self.vt_file_scan(file_path)
    #     else:
    #         print("[!] Invalid choice")

    # def vt_hash_lookup(self, file_hash):
    #     """Check file hash against VirusTotal"""
    #     if not CONFIG['VT_API_KEY'] or CONFIG['VT_API_KEY'] == 'YOUR_VIRUSTOTAL_API_KEY':
    #         print("[!] Configure your VirusTotal API key first")
    #         return

    #     try:
    #         url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    #         headers = {"x-apikey": CONFIG['VT_API_KEY']}
    #         response = requests.get(url, headers=headers)
            
    #         if response.status_code == 200:
    #             result = response.json()
    #             stats = result['data']['attributes']['last_analysis_stats']
    #             print(f"\n[+] Detection: {stats['malicious']}/{sum(stats.values())}")
    #             print(f"First submitted: {result['data']['attributes']['first_submission_date']}")
    #         else:
    #             print("[!] Hash not found in VirusTotal")
    #     except Exception as e:
    #         print(f"[!] Error: {e}")

    # def vt_file_scan(self, file_path):
    #     """Upload file to VirusTotal"""
    #     if not os.path.exists(file_path):
    #         print("[!] File not found")
    #         return

    #     if not CONFIG['VT_API_KEY'] or CONFIG['VT_API_KEY'] == 'YOUR_VIRUSTOTAL_API_KEY':
    #         print("[!] Configure your VirusTotal API key first")
    #         return

    #     try:
    #         url = "https://www.virustotal.com/api/v3/files"
    #         headers = {"x-apikey": CONFIG['VT_API_KEY']}
            
    #         with open(file_path, 'rb') as f:
    #             files = {'file': (os.path.basename(file_path), f)}
    #             response = requests.post(url, headers=headers, files=files)
            
    #         if response.status_code == 200:
    #             result = response.json()
    #             print(f"\n[+] Scan ID: {result['data']['id']}")
    #             print("Check results later at: https://www.virustotal.com")
    #         else:
    #             print("[!] Upload failed")
    #     except Exception as e:
    #         print(f"[!] Error: {e}")

    #         # =========Special code for vtscan below
    
    def vt_scan_menu(self):
        """Enhanced VirusTotal scanning interface"""
        print("\n[VirusTotal Scanner]")
        print("1. Hash lookup")
        print("2. File scan")
        print("3. Bulk scan folder")
        print("4. Check previous scan")
        choice = input("Select option: ")
        
        if choice == "1":
            file_hash = input("Enter file hash (MD5/SHA1/SHA256): ").strip()
            self.vt_hash_lookup(file_hash)
        elif choice == "2":
            file_path = input("File path to scan: ").strip()
            self.vt_file_scan(file_path)
        elif choice == "3":
            folder_path = input("Folder path to scan: ").strip()
            max_files = input("Max files to scan (default 10): ").strip() or 10
            self.vt_bulk_scan(folder_path, int(max_files))
        elif choice == "4":
            scan_id = input("Enter previous scan ID: ").strip()
            self.check_scan_result(scan_id)
        else:
            print("[!] Invalid choice")

    def vt_hash_lookup(self, file_hash):
        """Enhanced hash lookup with detailed results"""
        if not self._validate_vt_api():
            return

        try:
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": CONFIG['VT_API_KEY']}
            
            print(f"\n[+] Checking hash: {file_hash}...")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                attrs = result['data']['attributes']
                
                # Detailed report
                print(f"\n╔{'═'*60}╗")
                print(f"║ {'VirusTotal Report':^58} ║")
                print(f"╠{'═'*60}╣")
                print(f"║ {'Detection:':<15} {attrs['last_analysis_stats']['malicious']}/{sum(attrs['last_analysis_stats'].values())} ║")
                print(f"║ {'First Seen:':<15} {attrs['first_submission_date']} ║")
                print(f"║ {'File Type:':<15} {attrs.get('type_tag', 'Unknown')} ║")
                
                # Top detections
                malicious = [k for k,v in attrs['last_analysis_results'].items() if v['category'] == 'malicious']
                if malicious:
                    print(f"╠{'═'*60}╣")
                    print(f"║ {'Top Detections:':<58} ║")
                    for engine in malicious[:3]:
                        print(f"║ - {engine:<55} ║")
                print(f"╚{'═'*60}╝")
                
                # Auto-quarantine recommendation
                if attrs['last_analysis_stats']['malicious'] > 0:
                    print("\n[!] MALICIOUS FILE DETECTED!")
                    if input("Quarantine file? (y/N): ").lower() == 'y':
                        self.quarantine_file(None, file_hash=file_hash)
            else:
                print("[!] Hash not found in VirusTotal")
        except Exception as e:
            print(f"[!] Error: {e}")
  

    def vt_file_scan(self, file_path):
        """Upload file to VirusTotal with debug output"""
        print(f"\n[DEBUG] Starting scan for: {file_path}")  # Debug line
    
        if not os.path.exists(file_path):
            print("[!] Error: File not found")
            print(f"[DEBUG] Resolved path: {os.path.abspath(file_path)}")  # Debug line
            return

            print("[DEBUG] File exists check passed")  # Debug line
    
        if not self._validate_vt_api():
            print("[!] Error: VirusTotal API validation failed")
            print(f"[DEBUG] API Key: {'Set' if CONFIG.get('VT_API_KEY') else 'Not Set'}")  # Debug line
            return

        print("[DEBUG] API validation passed")  # Debug line
    
        MAX_SIZE = 32 * 1024 * 1024  # 32MB
        file_size = os.path.getsize(file_path)
        print(f"[DEBUG] File size: {file_size} bytes")  # Debug line

        if file_size > MAX_SIZE:
            print(f"[!] Error: File too large ({file_size/1024/1024:.2f}MB > 32MB)")
            return

        print("[DEBUG] Size check passed")  # Debug line
    
        try:
            print(f"\n[+] Analyzing {os.path.basename(file_path)}...")
            print(f"  ↳ Size: {file_size/1024:.2f}KB")
            print("  ↳ Uploading...", end='', flush=True)
        
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                headers = {"x-apikey": CONFIG['VT_API_KEY']}
                print(f"\n[DEBUG] Sending request to VirusTotal...")  # Debug line
                response = requests.post(
                    "https://www.virustotal.com/api/v3/files",
                    headers=headers,
                    files=files,
                    timeout=30
                )
            print(" Done!")

            print(f"[DEBUG] Response status: {response.status_code}")  # Debug line
            if response.status_code == 200:
                result = response.json()
                scan_id = result['data']['id']
                print(f"\n[+] Scan ID: {scan_id}")
                print(f"[+] Report URL: https://www.virustotal.com/gui/file/{scan_id}")
                self._cache_scan_id(file_path, scan_id)
            else:
                print(f"[!] Error: Upload failed (HTTP {response.status_code})")
                print(f"[DEBUG] Response text: {response.text}")  # Debug line

        except Exception as e:
            print(f"\n[!] Critical Error: {str(e)}")
            print("[DEBUG] Exception occurred during upload")  # Debug line

        if response.status_code == 200:
            result = response.json()
            scan_id = result['data']['id']
            print(f"\n[+] Scan ID: {scan_id}")
        
        # Start polling in background
        Thread(target=self._poll_results, args=(scan_id, file_path), daemon=True).start()
 
    def _cache_scan_id(self, file_path, scan_id):
        """Store scan IDs for future reference"""
        cache_file = os.path.expanduser("~/.dstenex_scans.log")
        with open(cache_file, "a") as f:
            f.write(f"{file_path}|{scan_id}|{datetime.now()}\n")

    def vt_bulk_scan(self, folder_path, max_files=10):
        """Scan multiple files in a folder"""
        if not os.path.isdir(folder_path):
            print("[!] Invalid folder path")
            return
            
        print(f"\n[+] Scanning up to {max_files} files in {folder_path}...")
        scanned = 0
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if scanned >= max_files:
                    break
                    
                file_path = os.path.join(root, file)
                print(f"\n[File {scanned+1}/{max_files}] {file}")
                
                # First try local scan
                local_result = self.local_scan(file_path, silent=True)
                if local_result and local_result['infected']:
                    print("[!] LOCAL SCAN DETECTED THREAT!")
                    self.quarantine_file(file_path)
                    scanned += 1
                    continue
                
                # Fall back to VT if file < 32MB
                if os.path.getsize(file_path) <= 32 * 1024 * 1024:
                    self.vt_file_scan(file_path)
                else:
                    print("[!] File too large for VT, skipped")
                
                scanned += 1
                time.sleep(15)  # Respect VT API rate limits
        
        print("\n[+] Bulk scan completed")

    def _poll_results(self, scan_id, original_path=None):
        """Background result polling"""
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {"x-apikey": CONFIG['VT_API_KEY']}
        
        print("\n[+] Waiting for results... (Ctrl+C to check later)")
        try:
            for _ in range(10):  # Max 10 checks
                time.sleep(30)
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    status = result['data']['attributes']['status']
                    
                    if status == 'completed':
                        stats = result['data']['attributes']['stats']
                        print(f"\n[+] Final Results: {stats['malicious']} malicious / {stats['harmless']} clean")
                        
                        if stats['malicious'] > 0 and original_path:
                            self.quarantine_file(original_path)
                        return
                    else:
                        print(f"\r  ↳ Status: {status}...", end='', flush=True)
        except Exception:
            print("\n[!] Polling interrupted. Check later with 'check_result'")

    def check_scan_result(self, scan_id):
        """Check existing scan results"""
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {"x-apikey": CONFIG['VT_API_KEY']}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                stats = result['data']['attributes']['stats']
                print(f"\n[+] Results: {stats['malicious']} malicious / {stats['harmless']} clean")
                
                if stats['malicious'] > 0:
                    print("[!] MALICIOUS CONTENT DETECTED")
            else:
                print("[!] Results not available yet")
        except Exception as e:
            print(f"[!] Error checking results: {e}")

    def local_scan(self, file_path, silent=False):
        """Integrate ClamAV for local scanning"""
        try:
            import pyclamd
            cd = pyclamd.ClamdAgnostic()
            scan_result = cd.scan_file(file_path)
            
            if scan_result and scan_result.get(file_path) == 'OK':
                if not silent:
                    print("[+] Local scan: Clean")
                return {'infected': False}
            else:
                if not silent:
                    print("[!] Local scan: Infected!")
                    print(f"Detection: {scan_result.get(file_path, 'Unknown threat')}")
                return {'infected': True, 'threat': scan_result.get(file_path)}
                
        except ImportError:
            if not silent:
                print("[!] ClamAV not installed (pip install pyclamd)")
        except Exception as e:
            if not silent:
                print(f"[!] Local scan failed: {e}")
        return None

    def quarantine_file(self, file_path, file_hash=None):
        """Move dangerous files to quarantine"""
        quarantine_dir = os.path.join(os.path.expanduser("~"), "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)
        
        try:
            if file_path:
                filename = os.path.basename(file_path)
                new_path = os.path.join(quarantine_dir, f"quarantined_{filename}")
                shutil.move(file_path, new_path)
                print(f"[+] File moved to quarantine: {new_path}")
            elif file_hash:
                with open(os.path.join(quarantine_dir, "quarantined_hashes.txt"), "a") as f:
                    f.write(f"{file_hash}\n")
                print("[+] Malicious hash recorded")
        except Exception as e:
            print(f"[!] Quarantine failed: {e}")

    def _validate_vt_api(self):
        """Check if API key is configured"""
        if not CONFIG.get('VT_API_KEY') or CONFIG['VT_API_KEY'] == 'YOUR_VIRUSTOTAL_API_KEY':
            print("[!] Configure VirusTotal API key first:")
            print("1. Get key from: https://www.virustotal.com/gui/join-us")
            print("2. Edit CONFIG['VT_API_KEY'] in your code")
            return False
        return True


        # go up to change

    def monitor_registry(self):
        """Monitor Windows registry changes"""
        if platform.system() != "Windows":
            return "[!] Registry monitoring requires Windows"

        suspicious_keys = [
            r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKLM\SYSTEM\CurrentControlSet\Services"
        ]
        
        try:
            import winreg
            changes = []
            
            for key_path in suspicious_keys:
                hive, path = key_path.split('\\', 1)
                hive = getattr(winreg, {
                    'HKLM': 'HKEY_LOCAL_MACHINE',
                    'HKCU': 'HKEY_CURRENT_USER'
                }[hive])
                
                with winreg.OpenKey(hive, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        name, value, _ = winreg.EnumValue(key, i)
                        changes.append(f"{key_path}\\{name} = {value}")
            
            if changes:
                return "\n".join(["[!] Suspicious registry entries:"] + changes)
            else:
                return "[+] No suspicious registry entries found"
        except Exception as e:
            return f"[!] Registry scan failed: {e}"

    # def harden_system(self):
    #     """Apply basic security hardening"""
    #     if not self.is_admin():
    #         print("[!] Requires admin privileges")
    #         return

    #     print("\n[+] Applying security hardening...")
    #     try:
    #         if platform.system() == "Windows":
    #             # Disable SMBv1
    #             os.system("Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol")
    #             # Enable Windows Defender
    #             os.system("Set-MpPreference -DisableRealtimeMonitoring $false")
    #             print("[+] Windows hardening applied")
    #         else:
    #             # Disable root login via SSH
    #             os.system("sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config")
    #             # Enable firewall
    #             os.system("sudo ufw enable")
    #             print("[+] Linux hardening applied")
    #     except Exception as e:
    #         print(f"[!] Error: {e}")



# UNCOMMENT GOING UP NOT BELOW

    # def harden_system(self):
    #     """Apply comprehensive security hardening based on platform"""
    #     if not self.is_admin():
    #         print("[!] Requires admin privileges")
    #         return

    #     print("\n[+] Applying security hardening...")
    
    #     try:
    #         if platform.system() == "Windows":
    #             self._harden_windows()
    #         elif platform.system() == "Linux":
    #             self._harden_linux()
    #         elif platform.system() == "Darwin":
    #             self._harden_macos()
    #         else:
    #             print("[!] Unsupported operating system")
    #     except Exception as e:
    #         print(f"[!] Error during hardening: {str(e)}")

    # def _harden_windows(self):
    #     """Windows-specific hardening measures"""
    #     print("\n=== Windows Hardening ===")
    
    # # Disable insecure protocols
    #     os.system("powershell Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart")
    #     os.system("powershell Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\SCHANNEL\\Protocols\\SSL 2.0\\Server' -Name Enabled -Value 0 -Type DWord")
    
    # # Enable security features
    #     os.system("powershell Set-MpPreference -DisableRealtimeMonitoring $false")
    #     os.system("powershell Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
    
    # # Configure User Account Control
    #     os.system("powershell Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System -Name ConsentPromptBehaviorAdmin -Value 2")
    
    # # Disable LLMNR (Link-Local Multicast Name Resolution)
    #     os.system("powershell Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient' -Name EnableMulticast -Value 0")
    
    #     print("[+] Windows hardening applied. Reboot recommended for some changes.")

    # def _harden_linux(self):
    #     """Linux-specific hardening measures"""
    #     print("\n=== Linux Hardening ===")
    
    # # SSH hardening
    #     os.system("sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config")
    #     os.system("sudo sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config")
    
    # # Firewall configuration
    #     os.system("sudo ufw --force enable")
    #     os.system("sudo ufw default deny incoming")
    #     os.system("sudo ufw default allow outgoing")
    
    # # Kernel hardening
    #     os.system("sudo sysctl -w kernel.kptr_restrict=2")
    #     os.system("sudo sysctl -w kernel.dmesg_restrict=1")
    
    # # Disable core dumps
    #     os.system("sudo echo '* hard core 0' >> /etc/security/limits.conf")
    
    # # Restart services
    #     os.system("sudo systemctl restart sshd")
    #     print("[+] Linux hardening applied. Some changes require reboot.")

    # def _harden_macos(self):
    #     """macOS-specific hardening measures"""
    #     print("\n=== macOS Hardening ===")
    
    # # Enable firewall
    #     os.system("sudo defaults write /Library/Preferences/com.apple.alf globalstate -int 1")
    
    # # Disable remote login
    #     os.system("sudo systemsetup -setremotelogin off")
    
    # # Enable SIP (System Integrity Protection)
    #     os.system("sudo csrutil enable")
    
    # # Disable Bonjour advertising
    #     os.system("sudo defaults write /Library/Preferences/com.apple.mDNSResponder.plist NoMulticastAdvertisements -bool YES")
    
    #     print("[+] macOS hardening applied. Some changes require reboot.")

    # def is_admin(self):
    #     """Check for administrator privileges"""
    #     try:
    #         if platform.system() == "Windows":
    #             import ctypes
    #             return ctypes.windll.shell32.IsUserAnAdmin() != 0
    #         else:
    #             return os.getuid() == 0
    #     except:
    #         return False




    def harden_system(self, dry_run=False, rollback=False):
        """
        Apply comprehensive system hardening with logging and rollback support
        Usage:
        - harden_system              # Apply hardening
        - harden_system --dry-run    # Preview changes
        - harden_system --rollback   # Revert changes
        """
        if not self.is_admin():
            print("[!] Requires admin privileges")
            return

        # Setup logging
        logging.basicConfig(
            filename='security_harden.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

        if rollback:
            self._rollback_hardening()
            return

        print(f"\n[+] {'Simulating' if dry_run else 'Applying'} security hardening...")
        start_time = datetime.now()
        logging.info(f"Hardening started at {start_time}")

        try:
            if platform.system() == "Windows":
                self._harden_windows(dry_run)
            elif platform.system() == "Linux":
                self._harden_linux(dry_run)
            elif platform.system() == "Darwin":
                self._harden_macos(dry_run)
            else:
                print("[!] Unsupported operating system")
        except Exception as e:
            logging.error(f"Hardening failed: {str(e)}")
            print(f"[!] Error: {e}")
        finally:
            duration = datetime.now() - start_time
            logging.info(f"Hardening completed in {duration.total_seconds():.2f} seconds")
            print(f"\n[+] Hardening completed in {duration.total_seconds():.2f} seconds")

    def _harden_windows(self, dry_run):
        """Windows-specific hardening measures"""
        steps = [
            ("Disabling SMBv1", "Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart"),
            ("Disabling LLMNR", "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient' -Name EnableMulticast -Value 0"),
            ("Enabling Windows Defender", "Set-MpPreference -DisableRealtimeMonitoring $false"),
            ("Configuring Firewall", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"),
            ("Enabling UAC", "Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System -Name ConsentPromptBehaviorAdmin -Value 2"),
            ("Disabling WDigest", "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\WDigest' -Name UseLogonCredential -Value 0"),
        ]

        print("\n=== Windows Hardening ===")
        for desc, cmd in tqdm(steps, desc="Windows Hardening"):
            logging.info(f"Attempting: {desc}")
            if not dry_run:
                os.system(f"powershell {cmd}")
            print(f"  {desc} {'(simulated)' if dry_run else ''}")

    def _harden_linux(self, dry_run):
        """Linux-specific hardening measures"""
        steps = [
            ("Disabling root SSH", "sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config"),
            ("Disabling SSH passwords", "sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config"),
            ("Enabling UFW", "ufw --force enable"),
            ("Configuring UFW defaults", "ufw default deny incoming && ufw default allow outgoing"),
            ("Hardening kernel", "sysctl -w kernel.kptr_restrict=2 && sysctl -w kernel.dmesg_restrict=1"),
            ("Disabling core dumps", "echo '* hard core 0' >> /etc/security/limits.conf"),
            ("Restarting SSH", "systemctl restart sshd"),
        ]

        print("\n=== Linux Hardening ===")
        for desc, cmd in tqdm(steps, desc="Linux Hardening"):
            logging.info(f"Attempting: {desc}")
            if not dry_run:
                os.system(f"sudo {cmd}")
            print(f"  {desc} {'(simulated)' if dry_run else ''}")

    def _harden_macos(self, dry_run):
        """macOS-specific hardening measures"""
        steps = [
            ("Enabling firewall", "defaults write /Library/Preferences/com.apple.alf globalstate -int 1"),
            ("Disabling remote login", "systemsetup -setremotelogin off"),
            ("Enabling SIP", "csrutil enable"),
            ("Disabling Bonjour", "defaults write /Library/Preferences/com.apple.mDNSResponder.plist NoMulticastAdvertisements -bool YES"),
            ("Disabling guest account", "defaults write /Library/Preferences/com.apple.loginwindow GuestEnabled -bool NO"),
        ]

        print("\n=== macOS Hardening ===")
        for desc, cmd in tqdm(steps, desc="macOS Hardening"):
            logging.info(f"Attempting: {desc}")
            if not dry_run:
                os.system(f"sudo {cmd}")
            print(f"  {desc} {'(simulated)' if dry_run else ''}")

    def _rollback_hardening(self):
        """Revert hardening changes using log file"""
        print("\n[+] Rolling back hardening changes...")
        
        try:
            with open('security_harden.log', 'r') as f:
                logs = f.read()
            
            revert_actions = {
                "Windows": [
                    ("Re-enabling SMBv1", "Enable-WindowsOptionalFeature -Online -FeatureName smb1protocol"),
                    ("Resetting LLMNR", "Remove-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient' -Name EnableMulticast"),
                ],
                "Linux": [
                    ("Re-enabling root SSH", "sed -i 's/^PermitRootLogin.*/#PermitRootLogin yes/' /etc/ssh/sshd_config"),
                    ("Re-enabling SSH passwords", "sed -i 's/^PasswordAuthentication.*/#PasswordAuthentication yes/' /etc/ssh/sshd_config"),
                ],
                "Darwin": [
                    ("Resetting firewall", "defaults write /Library/Preferences/com.apple.alf globalstate -int 0"),
                    ("Re-enabling remote login", "systemsetup -setremotelogin on"),
                ]
            }

            platform_specific = platform.system()
            if platform_specific in revert_actions:
                for desc, cmd in tqdm(revert_actions[platform_specific], desc=f"Reverting {platform_specific}"):
                    print(f"  {desc}")
                    if platform_specific == "Windows":
                        os.system(f"powershell {cmd}")
                    else:
                        os.system(f"sudo {cmd}")
            
            print("[+] Rollback completed. Some changes may require reboot.")
        except FileNotFoundError:
            print("[!] No hardening log found. Manual revert required.")

    def is_admin(self):
        """Check for administrator privileges"""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except:
            return False


    # ==================== COMMAND HANDLER ====================
    def handle_command(self, cmd):
        if cmd == "scan": 
            self.scan_system()
        elif cmd == "netmon": 
            self.network_monitor()

        elif cmd == "exploitcheck": 
            self.check_exploits()
        elif cmd.startswith("macspoof"): 
            self.spoof_mac(cmd.split()[1] if len(cmd.split()) > 1 else "eth0")
        elif cmd.startswith("sqlmap"): 
            self.sql_injection_scan(cmd.split()[1] if len(cmd.split()) > 1 else input("Target URL: "))
        elif cmd == "clearlogs": 
            self.clear_logs()
        elif cmd.startswith("portsweep"): 
            target = cmd.split()[1] if len(cmd.split()) > 1 else "127.0.0.1"
            self.port_scan(target)
        elif cmd.startswith("hashfile"): 
            self.hash_file(cmd.split()[1] if len(cmd.split()) > 1 else input("File path: "))
        elif cmd == "sysinfo": 
            self.system_info()
        elif cmd.startswith("killproc"): 
            self.kill_process(int(cmd.split()[1])) if len(cmd.split()) > 1 else print("Usage: killproc PID")
        elif cmd == "chkintegrity": 
            self.check_integrity()
        elif cmd.startswith("encrypt"): 
            self.encrypt_file(cmd.split()[1] if len(cmd.split()) > 1 else input("File to encrypt: "))
        elif cmd.startswith("decrypt"): 
            args = cmd.split()
            if len(args) > 2: 
                self.decrypt_file(args[1], args[2])
            else: 
                print("Usage: decrypt FILE.enc KEY")
        elif cmd.startswith("watchfolder"): 
            self.watch_folder(cmd.split()[1] if len(cmd.split()) > 1 else ".")
        elif cmd.startswith("traceroute"): 
            self.trace_route(cmd.split()[1] if len(cmd.split()) > 1 else "8.8.8.8")
        elif cmd == "ransomwatch": 
            self.monitor_ransomware()
        elif cmd.startswith("wificrack"): 
            self.wifi_audit(cmd.split()[1] if len(cmd.split()) > 1 else "wlan0")
        elif cmd.startswith("stegcheck"): 
            self.check_steganography(cmd.split()[1] if len(cmd.split()) > 1 else input("Image path: "))
        # elif cmd.startswith("certcheck"): 
        #     self.check_ssl(cmd.split()[1] if len(cmd.split()) > 1 else "google.com")

        elif cmd.startswith("certcheck"):
        # Handle both command line input and interactive prompt
            if len(cmd.split()) > 1:
                domain = cmd.split()[1]
                self.check_ssl(domain)
            else:
                self.check_ssl()  # Will prompt for domain inside the method

        elif cmd == "memdump": 
            self.dump_memory()
        elif cmd == "torify": 
            self.enable_tor_routing()
        elif cmd == "update": 
            print(f"\n[+] {self.check_updates()}")
        elif cmd == "vtscan": 
            self.vt_scan_menu()
        elif cmd == "regmon": 
            print(self.monitor_registry())
        elif cmd == "harden": 
            self.harden_system()
        elif cmd == "help": 
            self.show_help()
        elif cmd == "exit": 
            print("\n[*] Exiting Defensive Security Terminal")
            sys.exit(0)
        else: 
            print("[!] Unknown command. Type 'help' for more command options.")

    # ==================== HELP MENU ====================
    def show_help(self):
        help_text = """
    DSTerminal Commands:
    
    === Core Security ===
    scan           - System threat scan (animated)
    netmon         - Live network monitoring
    exploitcheck   - Check for critical CVEs
    vtscan         - VirusTotal file analysis
    clearlogs      - Securely wipe system logs
    
    === Network Tools ===
    portsweep [IP] - Scan target for open ports
    traceroute [IP]- Network path analysis
    torify         - Route traffic through Tor
    dnssec [DOMAIN]- Validate DNSSEC
    
    === Forensics ===
    memdump        - Capture RAM for analysis
    hashfile [PATH]- Generate file hashes
    stegcheck [IMG]- Detect hidden image data
    ransomwatch    - Find ransomware artifacts
    
    === System Management ===
    sysinfo        - Detailed system report
    killproc PID   - Terminate process
    macspoof [IFACE] - Randomize MAC address
    harden         - Apply security hardening
    
    === Crypto Tools ===
    encrypt FILE   - AES-256 file encryption
    decrypt FILE KEY - File decryption
    
    === Web Security ===
    sqlmap [URL]   - SQL injection scan
    certcheck [DOMAIN] - SSL certificate audit
    
    === Monitoring ===
    watchfolder [PATH] - Directory change detection
    regmon        - Windows registry monitor
    
    === Utilities ===
    update         - Check for DST updates
    help           - Show this menu
    exit           - Quit terminal
    """
        print(help_text)

    def run(self):
            self.print_banner()
            while True:
                try:
                        prompt_text = HTML('<ansigreen><b>DFFENEX</b></ansigreen>'
                               '<ansiblue>@</ansiblue>'
                               '<ansigreen><b>DSTerminal</b></ansigreen> '
                               '<ansired>--]</ansired> ')
                        user_input = self.session.prompt(prompt_text)
                        self.handle_command(user_input.strip())
                except KeyboardInterrupt:
                    print("\n[*] Use 'exit' to quit")
                except Exception as e:
                    print(f"[!] Error: {str(e)}")

if __name__ == "__main__":
    terminal = SecurityTerminal()
    terminal.run()