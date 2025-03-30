Made By Ratichubi <3


requirements: flask (pip install flask)
for new pip do: pip install flask --break-system-packages


command: python3 app.py
binded server: 127.0.0.1:5000 (localhost)
you can change bind of server with this: 
if __name__ == '__main__':
    app.run(port=5000)

Bind to another ip and port
if __name__ == '__main__':
    app.run(host='192.168.1.100', port=5000)
