import pickle
import pandas as pd
import struct
import socket
import numpy as np
import input1
from input1 import *

# Function to load models and encoder
def load_models():
    with open('models/X_encoder.pkl', 'rb') as f: #enaku x_encoder.pkl
        x_label = pickle.load(f)            #unaku file path is
    with open('models/Class.pkl', 'rb') as f:      #add 'models/filename' for all models
        model2 = pickle.load(f)
    with open('models/SourceIP.pkl', 'rb') as f:
        model1 = pickle.load(f)
    return x_label, model2, model1

# Function to encode an IP address to an integer
def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

# Function to decode an integer back to an IP address
def int_to_ip(ip_int):
    return socket.inet_ntoa(struct.pack("!I", ip_int))

# Function to make predictions
def predict(flow_id, source_port, destination_ip, destination_port, protocol, timestamp, total_length_fwd_packets, x_label, model1, model2):
    new_data = pd.DataFrame({
        'Flow ID': [flow_id],
        'Source Port': [source_port],
        'Destination IP': [destination_ip],
        'Destination Port': [destination_port],
        'Protocol': [protocol],
        'Timestamp': [timestamp],
        'Total Length of Fwd Packets': [total_length_fwd_packets],
    })

    new_data["Destination IP"] = new_data["Destination IP"].apply(ip_to_int)
    new_data["Flow ID"] = x_label.fit_transform(new_data["Flow ID"])
    new_data["Timestamp"] = x_label.fit_transform(new_data["Timestamp"])
    array = np.array(new_data)

    y_pred = model1.predict(array)
    decoded_y1_pred = int_to_ip(y_pred[0])

    y1_pred = model2.predict(array)

    return y1_pred[0], decoded_y1_pred

def main_function():
    print(decoded_y1_pred)


x_label, model2, model1 = load_models()
    
_,decoded_y1_pred = predict(
        flow_id=input1.flow_id(),
        source_port=input1.src_port(),
        destination_ip=input1.dst_ip(),
        destination_port=input1.dst_port(),
        protocol=input1.protocol(),
        timestamp=input1.timestamp(),
        total_length_fwd_packets=input1.total_leng(),
        x_label=x_label,
        model1=model1,
        model2=model2
    )
main_function()




