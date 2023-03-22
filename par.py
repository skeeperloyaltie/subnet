import sys
import math

def calculate_subnet_details(ip_address, subnet_mask, num_hosts):
    # Convert the IP address and subnet mask to binary strings
    ip_address_bin = ''.join([bin(octet)[2:].zfill(8) for octet in ip_address])
    subnet_mask_bin = ''.join([bin(octet)[2:].zfill(8) for octet in subnet_mask])

    # Calculate the network address and broadcast address
    network_address_bin = ''.join([str(int(ip_address_bin[i]) & int(subnet_mask_bin[i])) for i in range(32)])
    broadcast_address_bin = network_address_bin[:-(math.ceil(math.log2(num_hosts + 2)))]

    # Convert the binary strings to decimal format
    network_address = '.'.join([str(int(network_address_bin[i:i+8], 2)) for i in range(0, 32, 8)])
    broadcast_address = '.'.join([str(int(broadcast_address_bin[i:i+8], 2)) for i in range(0, 32, 8)])
    subnet_mask_str = '.'.join([str(octet) for octet in subnet_mask])

    print("IP address (binary):", ip_address_bin)
    print("Subnet mask (binary):", subnet_mask_bin)
    print("Network address (binary):", network_address_bin)
    print("Broadcast address (binary):", broadcast_address_bin)
    print("Network address:", network_address)
    print("Broadcast address:", broadcast_address)
    print("Subnet mask:", subnet_mask_str)

    return {
        "subnet_address": network_address,
        "broadcast_address": broadcast_address,
        "usable_hosts": num_hosts,
        "subnet_mask": subnet_mask_str
    }


def calculate_subnet_mask(subnet_bits):
    subnet_mask = [0, 0, 0, 0]
    for i in range(subnet_bits):
        subnet_mask[i // 8] += 1 << (7 - i % 8)
    return subnet_mask


def print_subnet_details(ip_address, subnet_mask, network_address, broadcast_address, num_usable_hosts):
    print("Subnet mask: {}.{}.{}.{}".format(*subnet_mask))
    print("Network address: {}.{}.{}.{}".format(*network_address))
    print("Broadcast address: {}.{}.{}.{}".format(*broadcast_address))
    print("Usable hosts: {}/{}".format(num_usable_hosts, num_usable_hosts + 2))
    print("Total number of hosts: {}".format(num_usable_hosts + 2))


def main():
    # Get the IP address and subnet bits from the command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python ipcalc.py [IP address] [Number of subnets] -s [Number of hosts for each subnet]")
        sys.exit(1)

    ip_address = list(map(int, sys.argv[1].split(".")))
    num_subnets = int(sys.argv[2])

    # Parse subnet hosts from command-line arguments
    subnet_hosts = []
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "-s":
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith("-"):
                subnet_hosts.append(int(sys.argv[i]))
                i += 1
        else:
            i += 1

    # Calculate the subnet bits and total number of hosts for each subnet
    subnet_bits = int(math.ceil(math.log2(num_subnets)))
    if subnet_bits > 30:
        print("Too many subnets")
        sys.exit(1)

    if len(subnet_hosts) != num_subnets:
        print("Number of subnet hosts does not match number of subnets")
        sys.exit(1)

    total_hosts = sum(subnet_hosts)
    if total_hosts > pow(2, 32 - subnet_bits) - 2:
        print("Too many hosts")
        sys.exit(1)

    # Print the details for each subnet
    subnet_mask_bits = 32 - subnet_bits
    for i, num_hosts in enumerate(subnet_hosts):
        print("Subnet #{}".format(i+1))
        subnet_mask = calculate_subnet_mask(subnet_mask_bits)
        subnet_details = calculate_subnet_details(ip_address, subnet_mask, num_hosts)
        print_subnet_details(subnet_mask, subnet_details["subnet_address"], subnet_details["broadcast_address"], subnet_details["num_usable_hosts"])
        ip_address[3] += subnet_details["num_hosts"]

if __name__ == '__main__':
    main()
