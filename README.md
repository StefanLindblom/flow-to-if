flow-to-if
=========
Replay netflow/sflow captured data as regular IP traffic to a network interface

I was looking for a way to run snort or maltrail (or similar IDS's, intrusion detection system) - but on an already existing netflow or sflow collector.
There seems to be very limited support for doing this.
In my case, using nfdump (1.6.8p1) + nfsen (1.3.8).

One should of course be aware, that _full_ IDS capabilities cannot be expected with this setup, as you do not get the packets' payload when doing flow sampling.
This solution will mainly help with identifying attacks that can be tied to the 5-tuple.

The python script is not optimised in any special way, but it seems to do the job so far.

Usage
-----
- It is expected that you already have nfcap set up, in my case the destination directory is
    `/opt/nfsen/profiles-data/live/`

- Python 2.7 with scapy
    ```
    make_install pip
    pip install scapy
    ```
- file_monitor.sh needs to be running at all times (cronjob?), to detect new nfcap files. It depends on inotify-tools:
    `sudo apt-get install inotify-tools`

- file_monitor.sh will then trigger nfdump-to-packet.py, which will send the 5-tuple (so far only IPv4 TCP or UDP) to the configured network interface. In my case I set up a dummy interface called nfdump:
    ```
    sudo ip link add name nfdump type dummy
    sudo ifconfig nfdump up
    ```

Troubleshooting
---------------
- To verify that the file system monitoring is working properly, do the following in two separate shells:
   
    `./file_monitor.sh`

    `touch /opt/nfsen/profiles-data/live/nfcapd.2018123`

- To verify that nfdump-to-packet.py can create and send packets to the network interface, two shells again:
    `echo "2011,2012,garbage,10.10.10.10,20.20.20.20,55555,80,TCP" | python nfdump-to-packet.py -`

    `tcpdump -n -i nfdump ''`

