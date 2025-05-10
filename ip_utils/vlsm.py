from .ipv4 import Ipv4

from .helpfunction import hostsRequiermentNumber


class VLSM:
    def __init__(self, network, cidr, hosts:"name1:n1,name2:n2,name+1:n+1"): # type: ignore
        necessaryHost = sum([hostsRequiermentNumber(int(numberOfHosts.split(":")[1])) for numberOfHosts in hosts.split(",")])
        self.subdivisedNetwork = Ipv4(network, cidr, "VLSM")
        if self.subdivisedNetwork.totalHost < necessaryHost:
            raise ValueError(f"Your subdivised network is too short. {hostsRequiermentNumber(necessaryHost)} minimum. Only {self.subdivisedNetwork.totalHost} hosts are avaible.\n" \
                             f"{hostsRequiermentNumber(necessaryHost)},{self.subdivisedNetwork.totalHost}")
        self.hosts = [(numberOfHosts.split(":")[0], int(numberOfHosts.split(":")[1])) for numberOfHosts in hosts.split(",")]
        self.hosts = list(reversed(sorted(self.hosts, key=lambda x: x[1])))
        
        self.subNetworks = []
        self.generate_sub_network()

    def selectMask(self, numberOfHosts, cidrTarget=30) -> "cidr": # type: ignore
        tmpIpv4 = Ipv4("0.0.0.0", cidrTarget)
        if tmpIpv4.totalHost >= numberOfHosts:
            return cidrTarget
        elif cidrTarget < 1:
            raise ValueError("Hosts possible exceded")
        else:
            return self.selectMask(numberOfHosts, cidrTarget-1)

    def generate_sub_network(self):
        networkTarget = self.subdivisedNetwork

        for host in range(len(self.hosts)):
            newCIDR = self.selectMask(self.hosts[host][1])
            name = self.hosts[host][0]
            subNetwork = Ipv4(networkTarget.network, newCIDR, name)

            if host < len(self.hosts) - 1:
                nextCIDR = self.selectMask(self.hosts[host+1][1])
                networkTarget = subNetwork.get_next_network(nextCIDR)

            self.subNetworks.append(subNetwork)
