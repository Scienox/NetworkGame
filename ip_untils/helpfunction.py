from .ip import IP


def get_requiermentIpInfoForHost(hostNeeded, target=30):
    tmpIp = IP("0.0.0.0", target)
    if hostNeeded <= tmpIp.totalHost:
        return tmpIp
    elif target < 1:
        raise ValueError("Hosts possible exceded")
    else:
        return get_requiermentIpInfoForHost(hostNeeded, target-1)


def hostsRequiermentNumber(hostNeeded):
    totalHosts = get_requiermentIpInfoForHost(hostNeeded)
    return totalHosts.totalHost
    

def cidrRequiermentForHost(hostNeeded):
    cidr = get_requiermentIpInfoForHost(hostNeeded)
    return cidr.cidr

def get_requiermentIpInfoForMask(mask, target=30):
    tmpIp = IP("0.0.0.0", target)
    if mask == tmpIp.subMask:
        return tmpIp
    elif target < 1:
        raise ValueError("Lenght mask possible exceded")
    else:
        return get_requiermentIpInfoForMask(mask, target-1)


def cidrRequiermentForSubnetMask(subnetMask):
    cidr = get_requiermentIpInfoForMask(subnetMask)
    return cidr.cidr
