from scapy.all import *
import re

# Function to process each captured packet
def process_packet(packet):
    if packet.haslayer(IP):  # Only process IP packets
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        print(f"[🌐] {src_ip} → {dst_ip}")

        if packet.haslayer(TCP) or packet.haslayer(UDP):
            payload = bytes(packet[TCP].payload) if packet.haslayer(TCP) else bytes(packet[UDP].payload)

            # Extract visited websites
            if packet.haslayer(Raw) and b"Host:" in payload:
                host = re.search(br"Host: (.+)", payload)
                if host:
                    print(f"  └─[🌍] Visited Website: {host.group(1).decode()}")

            # Extract possible usernames and passwords from HTTP
            if packet.haslayer(Raw) and (b"username" in payload or b"password" in payload):
                print("\n[🔓] Possible Credentials Found!")
                print(f"  └─[📜] Data: {payload.decode(errors='ignore')}\n")

# Start sniffing on wlan0 (WiFi) or eth0 (Ethernet)
print("[+] Sniffing network packets...")
sniff(prn=process_packet, store=False, iface="wlan0", filter="tcp")
