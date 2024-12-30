import os
import time
from scapy.all import sniff, IP, TCP
import threading
import keyboard
import ml
from ml import *

# List of known malicious IPs or patternsq
malicious_ips = ml.main_function()

# Path to the file or process associated with the threat (simulated)
threat_file_path = "/path/to/malicious/file"
threat_process_name = "malicious_process"

# Function to close a port using iptables
def close_port(port):
    os.system(f"iptables -A INPUT -p tcp --dport {port} -j DROP")
    print(f"Port {port} has been closed!")

# Function to open a port using iptables
def open_port(port):
    os.system(f"iptables -D INPUT -p tcp --dport {port} -j DROP")
    print(f"Port {port} has been reopened!")

# Function to notify the user
def notify_user(message):
    print(f"ALERT: {message}")

# Function to remove the identified threat (e.g., delete a file)
def remove_threat():
    # Simulate threat removal by deleting a malicious file
    if os.path.exists(threat_file_path):
        os.remove(threat_file_path)
        notify_user(f"The malicious file {threat_file_path} has been removed.")
    else:
        notify_user(f"No malicious file found at {threat_file_path}.")

    # Simulate killing a malicious process
    os.system(f"pkill {threat_process_name}")
    notify_user(f"Any running process named '{threat_process_name}' has been terminated.")

# Function to handle threat mitigation and port reopening
def handle_threat(packet, port):
    ip_src = packet[IP].src
    ip_dst = packet[IP].dst
    notify_user(f"Detected malicious traffic from {ip_src} to {ip_dst} on port {port}.")
    close_port(port)

    # Remove the identified threat
    remove_threat()

    # Simulate a delay before reopening the port (e.g., 30 seconds)
    time.sleep(30)

    # Open the port after threat removal
    open_port(port)
    notify_user(f"The threat has been removed. Port {port} has been reopened.")

# Function to analyze packets
def analyze_packet(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        # Check if the source or destination IP is malicious
        if ip_src in malicious_ips or ip_dst in malicious_ips:
            # Identify the TCP layer to close the vulnerable port
            if TCP in packet:
                port = packet[TCP].dport
                handle_threat(packet, port)

# Function to start sniffing and monitoring network traffic
def start_firewall():
    print("Starting the firewall...")
    sniff(filter="tcp", prn=analyze_packet, store=0)

# Function to monitor for the termination key
def monitor_termination_key():
    while True:
        if keyboard.is_pressed('q'):  # Listen for the 'q' key
            os._exit(0)  # Terminate the script immediately

# Start the sniffing process in a separate thread
firewall_thread = threading.Thread(target=start_firewall)
firewall_thread.start()

# Start monitoring for the termination key in the main thread
monitor_termination_key()