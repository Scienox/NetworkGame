from .helpfunction import *
from random import choice, randint
from .ipv4 import Ipv4, addBool


class Ipv4Manager:
    def __init__(self, klass=None, reservation=None,
                 ttype=None, cidr=None):
        self.klass = klass
        self.reservation = reservation
        self.cidr = cidr
        self.ttype = ttype

    def getRangeAvaible(self):
        if self.klass == 'A':
            return "0.0.0.0", "126.255.255.255"
        elif self.klass == 'B':
            return "128.0.0.0", "191.255.255.255"
        elif self.klass == 'C':
            return "192.0.0.0", "223.255.255.255"
        elif self.klass == 'D':
            return "224.0.0.0", "239.255.255.255"
        elif self.klass == 'E':
            return "240.0.0.0", "255.255.255.255"
        
    def getRangeReservation(self):
        if self.klass == 'A':
            if self.reservation == 'private':
                return "10.0.0.0", "10.255.255.255"
            else:
                return "0.0.0.0", "9.255.255.255", "11.0.0.0", "191.0.0.0"
        elif self.klass == 'B':
            if self.reservation == 'private':
                return "172.16.0.0", "172.31.255.255"
            else:
                return "128.0.0.0", "172.15.255.255", "173.0.0.0", "191.255.255.255"
        elif self.klass == 'C':
            if self.reservation == 'private':
                return "192.168.0.0", "192.168.255.255"            
            else:
                return "192.0.0.0", "192.167.255.255", "193.0.0.0", "223.255.255.255"
        else:
            if self.reservation == 'localhost':
                return "127.0.0.0", "127.255.255.255"
            return self.getRangeAvaible()

    def selectFromRange(self):
        def buildVector(rRange):
            minimal = vectorStrToInt(rRange[0].split('.'))
            maximal = vectorStrToInt(rRange[1].split('.'))
            for octet in range(4):
                vectorSelected.append(randint(minimal[octet], maximal[octet]))

        if self.reservation == "IETF":
            return choice(["192.0.2.0", "198.51.100.0", "203.0.113.0"])
        vectorSelected = list()
        ranges = self.getRangeReservation()
        if len(ranges) != 2:
            firstSet = ranges[0], ranges[1]
            secondSet = ranges[2], ranges[3]
            setSelected = choice([firstSet, secondSet])
            ranges = setSelected
        buildVector(ranges)
        if self.klass == "C" and self.reservation != "IETF":
            excludeIETF(vectorSelected, self.cidr, choice)
        return ".".join(str(octet) for octet in vectorSelected)

    def generateRandomIpv4(self):
        setklass = ["E", "D", "A", "B", "C"]
        if self.cidr:
            if self.cidr < 16:
                setklass.pop()
            if self.cidr < 12:
                setklass.pop()
            if self.cidr < 8:
                setklass.pop()
        if not self.klass:
            self.klass = choice(setklass)
        if not self.reservation:
            multichoice = ["private", "public"]
            if self.klass == "C":
                multichoice += ["IETF"]
            elif self.klass == "None":
                multichoice = ['localhost']
            elif self.klass == "D":
                multichoice = ["multicast"]
            elif self.klass == "E":
                multichoice = ["None"]
            self.reservation = choice(multichoice)
        if not self.cidr:
            if self.reservation == "IETF":
                self.cidr = 24
            else: self.cidr = randint(self.getMinimalCidr(), 30)

        ipv4Tmp = Ipv4(self.selectFromRange(), self.cidr)
        randomHost(ipv4Tmp)
        ipv4 = Ipv4(ipv4Tmp.ipHost, ipv4Tmp.cidr)
        ipNetwork = Ipv4(ipv4Tmp.network, ipv4Tmp.cidr)
        ipBroadcast = Ipv4(ipv4Tmp.broadcast, ipv4Tmp.cidr)
        if self.ttype == "@Ipv4":
            return ipv4
        elif self.ttype == "@network":
            return ipNetwork
        elif self.ttype == "@broadcast":
            return ipBroadcast
        else:
            return choice([ipv4, ipNetwork, ipBroadcast])
    
    def getMinimalCidr(self, ipv4=None):
        current = 0 if self.reservation == 'private' else 1
        return self._getMinimalCidr()[current]

    def _getMinimalCidr(self):
        return getMinimalCidr(self.klass)


def vectorStrToInt(vectorStr):
    vectorInt = [int(octet) for octet in vectorStr]
    return vectorInt


def randomHost(ipv4:Ipv4):
    hostBits = ipv4.get_bitsHost()
    llen = len(hostBits) - 1
    for bit in hostBits:
        bit.value = 0
    for _ in range(1, llen):
        addBool(hostBits)
