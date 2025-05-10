def get_octet_binary_count():
    return [128, 64, 32, 16, 8, 4, 2, 1]


def get_requiermentIpv4InfoForHost(hostNeeded, target=30):
    totalHost = (2**(32 - target)) - 2
    if hostNeeded <= totalHost:
        return totalHost, target
    elif target < 1:
        raise ValueError("Hosts possible exceded")
    else:
        return get_requiermentIpv4InfoForHost(hostNeeded, target-1)


def hostsRequiermentNumber(hostNeeded):
    totalHosts = get_requiermentIpv4InfoForHost(hostNeeded)[0]
    return totalHosts


def convertDecimalToBinary(vector):
        octetBinaryCount = get_octet_binary_count()
        matrixBinary = [[0 for bit in range(8)] for _ in range(4)]
        for octet in range(len(vector)):
            octetValue = vector[octet]
            refOctet = 0

            for bit in range(len(octetBinaryCount)):
                bitValue = octetBinaryCount[bit]
                if refOctet + bitValue <= octetValue:
                    matrixBinary[octet][bit] = 1
                    refOctet += bitValue
        return matrixBinary


def convertBinaryToDecimal(matrix):
        octetBinaryCount = get_octet_binary_count()
        vector = [0 for _ in range(4)]
        for octet in range(len(matrix)):
            refOctet = 0
            for bit in range(len(matrix[octet])):
                if matrix[octet][bit] == 1:
                    refOctet += octetBinaryCount[bit]
            vector[octet] = refOctet
        return vector


def convertStrToDecimal(ipv4Str):
    return [int(octet) for octet in ipv4Str.split('.')]


def convertDecimalToStr(vector):
    return ".".join(str(octet) for octet in vector)


def get_requiermentIpv4InfoForMask(mask, target=30):
    mask_binary = [[0 for bit in range(8)] for octet in range(4)]
    currentBit = 0
    for octet in range(4):
        for bit in range(8):
            mask_binary[octet][bit] = 1 if currentBit < target else 0
            currentBit += 1

    maskStr = convertDecimalToStr(convertBinaryToDecimal(mask_binary))
    if mask == maskStr:
        return target
    elif target < 1:
        raise ValueError("Lenght mask possible exceded")
    else:
        return get_requiermentIpv4InfoForMask(mask, target-1)


def cidrRequiermentForHost(hostNeeded):
    cidr = get_requiermentIpv4InfoForHost(hostNeeded)[1]
    return cidr


def cidrRequiermentForSubnetMask(subnetMask):
    cidr = get_requiermentIpv4InfoForMask(subnetMask)
    return cidr


def get_bitsHost(matrix, cidr):
        bitCurrent = 1
        host = []
        for octet in range(4):
            for bit in range(8):
                if cidr < bitCurrent:
                    host.append(matrix[octet][bit])
                bitCurrent += 1
        return host


def getMinimalCidr(c_class):
        if (c_class == "A") or (c_class == "None"):
            return 8, 8
        elif c_class == "B":
            return 16, 12
        elif c_class == "C":
            return 24, 16
        else:
            return 4, 4


def getMinimalCidrForPrivate(c_class):
    return getMinimalCidr(c_class)[1]


def getMinimalCidrForPublic(c_class):
    return getMinimalCidr(c_class)[0]


def get_bitsNetwork(matrix, cidr):
        bitCurrent = 1
        network = []
        for octet in range(4):
            for bit in range(8):
                if bitCurrent <= cidr:
                    network.append(matrix[octet][bit])
                bitCurrent += 1
        return network


def IETF_is_in(vectorDecimal, cidr):
        test_net_1 = convertDecimalToBinary([192, 0, 2, 0])  # 192.0.2.0 /24
        test_net_2 = convertDecimalToBinary([198, 51, 100, 0])  # 198.51.100.0 /24
        test_net_3 = convertDecimalToBinary([203, 0, 113, 0])  # 203.0.113.0 /24
        networkRef = convertDecimalToBinary(vectorDecimal)
        if isInThisNetwork(networkRef, cidr, test_net_1, 24):
            return True
        elif isInThisNetwork(networkRef, cidr, test_net_2, 24):
            return True
        elif isInThisNetwork(networkRef, cidr, test_net_3, 24):
            return True
        return False


def excludeIETF(vectorDecimal, cidr, choice):
        byte1 = vectorDecimal[0]
        byte2 = vectorDecimal[1]
        byte3 = vectorDecimal[2]
        if IETF_is_in(vectorDecimal, cidr):
            if byte1 == 192:
                if byte2 == 0:
                    if cidr < 22:
                        vectorDecimal[1] = setRandomOctet(choice, [0])
                    elif byte3 == 2:
                         vectorDecimal[2] = setRandomOctet(choice, [2])
            elif byte1 == 198:
                if byte2 == 51:
                    eexcept = [n for n in range(64, 128)]
                    if cidr < 18: 
                        vectorDecimal[1] = setRandomOctet(choice, [51])
                    elif byte3 in eexcept:
                        vectorDecimal[2] = setRandomOctet(choice, eexcept)
            elif byte1 == 203:
                if byte2 == 0:
                    eexcept = [n for n in range(64, 128)]
                    if cidr < 18:
                        vectorDecimal[1] = setRandomOctet(choice, [0])
                    elif byte3 in eexcept:
                        vectorDecimal[2] = setRandomOctet(choice, eexcept)


def isInThisNetwork(networkRef, cidrRef, networkFocus, cidrFocus):
    bitsRef = get_bitsNetwork(networkRef, cidrRef)
    bitsFocus = get_bitsNetwork(networkFocus, cidrFocus)
    if len(bitsRef) < len(bitsFocus):
        for bit in range(len(bitsRef)):
            if bitsRef[bit] != bitsFocus[bit]:
                return False
        return True
    return False


def setRandomOctet(choice, eexcept):
    return choice([n for n in range(256) if n not in eexcept])


def isBadCidrForPrivate(klass, cidr):
        privateCidr = getMinimalCidrForPrivate(klass)
        return cidr < privateCidr


def isBadCidrForPublic(klass, cidr):
        publicCidr = getMinimalCidrForPublic(klass)
        return cidr < publicCidr
