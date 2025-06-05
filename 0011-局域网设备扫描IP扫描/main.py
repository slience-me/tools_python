# Author: slience_me
# Date: 2025/6/5 11:25
# Blog: https://slienceme.cn
import socket
import concurrent.futures
import ipaddress

# 设置你局域网网段，例如 192.168.1.0/24
NETWORK = '192.168.3.0/24'
TIMEOUT = 60  # 秒

# 尝试连接一个IP地址，返回是否在线以及主机名
def ping_ip(ip):
    try:
        ip_str = str(ip)
        socket.setdefaulttimeout(TIMEOUT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex((ip_str, 80))  # 尝试连接 HTTP 端口
            if result == 0:
                try:
                    hostname = socket.gethostbyaddr(ip_str)[0]
                except socket.herror:
                    hostname = 'Unknown'
                return (ip_str, True, hostname)
    except Exception:
        pass
    return (str(ip), False, None)

def scan_network(network):
    net = ipaddress.ip_network(network, strict=False)
    alive_hosts = []

    print(f"[+] 正在扫描局域网：{network} ...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(ping_ip, ip): ip for ip in net.hosts()}
        for future in concurrent.futures.as_completed(futures):
            ip_str, is_up, hostname = future.result()
            if is_up:
                print(f"[+] 主机在线: {ip_str} - 主机名: {hostname}")
                alive_hosts.append((ip_str, hostname))

    print(f"[+] 扫描完成，共发现 {len(alive_hosts)} 台设备在线。")
    return alive_hosts

if __name__ == '__main__':
    scan_network(NETWORK)
