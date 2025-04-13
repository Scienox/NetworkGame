def get_octet_binary_count():
    return [128, 64, 32, 16, 8, 4, 2, 1]


def get_requiermentIpInfoForHost(hostNeeded, target=30):
    #tmpIp = IP("0.0.0.0", target)
    totalHost = (2**(32 - target)) - 2
    if hostNeeded <= totalHost:
        return totalHost, target
    elif target < 1:
        raise ValueError("Hosts possible exceded")
    else:
        return get_requiermentIpInfoForHost(hostNeeded, target-1)


def hostsRequiermentNumber(hostNeeded):
    totalHosts = get_requiermentIpInfoForHost(hostNeeded)[0]
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


def convertStrToDecimal(ipStr):
    return [int(octet) for octet in ipStr.split('.')]


def convertDecimalToStr(vector):
    return ".".join(str(octet) for octet in vector)


def get_requiermentIpInfoForMask(mask, target=30):
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
        return get_requiermentIpInfoForMask(mask, target-1)


def cidrRequiermentForHost(hostNeeded):
    cidr = get_requiermentIpInfoForHost(hostNeeded)[1]
    return cidr


def cidrRequiermentForSubnetMask(subnetMask):
    cidr = get_requiermentIpInfoForMask(subnetMask)
    return cidr


def get_bitsHost(ip):
        bitCurrent = 1
        host = []
        for octet in range(4):
            for bit in range(8):
                if ip.cidr < bitCurrent:
                    host.append(ip.ipHostBinary[octet][bit])
                bitCurrent += 1
        return host


def getMinimalCidr(c_class):
        if c_class == "A":
            return 8, 8
        elif c_class == "B":
            return 16, 12
        elif c_class == "C":
            return 24, 16
        else:
            return 4, 4


def get_bitsNetwork(ip):
        bitCurrent = 1
        network = []
        for octet in range(4):
            for bit in range(8):
                if bitCurrent <= ip.cidr:
                    network.append(ip.ipHostBinary[octet][bit])
                bitCurrent += 1
        return network


def isInIETF(vectorDecimal, cidr):
        test_net_1 = [192, 0, 0, 0]
        test_net_2 = [198, 51, 0, 0]
        test_net_3 = [203, 0, 0, 0]
        if vectorDecimal[0:2] == test_net_1[0:2]:
            # cidr 23 minimum
            if cidr < 23:
                return True
        elif vectorDecimal[0:2] == test_net_2[0:2]:
            # cidr 18 minimum
            if cidr < 18 or vectorDecimal[2] in [n for n in range(64, 128)]:
                return True
        elif vectorDecimal[0:2] == test_net_3[0:2]:
            # cidr 18 minimum
            if cidr < 18:
                return True
        return False


def excludeIETF(vectorDecimal, cidr, choice):
        if isInIETF(vectorDecimal, cidr):
            if vectorDecimal[0] == 192:
                vectorDecimal[1] = choice([n for n in range(1, 256)])
            elif vectorDecimal[0] == 198:
                vectorDecimal[1] = choice([n for n in range(0, 256) if n != 51])
                vectorDecimal[2] = choice([n for n in range(0, 64)] + [n for n in range(128, 256)])
            elif vectorDecimal[0] == 203:
                vectorDecimal[1] = choice([n for n in range(1, 256)])
