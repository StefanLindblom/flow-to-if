from scapy.all import *
import sys

# Set destination interface
dst_if = "nfdump"


try:
  s = conf.L2socket(iface=dst_if)

  for line in sys.stdin:
    row = line.split(',')

    # Only process IPv4
    if len(row[3]) >= 16:
      continue

    date_start = row[0]
    date_end = row[1]
    ip_src = row[3]
    ip_dst = row[4]
    port_src = row[5]
    port_dst = row[6]
    proto = row[7]

    if proto == 'TCP':
      packet = IP(src=ip_src, dst=ip_dst)/TCP(sport=int(port_src), dport=int(port_dst))/""
    elif proto == 'UDP':
      packet = IP(src=ip_src, dst=ip_dst)/UDP(sport=int(port_src), dport=int(port_dst))/""
    else:
      continue

    s.send(Ether()/packet)

except IOError, e:
    if e.errno == errno.EPIPE:
      print e
