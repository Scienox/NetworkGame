from copy import deepcopy
from .helpfunction import *


class IP:
    def __init__(self, ipHost, cidr, name=""):
        if 30 < cidr or cidr < 1:
            raise ValueError("It's not a valid CIDR")
        self.octetBinary = [128, 64, 32, 16, 8, 4, 2, 1]
        self.cidr_ = cidr
        self.totalHost_ = (2**(32 - self.cidr)) - 2
        self.name_ = name

        self.ipHost_ = convertStrToDecimal(ipHost)
        self.ipHostBinary = self.convertDecimalToBinary(self.ipHost_)
        if len(self.ipHost_) != 4:
            raise ValueError("Ip is composed of 4 Bytes and 32 bits ex:192.168.0.0")
        self.__debugIp()        
        self.subMaskBinary = self.buildSubMask()
        self.subMask_ = self.convertBinaryToDecimal(self.subMaskBinary)
        self.networkBinary = self.buildNetwork()
        self.network_ = self.convertBinaryToDecimal(self.networkBinary)

        self.firstHostBinary = self.get_first_host_b()
        self.firstHost_ = self.convertBinaryToDecimal(self.firstHostBinary)
        self.broadcastBinary = self.get_broadcast_b()
        self.broadcast_ = self.convertBinaryToDecimal(self.broadcastBinary)
        self.lastHostBinary = self.get_last_host_b()
        self.lastHost_ = self.convertBinaryToDecimal(self.lastHostBinary)

        self.type_ = self.type_detect()
        self.class_ = self.get_class()
        self.reservation_ = self.get_reservation()

    def __str__(self):
        infos = [
            f"Network Name: {self.name}\n",
            f"Type: {self.type}\n",
            f"Class: {self.classIP}\n",
            f"Reservation: {self.reservation}\n"
            f"Total hosts: {self.totalHost}\n",
            f"Ipv4: {self.ipHost}\n" if self.type == "@Ipv4" else "",
            f"SubnetMask: {self.subMask}\n",
            f"Network: {self.network}\n",
            f"First host avaible: {self.firstHost}\n",
            f"Last host avaible: {self.lastHost}\n",
            f"Broadcast: {self.broadcast}\n"
        ]
        return f"".join(str(info) for info in infos)

    def __eq__(self, ip):
        if isinstance(ip, IP):
            return (self.network == ip.network) \
            and (self.ipHost == ip.ipHost) \
            and (self.subMask == ip.subMask)
        else:
            return NotImplemented
        
    def __iter__(self):
        referenceIp = IP(self.network, self.cidr)
        hostBits = referenceIp.get_bitsHost()
        for _ in range(2**len(hostBits)):
            yield referenceIp.ipHost
            addBool(hostBits)

    def __contains__(self, otherIp):
        if isinstance(otherIp, IP):
            otherNetworkBits = otherIp.get_bitsNetwork()
            selfNetworkBits = self.get_bitsNetwork()
            if len(otherNetworkBits) < len(selfNetworkBits):
                return False
            else:
                for bit in range(len(selfNetworkBits)):
                    if selfNetworkBits[bit] != otherNetworkBits[bit]:
                        return False
                return True            
        else:
            return NotImplemented

    @property
    def cidr(self):
        return self.cidr_

    @property
    def ipHost(self):
        self.ipHost_ = self.convertBinaryToDecimal(self.ipHostBinary)
        return self.convertDecimalToString(self.ipHost_)

    @property
    def name(self):
        return self.name_

    @property
    def subMask(self):
        return self.convertDecimalToString(self.subMask_)

    @property
    def network(self):
        self.network_ = self.convertBinaryToDecimal(self.networkBinary)
        return self.convertDecimalToString(self.network_)

    @property
    def firstHost(self):
        return self.convertDecimalToString(self.firstHost_)

    @property
    def broadcast(self):
        return self.convertDecimalToString(self.broadcast_)

    @property
    def lastHost(self):
        return self.convertDecimalToString(self.lastHost_)

    @property
    def type(self):
        return self.type_

    @property
    def classIP(self):
        return self.class_

    @property
    def reservation(self):
        return self.reservation_

    @property
    def totalHost(self):
        return self.totalHost_
    
    def get_bitsHost(self):
        return get_bitsHost(self)

    def get_bitsNetwork(self):
        return get_bitsNetwork(self)

    def convertDecimalToBinary(self, vector):
        matrix = convertDecimalToBinary(vector)
        return [[Bit(matrix[octet][bit]) for bit in range(8)] for octet in range(4)]

    def convertBinaryToDecimal(self, matrix):
        matrix = [[matrix[octet][bit].value for bit in range(8)] for octet in range(4)]
        return convertBinaryToDecimal(matrix)

    def buildSubMask(self):
        bitCurrent = 0
        matrixBinary = [[Bit() for bit in range(8)] for _ in range(4)]
        for octet in range(len(matrixBinary)):
            for bit in range(len(matrixBinary[octet])):
                if bitCurrent < self.cidr:
                    matrixBinary[octet][bit].value = 1
                bitCurrent += 1
            if bitCurrent == self.cidr:
                break
        return matrixBinary

    def buildNetwork(self):
        matrixBinary = [[Bit() for bit in range(8)] for _ in range(4)]
        for octet in range(len(self.subMaskBinary)):
            for bit in range(len(self.subMaskBinary[octet])):
                if self.subMaskBinary[octet][bit].value == 1:
                    matrixBinary[octet][bit] = self.ipHostBinary[octet][bit]
                else:
                    matrixBinary[octet][bit].value = 0
        return matrixBinary

    def get_first_host_b(self):
        matrixBinary = deepcopy(self.networkBinary)
        matrixBinary[-1][-1].value = 1
        return matrixBinary

    def get_broadcast_b(self):
        matrixBinary = deepcopy(self.networkBinary)
        for octet in range(len(matrixBinary)-1, -1, -1):
            for bit in range(len(matrixBinary[len(matrixBinary)-1])-1, -1, -1):
                if self.subMaskBinary[octet][bit].value == 0:
                    matrixBinary[octet][bit].value = 1
                else:
                    return matrixBinary
        return matrixBinary

    def get_last_host_b(self):
        matrixBinary = deepcopy(self.broadcastBinary)
        matrixBinary[-1][-1].value = 0
        return matrixBinary

    def get_next_network(self, cidr):
        nextNetwork = IP(self.network, self.cidr)
        addBool(nextNetwork.get_bitsNetwork())
        nextNetwork = IP(nextNetwork.network, cidr)
        if nextNetwork.class_ != self.class_:
            raise ValueError("The next network belongs to a different class")
        elif nextNetwork.reservation != self.reservation:
            raise ValueError("The next network belongs to a different reservation")
        return nextNetwork


    """    def get_next_network(self, cidr):

            def To256(octet_l):
                if nextNetwork[octet_l] + 1 < 256:
                    nextNetwork[octet_l+1] = 0
                    nextNetwork[octet_l] += 1
                    return 
                else:
                    nextNetwork[octet_l+1] = 0
                    return To256(octet_l-1)

            magic_table = {
                "8-16-24-32": 1,
                "7-15-23-31": 2,
                "6-14-22-30": 4,
                "5-13-21-29": 8,
                "4-12-20-28": 16,
                "3-11-19-27": 32,
                "2-10-18-26": 64,
                "1-9-17-25": 128
            }

            nextNetwork = deepcopy(self.network_)
            for key in magic_table.keys():
                if str(self.cidr) in key:
                    vectorKey = key.split("-")
                    for octet in range(len(vectorKey)):
                        if str(self.cidr) == vectorKey[octet]:
                            if nextNetwork[octet] + magic_table[key] < 256:
                                nextNetwork[octet] += magic_table[key]
                            else:
                                To256(octet-1)
                            nextNetworkBuilded = IP(self.convertDecimalToString(nextNetwork), cidr)
                            if nextNetworkBuilded.class_ != self.class_:
                                raise ValueError("The next network belongs to a different class")
                            elif nextNetworkBuilded.reservation != self.reservation:
                                raise ValueError("The next network belongs to a different reservation")
                            return nextNetworkBuilded"""

    def convertDecimalToString(self, vector):
        return convertDecimalToStr(vector)
    
    def __debugIp(self):
        for octet in self.ipHost_:
            if (octet < 0) or (255 < octet):
                raise ValueError("One byte has a range 0 to 255")

    def get_class(self):
        if self.network_[0] < 127:
            return "A"
        elif self.network_[0] < 128:
            return "None"
        elif self.network_[0] < 192:
            return "B"
        elif self.network_[0] < 224:
            return "C"
        elif self.network_[0] < 240:
            return "D"
        else:
            return "E"

    def get_reservation(self):
        return Reservation(self)._detectReservation()

    def type_detect(self):
        if self.ipHost == self.network:
            return "@network"
        elif self.ipHost == self.broadcast:
            return "@broadcast"
        else:
            return "@Ipv4"


