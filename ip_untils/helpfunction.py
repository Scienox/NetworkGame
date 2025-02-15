from .ip import IP


def hostsRequiermentNumber(hostNeeded, target=30):
    tmpIp = IP("0.0.0.0", target)
    if hostNeeded <= tmpIp.totalHost:
        return tmpIp.totalHost
    elif target < 1:
        raise ValueError("Hosts possible exceded")
    else:
        return hostsRequiermentNumber(hostNeeded, target-1)
    