import psutil
import time
import speedtest
import socket

# Function to get real-time upload and download speed
def get_network_speed():
    speed = speedtest.Speedtest()
    download_speed = speed.download() / 1_000_000  # convert to Mbps
    upload_speed = speed.upload() / 1_000_000  # convert to Mbps
    return download_speed, upload_speed

# Function to get total number of packets transferred
def get_total_packets():
    net_io = psutil.net_io_counters()
    return net_io.packets_sent, net_io.packets_recv

# Function to get number of open ports
def get_open_ports():
    open_ports = []
    for port in range(1, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex(('localhost', port)) == 0:
                open_ports.append(port)
    return open_ports

# Main function to gather all real-time metrics
def gather_metrics(interval=10):
    while True:
        # Gather speeds
        download_speed, upload_speed = get_network_speed()

        # Gather total packets
        packets_sent, packets_received = get_total_packets()

        # Gather open ports
        open_ports = get_open_ports()

        # Print real-time metrics
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Packets Sent: {packets_sent}")
        print(f"Packets Received: {packets_received}")
        print(f"Open Ports: {len(open_ports)}")

        # Wait for the specified interval before collecting again
        time.sleep(interval)

if __name__ == "__main__":
    gather_metrics()
