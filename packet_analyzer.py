import socket
import struct
import sys
from datetime import datetime

def get_local_ip():
    """Get the local IP address automatically"""
    try:
        # Create a temporary socket to get local IP
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to Google DNS (doesn't actually send data)
            temp_sock.connect(("8.8.8.8", 80))
            local_ip = temp_sock.getsockname()[0]
        finally:
            temp_sock.close()
        return local_ip
    except Exception:
        return None

def main():
    try:
        # Get local IP automatically
        local_ip = get_local_ip()
        if not local_ip:
            print("\nERROR: Could not determine local IP address!")
            print("Please connect to a network and try again.")
            return

        print(f"\nDetected local IP: {local_ip}")
        
        # Create raw socket for Windows
        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        
        # Bind to local IP
        conn.bind((local_ip, 0))
        
        # Include IP headers
        conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        # Enable promiscuous mode
        try:
            conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except AttributeError:
            print("\nWARNING: Promiscuous mode not available on this system")
            print("You'll only see packets destined for your machine")
        
        print("\nPacket Sniffer Started (Ctrl+C to stop)\n")
        print("Timestamp           Source IP        Destination IP   Protocol  Size")
        print("-" * 80)
        
        while True:
            try:
                raw_data, addr = conn.recvfrom(65535)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Parse IP header (first 20 bytes)
                ip_header = raw_data[:20]
                iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                
                version_ihl = iph[0]
                ihl = version_ihl & 0xF
                iph_length = ihl * 4
                protocol = iph[6]
                src_ip = socket.inet_ntoa(iph[8])
                dest_ip = socket.inet_ntoa(iph[9])
                
                # TCP
                if protocol == 6:
                    print(f"{timestamp}  {src_ip:15}  {dest_ip:15}  TCP       {len(raw_data)} bytes")
                
                # UDP
                elif protocol == 17:
                    print(f"{timestamp}  {src_ip:15}  {dest_ip:15}  UDP       {len(raw_data)} bytes")
                
                # ICMP
                elif protocol == 1:
                    print(f"{timestamp}  {src_ip:15}  {dest_ip:15}  ICMP      {len(raw_data)} bytes")
                
                # Other
                else:
                    print(f"{timestamp}  {src_ip:15}  {dest_ip:15}  Other     {len(raw_data)} bytes")
            
            except socket.error as e:
                print(f"\nNetwork error: {e}")
                break
    
    except KeyboardInterrupt:
        print("\nStopping packet capture...")
    except PermissionError:
        print("\nERROR: Must run as Administrator!")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    finally:
        try:
            conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            conn.close()
        except:
            pass
        print("Packet capture stopped.")

if __name__ == "__main__":
    print("""
    =============================================
    NETWORK PACKET ANALYZER - EDUCATIONAL USE ONLY
    =============================================
    This tool will capture and display network packets.
    Use only on networks you own or have permission to monitor.
    Press Ctrl+C to stop.
    """)
    
    # Verify admin privileges
    try:
        main()
    except PermissionError:
        print("\nERROR: This program requires Administrator privileges!")
        print("Right-click Command Prompt and select 'Run as Administrator'")
