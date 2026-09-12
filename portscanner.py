from scapy.all import IP, ICMP, TCP, sr1, send
import sys, time

def check_host_up(host_ip):
    icmp_request = IP(dst=host_ip)/ICMP()
    icmp_response = sr1(icmp_request, timeout=2, verbose=0)
    if icmp_response and icmp_response.haslayer(ICMP) and icmp_response.getlayer(ICMP).type == 0:
        print(f"Host {host_ip} is up. Response: {icmp_response.summary()}")
        return True
    return False

def scan_ports(host_ip, port_range):
    start_port, end_port = port_range
    open_ports = []
    print(f"Scanning ports {start_port} to {end_port} for {host_ip}...")
    for port in range(start_port, end_port + 1):
        tcp_syn_packet = IP(dst=host_ip)/TCP(dport=port, flags='S')
        scan_response = sr1(tcp_syn_packet, timeout=1, verbose=0)
        if scan_response is None:
            print(f"Port {port} is closed or filtered.")
        elif scan_response.haslayer(TCP) and (scan_response.getlayer(TCP).flags & 0x12 == 0x12): #SYN-ACK
            print(f"Port {port} is open.")
            open_ports.append(port)
            # Send RST to close the connection
            rst_packet = IP(dst=host_ip)/TCP(dport=port, flags='R')
            send(rst_packet, verbose=0)
        elif scan_response.haslayer(TCP) and (scan_response.getlayer(TCP).flags & 0x04 == 0x04): #RST
            print(f"Port {port} is closed.")
    return open_ports

def main():
    if len(sys.argv) < 2:
        print("Please specify the IP address of the host you wish to scan.")
        sys.exit(1)

    host_ip = sys.argv[1]  # Get the host IP from command line arguments
    if check_host_up(host_ip) == False:
        print(f"Host {host_ip} is down or not responding.")
        time.sleep(5)
        sys.exit(1)
    try:
        
        scan_well_known_ports = input("Do you wish to scan all well-known ports? ").strip().lower()
        scan_registered_ports = input("Do you wish to scan all registered ports? ").strip().lower()
        scan_ephemeral_ports = input("Do you wish to scan all ephemeral ports? ").strip().lower()
    
        open_ports = set()

        if scan_well_known_ports in ['yes', 'y']:
            print(f"Proceeding with port scan on {host_ip}...")
            time.sleep(1)
            open_well_known_ports =scan_ports(host_ip, port_range=(0, 1023))
            open_ports.update(open_well_known_ports)

        if scan_registered_ports in ['yes', 'y']:
            print(f"Proceeding with registered port scan on {host_ip}...")
            time.sleep(5)
            open_registered_ports = scan_ports(host_ip, port_range=(1024, 49151))
            open_ports.update(open_registered_ports)

        if scan_ephemeral_ports in ['yes', 'y']:
            print(f"Proceeding with ephemeral port scan on {host_ip}...")
            time.sleep(5)
            open_ephemeral_ports = scan_ports(host_ip, port_range=(49152, 65535))
            open_ports.update(open_ephemeral_ports)
        open_chosen_ports = []
        
        while True:
            chosen_port = input("Enter a specific port to scan (x to skip): ")
            if chosen_port.lower() == 'x':
                break
            if chosen_port.isdigit():
                chosen_port = int(chosen_port)
                if 0 <= chosen_port <= 65535:
                    print(f"Scanning port {chosen_port} on {host_ip}...")
                    open_port = scan_ports(host_ip, port_range=(chosen_port, chosen_port))
                    if open_port:
                        open_chosen_ports.append(chosen_port)
                else:
                    print("Invalid port number")
        open_ports.update(open_chosen_ports)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"Open ports on {host_ip}: {sorted(open_ports)}")
        input("Press enter to exit the program...")



if __name__ == "__main__":
    main()