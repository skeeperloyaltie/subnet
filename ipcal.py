import math
import sys

def subnet_calc(ip_address, bits, num_hosts_per_subnet):
    # Calculate the subnet mask
    subnet_mask_bits = 32 - bits
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

    # Calculate the number of usable hosts per subnet
    num_usable_hosts_per_subnet = [num_hosts_per_subnet[i] - 2 for i in range(len(num_hosts_per_subnet))]

    # Calculate the number of subnets
    num_subnets = int(math.pow(2, bits - subnet_mask_bits))

    # Calculate the network and broadcast addresses for each subnet
    subnet_addresses = []
    broadcast_addresses = []
    network_address = list(ip_address)
    for i in range(num_subnets):
        # Calculate the network and broadcast address for the current subnet
        subnet_addresses.append(tuple(network_address))
        broadcast_address = list(network_address)
        broadcast_address[3] += num_hosts_per_subnet[i] - 1
        if broadcast_address[3] > 255:
            broadcast_address[2] += int(broadcast_address[3]/256)
            broadcast_address[3] = broadcast_address[3] % 256
        broadcast_addresses.append(tuple(broadcast_address))

        # Calculate the network address for the next subnet
        network_address[3] += num_hosts_per_subnet[i]
        if network_address[3] > 255:
            network_address[2] += int(network_address[3]/256)
            network_address[3] = network_address[3] % 256

    # Print the details for each subnet
    for i in range(num_subnets):
        print("Subnet #{}".format(i+1))
        print("Subnet address: {}".format(subnet_addresses[i]))
        print("Broadcast address: {}".format(broadcast_addresses[i]))
        print("Subnet mask: {}".format(subnet_mask))
        print("Usable hosts: {}/{}".format(num_usable_hosts_per_subnet[i], num_hosts_per_subnet[i]))
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
