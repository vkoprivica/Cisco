# __main__.py

import os
import re
import sys

FOLDER = os.path.dirname(os.path.realpath(__file__))

# Regex filters to match interface names coppied from switches.
GI_PORT_REGEX = re.compile(
    r"gi(?:gabitethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")
TE_PORT_REGEX = re.compile(
    r"te(?:ngabitethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")
FA_PORT_REGEX = re.compile(
    r"fa(?:stethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?$")
PO_PORT_REGEX = re.compile(
    r"po(?:rt-channel)?\d{0,4}$")
LO_PORT_REGEX = re.compile(
    r"lo(?:opback)?\d{0,4}$")
ETH_PORT_REGEX = re.compile(
    r"eth(?:ernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")


# Regex filters to match only numberic values at the end of interface names.
# This will help determine if there is duplicate interface names:
# for example between gi and gigabithethernet
ETH_NUM_CHECK_REGEX = r"\d+(?:\/\d+)?(?:\/\d{0,2})?$"  # gi, te, fa, eth
LO_PO_NUM_CHECK_REGEX = r"\d{0,4}$"  # loopback, port-channel

# Dictionary to map interface prefix with numeric value
INTERFACES_NAME_ELEMENTS = {
    "gi": ETH_NUM_CHECK_REGEX,
    "te": ETH_NUM_CHECK_REGEX,
    "fa": ETH_NUM_CHECK_REGEX,
    "eth": ETH_NUM_CHECK_REGEX,
    "po": LO_PO_NUM_CHECK_REGEX,
    "lo": LO_PO_NUM_CHECK_REGEX,
}


def interfaces_input() -> list:
    # Take the input from the user, create the list of lines and transfer into lower case characters.
    print("#" * 79)
    print(f"Paste text with the list of switch ports. You can reference 'input_examples.txt'.")
    input_lines_lst = []
    while True:
        user_input = input(
            "Press Enter once again when done: ")
        if not user_input:
            break
        input_lines_lst.append(user_input.lower())

    # Since each line could contain white spaces and other gibberish characters,
    # transfer list of lines into list of strings.
    return [i.split() for i in input_lines_lst]


def parse_interfaces(interfaces_list: list) -> list:
    # Search interfaces_list with Regex.
    # Match the first interface name in the line and ignore any additional
    # that could exist by user input mistake in the same line.

    if len(interfaces_list) > 0:
        interface_names = []
        for line in interfaces_list:
            for item in line:
                any(re.search(re_string, item) for re_string in [
                    GI_PORT_REGEX,
                    TE_PORT_REGEX,
                    FA_PORT_REGEX,
                    PO_PORT_REGEX,
                    LO_PORT_REGEX,
                    ETH_PORT_REGEX,
                ])
                interface_names.append(item)
                break

        # Transfer all parsed interfaces to the same naming convention: gi, or fa, or lo, etc.
        # This is nacessary to find out for example if duplicate interfaces exist between GigabitEthernet and Gi.
        parsed_interfaces = []
        line_count = 0
        for interface in interface_names:
            line_count += 1
            for int_name, int_number in INTERFACES_NAME_ELEMENTS.items():
                try:
                    if re.search(int_name, interface):
                        match = (re.search(int_number, interface))
                        numeric_match = (interface[match.span()[0]:])
                        if (f"{int_name}{numeric_match}") not in parsed_interfaces:
                            parsed_interfaces.append(
                                f"{int_name}{numeric_match}")
                            break
                        else:
                            print(
                                f"""Interface duplicate at line {line_count} ({int_name}{numeric_match}). 
                                Please remove and start from the beginning!""")
                            parsed_interfaces = []
                            return parsed_interfaces
                except:
                    print(
                        f"Script have not been able to parse input at line {line_count}!")
                    parsed_interfaces = []
                    return parsed_interfaces
        return parsed_interfaces

    else:
        print("Detected empty input. Please enter interface name!")


def create_config(parsed_interfaces: list) -> str:
    # If no duplicates; prompt user for switch port configuration.
    if parsed_interfaces != [] and parsed_interfaces != None:
        config_list = []
        config_str = ""
        print()
        print(f"Please enter desired interface configuration - Line by Line.")
        while config_str != 'end':
            config_str = input(
                "Type 'end' at the last line to continue: ")
            config_list.append(config_str)
            continue

    # Write output configuration to the external file located in same directory where script reside.
        output_text_file = f"{FOLDER}/output.txt"
        with open(os.path.join(sys.path[0], output_text_file), "w") as interface_config_output:
            for i in parsed_interfaces:
                interface_config_output.write(f"interface {i}\n")
                for item in config_list:
                    interface_config_output.write(f"{item}\n")
        print(f"Configuration has been exported to: 'output.txt'!")


def main():
    user_input = interfaces_input()
    parsed_interfaces = parse_interfaces(user_input)
    create_config(parsed_interfaces)


if __name__ == "__main__":
    main()
