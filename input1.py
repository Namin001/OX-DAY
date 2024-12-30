from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime

def packet_callback(packet):
    if IP in packet:
        # Extracting flow information
        flow_id = f"{packet[IP].src}-{packet[IP].dst}-{packet[IP].proto}"
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport if TCP in packet else packet[UDP].sport
        dst_port = packet[TCP].dport if TCP in packet else packet[UDP].dport
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        protocol = packet[IP].proto
        total_length = len(packet[IP])

        print(f"Flow ID: {flow_id}")
        print(f"Destination IP: {dst_ip}")
        print(f"Source Port: {src_port}")
        print(f"Destination Port: {dst_port}")
        print(f"Timestamp: {timestamp}")
        print(f"Protocol: {protocol}")
        print(f"Total Length of Forward Packets: {total_length}")
        print("-" * 50)

# Start sniffing packets
sniff(prn=packet_callback, store=0)

def flow_id():
    return packet_callback.flow_id
def dst_ip():
    return packet_callback.dst_ip
def src_port():
    return packet_callback.src_port
def dst_port():
    return packet_callback.dst_port
def timestamp():
    return packet_callback.timestamp
def protocol():
    return packet_callback.protocol
def total_leng():
    return packet_callback.total_length
