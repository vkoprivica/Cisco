# __main__.py

import os
import re
import sys

FOLDER = os.path.dirname(os.path.realpath(__file__))

# Regex filters to match interface names coppied from switches.
GI_PORT_REGEX = re.compile(
    r"^gi(?:gabitethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")
TE_PORT_REGEX = re.compile(
    r"^te(?:ngabitethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")
FA_PORT_REGEX = re.compile(
    r"^fa(?:stethernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?$")
PO_PORT_REGEX = re.compile(
    r"^po(?:rt-channel)?\d{0,4}$")
LO_PORT_REGEX = re.compile(
    r"^lo(?:opback)?\d{0,4}$")
ETH_PORT_REGEX = re.compile(
    r"^eth(?:ernet)?\d+(?:\/\d+)?(?:\/\d{0,2})?")


# Regex filters to match only numberic values at the end of interface names.
# This will help determine if there is duplicate interface names:
# for example between gi and gigabithethernet.
ETH_NUM_CHECK_REGEX = r"\d+(?:\/\d+)?(?:\/\d{0,2})?$"  # gi, te, fa, eth
LO_PO_NUM_CHECK_REGEX = r"\d{0,4}$"  # loopback, port-channel

# Dictionary to map interface prefix with numeric value.
INTERFACES_NAME_ELEMENTS = {
    "gi": [GI_PORT_REGEX, ETH_NUM_CHECK_REGEX],
    "te": [TE_PORT_REGEX, ETH_NUM_CHECK_REGEX],
    "fa": [FA_PORT_REGEX, ETH_NUM_CHECK_REGEX],
    "eth": [ETH_PORT_REGEX, ETH_NUM_CHECK_REGEX],
    "po": [PO_PORT_REGEX, LO_PO_NUM_CHECK_REGEX],
    "lo": [LO_PORT_REGEX, LO_PO_NUM_CHECK_REGEX],
}


def lowercase_transfer(input_interfaces: str) -> list:
    # Read the input from input_interfaces.txt file.
    with open(f"{FOLDER}/data/{input_interfaces}", "r") as input_data:
        input_lines_lst = input_data.readlines()

    return [i.lower().split() for i in input_lines_lst]


def parse_interfaces(interfaces_list: list) -> list:
    # Search interfaces_list with Regex.
    # Match the first interface name in the line and ignore any additional
    # that could exist by user input mistake in the same line.
    if interfaces_list != [[]]:
        interface_names = []
        for parent_list in interfaces_list:
            for child_list in parent_list:
                if any(re.search(re_string, child_list) for re_string in [
                    GI_PORT_REGEX,
                    TE_PORT_REGEX,
                    FA_PORT_REGEX,
                    PO_PORT_REGEX,
                    LO_PORT_REGEX,
                    ETH_PORT_REGEX,
                ]):
                    interface_names.append(child_list)
                    break

        # Transfer all parsed interfaces to the same naming convention: gi, or fa, or lo, etc.
        # This is nacessary to find out for example if duplicate interfaces exist
        # between GigabitEthernet and Gi.
        parsed_interfaces = []
        for interface in interface_names:
            for int_name, int_number in INTERFACES_NAME_ELEMENTS.items():
                try:
                    if re.search(int_number[0], interface):
                        match = (re.search(int_number[1], interface))
                        numeric_match = (interface[match.span()[0]:])
                        if (f"{int_name}{numeric_match}") not in parsed_interfaces:
                            parsed_interfaces.append(
                                f"{int_name}{numeric_match}")
                            break
                        else:
                            print(
                                f"Interface duplicate detected ({interface}).")
                            print("Please remove and start from the beginning!")
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
    if len(parsed_interfaces) > 0:
        # Read the input from input_interfaces.txt file.
        with open(f"{FOLDER}/data/desired_config.txt", "r") as input_data:
            desired_config = input_data.read()

        # Write output configuration to the output.txt file.
            output_text_file = f"{FOLDER}/data/output.txt"
            with open(os.path.join(sys.path[0], output_text_file), "w") as interface_config_output:
                for i in parsed_interfaces:
                    interface_config_output.write(f"interface {i}\n")
                    interface_config_output.write(f"{desired_config}\n")
            print(f"Configuration has been exported to: 'output.txt'!")


def main():
    interfaces_list = lowercase_transfer("input_interfaces.txt")
    parsed_interfaces = parse_interfaces(interfaces_list)
    create_config(parsed_interfaces)


if __name__ == "__main__":
    main()
