"""
Author: Vukasin Koprivica
Purpose: Create quickly switch port cli configurations for provided list of switch ports. 
INPUT:
Paste one or multiple switch port names for which you would like to build 
switch port configurations. Script will parse and remove additional text. 
You can use commands: show cdp neighbors, show ip interface brief, show interface description, show interfaces.

Example of provided switch ports for script to parse:
b0:b8:67:c6:dd:d0   Gi8/0/18       120                        b0b8.67c6.ddd0
Te2/0/33                       admin down     down    
Te2/0/34                       admin down     down  
GigabitEthernet0/0/1   unassigned      YES NVRAM  administratively down down   
Loopback0              unassigned      YES unset  up                    up  
Port-channel18         unassigned      YES unset  administratively down down  
Gi0/0                          up             up     

Provide switch port configuration you would like to be assigned to provided ports. 

Example of provided switch port configuration:
switchport mode access
switchport access vlan 3
no shut
exit
end

OUTPUT:
Script will create a text file (interface_config_output.txt) under the same directory where reside and dump configuration. 
Example:
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
"""
import re
import sys, os

# From user input create the list of lines and transfer into lower case character.
input_lines_lst = []
while True:
    user_input_str = input('Paste text with the list of switch ports. Press Enter once again when done: ')
    if not user_input_str:
        break
    input_lines_lst.append(user_input_str.lower())


# Since each line could contain white spaces and other gibberish characters, transfer list of lines to list of strings. 
list_of_strings = []
for i in input_lines_lst:
    list_of_strings.append(i.split())


# Regex filters to match interface names coppied from switches.
gi_port = re.compile(r"gi(?:gabitethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")
te_port = re.compile(r"te(?:ngabitethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")
fa_port = re.compile(r"fa(?:stethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?$")
po_port = re.compile(r"po(?:rt-channel)?\d{0,4}$")
lo_port = re.compile(r"lo(?:opback)?\d{0,4}$")
eth_port = re.compile(r"eth(?:ernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")

# Regex filters to match only numberic values at the end of interface names. This will help determine if 
# there is an duplicate interface for example between gi and gigabithethernet. 
gi_numeric_checker = "\d+(?:\/\d+)?(?:\/\d{0,2})?$"    
te_numeric_checker = "\d+(?:\/\d+)?(?:\/\d{0,2})?$"
fa_numeric_checker = "\d+(?:\/\d+)?(?:\/\d{0,2})?$"
po_numeric_checker = "\d{0,4}$"
lo_numeric_checker = "\d{0,4}$"
eth_numeric_checker = "\d+(?:\/\d+)?(?:\/\d{0,2})?$"


# Search list_of_strings with Regex. 
# Match first interface in line and ignore any additional interface name that could exist in the same line as port descriptions could 
# contain interface names as well.
interface_names = []
for line in list_of_strings:
    for item in line:
        # if item not in interface_names:
        if re.search(gi_port, item):
            interface_names.append(item)
            break
        elif re.search(te_port, item):
            interface_names.append(item)
            break
        elif re.search(fa_port, item):
            interface_names.append(item)
            break
        elif re.search(lo_port, item):
            interface_names.append(item)
            break
        elif re.search(po_port, item):
            interface_names.append(item)
            break
        elif re.search(eth_port, item):
            interface_names.append(item)
            break


# Transfer all parsed interfaces to the same naming convention: gi, or fa, or lo, etc. This is nacessary 
# to find out for example if duplicate interfaces exist between GigabitEthernet and Gi.
interface_names_final = []
count = 0
for interface in interface_names:
    count += 1
    if re.search("gi", interface):
        gi_match = (re.search(gi_numeric_checker, interface))
        numeric_match = (interface[gi_match.span()[0] :])
        if (f"gi{numeric_match}") not in interface_names_final:
            interface_names_final.append(f"gi{numeric_match}")
        else:
            print(f"Interface duplicate: ({(f'gi{numeric_match}')}). Please remove and start from beginning!")
            interface_names_final = []
            break

    elif re.search("te", interface):
        te_match = (re.search(te_numeric_checker, interface))
        numeric_match = (interface[te_match.span()[0] :])
        if (f"te{numeric_match}") not in interface_names_final:
            interface_names_final.append(f"te{numeric_match}")
        else:
            print(f"Interface duplicate: ({(f'te{numeric_match}')}). Please remove and start from beginning!")
            interface_names_final = []
            break

    elif re.search("fa", interface):
        fa_match = (re.search(fa_numeric_checker, interface))
        numeric_match = (interface[fa_match.span()[0] :])
        if (f"fa{numeric_match}") not in interface_names_final:
            interface_names_final.append(f"fa{numeric_match}")
        else:
            print(f"Interface duplicate: ({(f'fa{numeric_match}')}). Please remove and start from beginning!")
            interface_names_final = []
            break

    elif re.search("lo", interface):
        lo_match = (re.search(lo_numeric_checker, interface))
        numeric_match = (interface[lo_match.span()[0] :])
        if (f"lo{numeric_match}") not in interface_names_final:
            interface_names_final.append(f"lo{numeric_match}")
        else:
            print(f"Interface duplicate: ({(f'lo{numeric_match}')}). Please remove and start from beginning!")
            interface_names_final = []
            break

    elif re.search("po", interface):
        po_match = (re.search(po_numeric_checker, interface))
        numeric_match = (interface[po_match.span()[0] :])
        if (f"po{numeric_match}") not in interface_names_final:
            interface_names_final.append(f"po{numeric_match}")
        else:
            print(f"Interface duplicate: ({(f'po{numeric_match}')}). Please remove and start from beginning!")
            interface_names_final = []
            break

    elif re.search("eth", interface):
        eth_match = (re.search(eth_numeric_checker, interface))
        numeric_match = (interface[eth_match.span()[0] :])
        if (f"eth{numeric_match}") not in interface_names_final:
            interface_names_final.append(f"eth{numeric_match}")
        else:
            print(f"Interface duplicate: ({(f'eth{numeric_match}')}). Please remove and start from beginning!")
            interface_names_final = []
            break


# If no duplicates exist prompt user for switch port configuration. 
if interface_names_final != []:
    config_list = []
    config_str = ""
    while config_str != 'end':
        config_str = input("Please enter switch port configuration - Line by Line. Type 'end' in the last line to continue: ")
        config_list.append(config_str)
        continue

# Write output with switch port configuration to the external file located in same directory where script reside. 
    output_text_file = "interface_config_output.txt"
    with open(os.path.join(sys.path[0], output_text_file), "w") as interface_config_output:
        for i in interface_names_final:
            interface_config_output.write(f"interface {i}\n")
            for item in range(len(config_list)-1):
                interface_config_output.write(f"{config_list[item]}\n")
    print (f"Configuration has been exported to: 'interface_config_output.txt'!")
# If Regex failed to parse data display an error:                    
else:
    print("Script have not been able to parse input!")

