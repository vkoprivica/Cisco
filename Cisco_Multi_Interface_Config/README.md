# Cisco Multi Interface CLI Configuration Build

The purpose of the script is to help quickly build CLI configuration for multiple Cisco Interfaces that are in scope of different interface ranges. Prior to running the script, the user should save multiple lines of text that contain interface names into the data/input_interfaces.txt file. Also, the user should specify desired interface configuration into /data/desired_config.txt and run the script. Once done, the script will export parsed proposed interface configuration into /data/output.txt file. 

### Prerequisites

Python 3.   

### Instructions

1. Fill out data/input_interfaces.txt and data/desired_config.txt files. 
2. Run script. 
3. Find proposed configuration in /data/output.txt.

Example of text lines containing interface names (data/input_interfaces.txt):

b0:b8:67:c6:dd:d0   Gi8/0/18       120                        b0b8.67c6.ddd0
Te2/0/33                       admin down     down    
Te2/0/34                       admin down     down  
GigabitEthernet0/0/1   unassigned      YES NVRAM  administratively down down   
Loopback0              unassigned      YES unset  up                    up  
Port-channel18         unassigned      YES unset  administratively down down  
Gi0/0                          up             up  

Example of provided interface CLI configuration (/data/desired_config.txt):

switchport mode access  
switchport access vlan 3    
no shut        
exit        
end 

Example of /data/output.txt file:

interface Gi8/0/18  
switchport mode access  
switchport access vlan 3    
no shut  
exit               
interface Te2/0/33  
switchport mode access  
switchport access vlan 3    
no shut  
exit            
interface Te2/0/34  
switchport mode access  
switchport access vlan 3    
no shut  
exit        
interface Loopback0  
switchport mode access  
switchport access vlan 3    
no shut  
exit            

##################################

Supported Interface Input Formats:

GiX/X/X or GiX/X or GiX 
GigabitEthernetX/X/X or GigabitEthernetX/X or GigabitEthernetX  
PoXXXX or PoXXX or PoXX or PoX  
Port-channelXXXX or Port-channelXXX or Port-channelXX or Port-channelX  
FastEthernetX/X/X or FastEthernetX/X or FastEthernetX   
FaX/X/X or FaX/X or FaX 
LoopbackXXX or LoopbackXX or LoopbackX  
LoXXX or LoXX or LoX    
TenGigabitEthernetX/X/X or TenGigabitEthernetX/X or TenGigabitEthernetX  
TeX/X/X or TeX/X or TeX 
X == any number 

##################################

To run script:
python -m ciscomintconfig, or
python3 -m ciscomintconfig
 