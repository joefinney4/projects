# Packet Tracer Enterprise Network
### This project found me creating a simulated network in Cisco Packet Tracer, from scratch. This used the skills I'd learnt, regarding configuration, architectures, and best practices.
## Showcase
<img width="1006" height="623" alt="image" src="https://github.com/user-attachments/assets/7acc6158-353c-42ed-802d-6451045c2663" />

## Main Architecture:
-Uses a '3-tier' architecture with a core, distribution and access layer.  
-Dual-homed architecture with each core router connecting to a separate ISP router (due to limited interfaces on chosen routers - intention would've been dual-multihomed for full redundancy)  
-Serial Links used where needed due to interface constraints  
-3 OSPF areas used: Router0 and Router1 acting as ABRs.  
-VLANs 10,20,30,80,100 present.  
-2 servers: 1 internal, 1 external. The internal server holds internal DNS 'A' records, DHCP pools, email, syslog logs, and acts as the NTP & SNMP server.  
-2 multilayer switches act as the distribution layer - connected via a Layer 2 EtherChannel. These carry out inter-VLAN routing across all VLANs. 'Router-on-a-stick' has not been implemented.  
-A 2nd EtherChannel (using LAGP) is active between MultilayerSwitch2 and Switch2 to simulate 'high traffic demands' from VLAN30.  
-Wireless functionality has been implemented - although while facing infamous packet tracer issues with WLC connectivity. The solution was to 'ditch' lightweight AP architecture using a WLC-3504 and implementing an autonomous architecture using a Wireless Access Point per-VLAN. This works within the architecture due to its small size. I understand the limits with this and if there were to be expansion the expectation would be lightweight or cloud-based architecture.  
-All routing devices (routers and multilayer switches) are in a full-mesh architecture for redundancy. The access layer is in a partial mesh with the distribution layer.  
-RPVST+ has been used to allow quick recovery from link failure.  
-Subnetted using class C 192.168.0.0/16 network. Each VLAN is given its own /24 Block and point-to-point links use a /30, despite RFC 3021.  
-PAT / NAT Overload is used on Router0 and Router1 to conserve IPV4 addresses (and to simulate private IPs not being allowed across the internet).  
## Extra Features:
-VLAN100 contains a DMZ that holds the public facing 'external' server. This acts as a webserver that can be accessed by external hosts (PC12) using port forwarding on Router1.  
-VLAN10 is for 'Network Engineers'. Devices on this VLAN can SSH into network devices, but others can't due to ACLs.  
-Port Security, DAI and DHCP Snooping has been implemented across access ports.  
-HSRP used for each VLAN to load balance traffic across switches- i.e. some VLANs use MLSW1 as their default gateway while others use MLSW2. This is synchronized with STP.  
-All devices protected from unauthorized access by using 'enable secret'- although insecure passwords ('joe') have been used for practicality in lab environment.  
## Things to add in the future:
-GRE tunnelling  
-IP Phones
