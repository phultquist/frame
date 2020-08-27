import socket

# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)

def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

print(get_ip_address())
