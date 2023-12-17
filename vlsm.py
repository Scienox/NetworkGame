from ip import IP


class VLSM:
    def __init__(self, network, cidr, hosts:"name1:n1,name2:n2,name+1:n+1"):
        self.hosts = [int(numberOfHosts) for numberOfHosts in hosts.split(",")]
        self.hosts = list(reversed(sorted(self.hosts)))
        self.motherNetwork = IP(network, cidr)
        self.subNetworks = []
        self.generate_sub_network()

    def selectMask(self, numberOfHosts, cidrTarget=30) -> "cidr":
        tmpIP = IP("0.0.0.0", cidrTarget)
        if tmpIP.totalHost >= numberOfHosts:
            return cidrTarget
        else:
            return self.selectMask(numberOfHosts, cidrTarget-1)

    def generate_sub_network(self):
        networkTarget = self.motherNetwork

        for host in range(len(self.hosts)):
            newCIDR = self.selectMask(self.hosts[host])
            subNetwork = IP(networkTarget.network, newCIDR)

            if host < len(self.hosts) - 1:
                nextCIDR = self.selectMask(self.hosts[host+1])
                networkTarget = subNetwork.get_next_network(nextCIDR)

            self.subNetworks.append(subNetwork)