class Bit:
    def __init__(self, value=0):
        self._value = self.value = value

    def __repr__(self):
        return f"{self.value}"
    
    def __eq__(self, value):
        if isinstance(value, int):
            return self.value == value
        elif isinstance(value, Bit):
            return self.value == value.value
        else:
            return NotImplemented

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if isinstance(value, int) and (value == 0 or value == 1):
            self._value = value
        else:
            raise ValueError("Value is an int from 0 to 1")


class Reservation:
    def __init__(self, Ip:IP):
        self._networkIp = Ip.network_
        self._classIp = Ip.classIP
        self._cidrIp = Ip.cidr

    @property
    def networkIp(self):
        return self._networkIp

    @property
    def classIp(self):
        return self._classIp
    
    @property
    def cidr(self):
        return self._cidrIp

    @property  
    def isBadCidrForPrivate(self):
        privateCidr, _ = getMinimalCidr(self.classIp)
        return self.cidr < privateCidr
    
    @property
    def isBadCidrForPublic(self):
        _, publicCidr = getMinimalCidr(self.classIp)
        return self.cidr < publicCidr

    def _detectReservation(self):
        if self.classIp == "A":  # ok
            if 9 < self.networkIp[0] < 11:
                if self.isBadCidrForPrivate:
                    return "mixed"
                return "private"
            if self.isBadCidrForPublic:
                return "mixed"
            return "public"
        
        elif self.classIp == "None":
            return "localhost"
        
        elif self.classIp == "B":
            if (171 < self.networkIp[0] < 173) and (15 < self.networkIp[1] < 32):
                if self.isBadCidrForPrivate:
                    return "mixed"
                return "private"
            if self.isBadCidrForPublic:
                return "mixed"
            return "public"
        
        elif self.classIp == "C":
            if (self.networkIp == [192, 0, 2, 0]) and (self.cidr == 24):
                #self.name_ = "(TEST-NET-1)"
                return "IETF"
            elif (self.networkIp == [198, 51, 100, 0]) and (self.cidr == 24):
                #self.name_ = "(TEST-NET-2)"
                return "IETF"
            elif (self.networkIp == [203, 0, 113, 0]) and (self.cidr == 24):
                #self.name_ = "(TEST-NET-3)"
                return "IETF"
            
            elif (191 < self.networkIp[0] < 193) and (167 < self.networkIp[1] < 169):
                if self.isBadCidrForPrivate:
                    return "mixed"
                return "private"
            elif self.isBadCidrForPublic:
                return "mixed"
            return "public"
        
        elif self.classIp == "D":
            if self.isBadCidrForPrivate:
                raise ValueError("Multicast exceeded\nMinimal cidr is /4\n")
            return "multicast"
        else:
            return "None"


def addBool(sequence, current=-1):
    target:Bit = sequence[current]
    if target.value == 0:
        sequence[current].value = 1
        return
    elif all(bit.value == 1 for bit in sequence):
        return
    else:
        sequence[current].value = 0
        return addBool(sequence, current-1)
