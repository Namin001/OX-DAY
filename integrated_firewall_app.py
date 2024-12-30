from flask import Flask, jsonify, render_template, request, send_from_directory
import psutil
import threading
import time
import socket
import os
import subprocess

app = Flask(__name__)
# Global variables to store the current network stats
network_stats = {
    'upload_speed': 0,
    'download_speed': 0,
    'total_data': 0,  # Placeholder for total data
    'vulnerability_score': 0
}

# Firewall rules
OPEN_PORTS = {8080, 9090}  # Set of ports to open
BLOCKED_PORTS = {5050, 6060}  # Set of ports to block

# Path to the firewall script
FIREWALL_SCRIPT = 'firewall.py'

# Function to run firewall.py in the background
def run_firewall():
    try:
        # Run firewall.py in the background using subprocess
        subprocess.Popen(['python3', FIREWALL_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Firewall script {FIREWALL_SCRIPT} is running.")
    except Exception as e:
        print(f"Error running firewall script: {e}")

def monitor_network_traffic():
    global network_stats
    net_io = psutil.net_io_counters()
    initial_bytes_sent = net_io.bytes_sent
    initial_bytes_received = net_io.bytes_recv
    initial_packets_sent = net_io.packets_sent
    initial_packets_received = net_io.packets_recv

    while True:
        time.sleep(1)
        net_io = psutil.net_io_counters()
        current_bytes_sent = net_io.bytes_sent
        current_bytes_received = net_io.bytes_recv
        current_packets_sent = net_io.packets_sent
        current_packets_received = net_io.packets_recv

        bytes_sent_per_sec = current_bytes_sent - initial_bytes_sent
        bytes_received_per_sec = current_bytes_received - initial_bytes_received
        packets_sent_per_sec = current_packets_sent - initial_packets_sent
        packets_received_per_sec = current_packets_received - initial_packets_received

        initial_bytes_sent = current_bytes_sent
        initial_bytes_received = current_bytes_received
        initial_packets_sent = current_packets_sent
        initial_packets_received = current_packets_received

        mb_sent_per_sec = bytes_sent_per_sec / (1024 * 1024)
        mb_received_per_sec = bytes_received_per_sec / (1024 * 1024)

        total_packets = packets_sent_per_sec + packets_received_per_sec
        vulnerability_score = calculate_vulnerability_score(mb_sent_per_sec, mb_received_per_sec)

        network_stats.update({
            'upload_speed': mb_sent_per_sec,
            'download_speed': mb_received_per_sec,
            'total_data': total_packets,
            'vulnerability_score': vulnerability_score
        })

def calculate_vulnerability_score(upload_speed, download_speed):
    base_score = 0
    high_speed_threshold = 10
    moderate_speed_threshold = 5

    if upload_speed > high_speed_threshold or download_speed > high_speed_threshold:
        base_score += 7
    elif upload_speed > moderate_speed_threshold or download_speed > moderate_speed_threshold:
        base_score += 4
    else:
        base_score += 1

    return min(base_score, 10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(network_stats)

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096)
        print(f"Received data: {request.decode('utf-8')}")
        client_socket.send("ACK".encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def open_port(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Port {port} is open and listening.")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def close_port(port):
    print(f"Port {port} is closed (simulated).")

@app.route('/open_port', methods=['POST'])
def api_open_port():
    data = request.json
    port = data.get('port')
    if port in OPEN_PORTS:
        threading.Thread(target=open_port, args=(port,), daemon=True).start()
        return jsonify({'message': f'Port {port} is now open.'}), 200
    else:
        return jsonify({'message': f'Port {port} is not in the allowed list.'}), 400

@app.route('/close_port', methods=['POST'])
def api_close_port():
    data = request.json
    port = data.get('port')
    if port in BLOCKED_PORTS:
        close_port(port)
        return jsonify({'message': f'Port {port} is now closed.'}), 200
    else:
        return jsonify({'message': f'Port {port} is not in the blocked list.'}), 400

@app.route('/notify')
def notify():
    return send_from_directory('static', 'notify.html')

if __name__ == '__main__':
    threading.Thread(target=monitor_network_traffic, daemon=True).start()
    
    # Run firewall script in background when app starts
    run_firewall()
    
    app.run(debug=True, host='0.0.0.0', port=5000)