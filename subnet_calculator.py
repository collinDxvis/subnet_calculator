import ipaddress
import pandas as pd
import os
import math

def subnet_calculator(network, num_subnets):
    try:
        network = ipaddress.IPv4Network(network, strict=False)
        new_prefix_len = network.prefixlen + math.ceil(math.log2(num_subnets))
        subnets = list(network.subnets(new_prefix=new_prefix_len))
        if len(subnets) < num_subnets:
            raise ValueError(f"Unable to create {num_subnets} subnets from {network}")
        
        results = []
        for subnet in subnets[:num_subnets]:
            result = {
                "Subnet Network Address": str(subnet.network_address),
                "Broadcast Address": str(subnet.broadcast_address),
                "Subnet Mask": str(subnet.netmask),
                "Number of Usable Hosts": subnet.num_addresses - 2,
                "First Usable Host": str(subnet.network_address + 1),
                "Last Usable Host": str(subnet.broadcast_address - 1),
            }
            results.append(result)
        return results
    except ValueError as e:
        return [{"Error": str(e)}]

def main():
    network = input("Enter the network (e.g., 192.168.1.0/24): ")
    num_subnets = int(input("Enter the number of subnets to create: "))

    results = subnet_calculator(network, num_subnets)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(results)

    # Get the script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Export the DataFrame to a CSV file in the script's directory
    output_file = os.path.join(script_dir, 'subnet_calculations.csv')
    df.to_csv(output_file, index=False)
    print(f"Subnet calculations have been exported to {output_file}")

if __name__ == "__main__":
    main()
