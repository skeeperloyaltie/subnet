import math
import sys

def subnet_calc(ip_address, subnet_bits):
    # Calculate the subnet mask
    subnet_mask = ""
    for i in range(32):
        if i < subnet_bits:
            subnet_mask += "1"
        else:
            subnet_mask += "0"
    subnet_mask = [int(subnet_mask[i:i+8], 2) for i in range(0, 32, 8)]

    # Calculate the network address
    network_address = []
    for i in range(4):
        network_address.append(ip_address[i] & subnet_mask[i])

    # Calculate the broadcast address
    broadcast_address = []
    for i in range(4):
        broadcast_address.append(ip_address[i] | (255 - subnet_mask[i]))

    # Calculate the number of hosts per subnet
    num_hosts = int(math.pow(2, 32 - subnet_bits)) - 2

    # Calculate the usable and unusable hosts
    usable_hosts = num_hosts
    unusable_hosts = 0
    if num_hosts >= 2:
        usable_hosts -= 2
        unusable_hosts = 2

    # Print the results
    print("Subnet mask: {}.{}.{}.{}".format(subnet_mask[0], subnet_mask[1], subnet_mask[2], subnet_mask[3]))
    print("Network address: {}.{}.{}.{}".format(network_address[0], network_address[1], network_address[2], network_address[3]))
    print("Broadcast address: {}.{}.{}.{}".format(broadcast_address[0], broadcast_address[1], broadcast_address[2], broadcast_address[3]))
    print("Number of hosts per subnet: {}".format(num_hosts))
    print("Usable hosts per subnet: {}".format(usable_hosts))
    print("Unusable hosts per subnet: {}".format(unusable_hosts))
    print("")


def main():
    # Get the IP address, number of subnets, and number of hosts per subnet from the command-line arguments
    if len(sys.argv) != 4:
        print("Usage: python subnet_calc.py [IP address] [Number of subnets] [Number of hosts per subnet]")
        sys.exit(1)

    ip_address = list(map(int, sys.argv[1].split(".")))
    num_subnets = int(sys.argv[2])
    num_hosts_per_subnet = int(sys.argv[3])

    # Calculate the subnet bits for each subnet
    subnet_bits = int(math.ceil(math.log2(num_subnets)))
    if subnet_bits > 30:
        print("Too many subnets")
        sys.exit(1)

    # Calculate the host bits for each subnet
    host_bits = int(math.ceil(math.log2(num_hosts_per_subnet+2)))
    if host_bits > 30-subnet_bits:
        print("Too many hosts per subnet")
        sys.exit(1)

    # Print the details for each subnet
    for i in range(num_subnets):
        print("Subnet #{}".format(i+1))
        subnet_mask_bits = 32 - subnet_bits - host_bits
        subnet_mask = [255, 255, 255, 255]
        subnet_mask_bits_left = subnet_mask_bits
        while subnet_mask_bits_left > 0:
            if subnet_mask_bits_left >= 8:
                subnet_mask[3-int(subnet_mask_bits_left/8)] = 0
                subnet_mask_bits_left -= 8
            else:
                subnet_mask[3-int(subnet_mask_bits_left/8)] = 256 - int(math.pow(2, 8 - subnet_mask_bits_left))
                subnet_mask_bits_left = 0
        subnet_mask = tuple(subnet_mask)
        subnet_calc(ip_address, subnet_bits+subnet_mask_bits+host_bits, num_hosts_per_subnet)
        ip_address[3] += int(math.pow(2, subnet_mask_bits+host_bits))
        if ip_address[3] > 255:
            ip_address[2] += int(ip_address[3]/256)
            ip_address[3] = ip_address[3] % 256

if __name__ == "__main__":
    main()
