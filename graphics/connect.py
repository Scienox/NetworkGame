from ip_untils.ip import IP
from ip_untils.helpfunction import cidrRequiermentForHost, cidrRequiermentForSubnetMask
from PySide6.QtWidgets import QTableWidgetItem

def __selectChoiceCidr(choiceDelimiter, delimiterNetwork):
    cidr = None
    if choiceDelimiter == 0:
        cidr = int(delimiterNetwork)
    elif choiceDelimiter == 1:
        cidr = cidrRequiermentForSubnetMask(delimiterNetwork)
    elif choiceDelimiter == 2:
        delimiterTmp = int(delimiterNetwork)
        cidr = cidrRequiermentForHost(delimiterTmp)
    return cidr


def showIpConfig(ip, choiceDelimiter, delimiterNetwork, table):
    cidr = __selectChoiceCidr(choiceDelimiter, delimiterNetwork)

    IpTmp = IP(ip, cidr)

    methodes = [
        "type", "classIP", "reservation",
        "network", "subMask", "cidr",
        "ipHost", "firstHost", "lastHost",
        "broadcast", "totalHost"
        ]
    for row in range(0, len(methodes)):
        methode = methodes[row]
        targetMethode = getattr(IpTmp, methode)
        element = QTableWidgetItem(str(targetMethode))
        table.setItem(row, 0, element)


def detectHostPart(adressBinary, cidr):
    netPart = ""
    hostPart = ""
    adressBinaryToStr = str("".join(str(octet[bit]) for octet in adressBinary for bit in range(8)))
    dotIndex = 0
    for index in range(32):
        dotIndex += 1
        element = str(adressBinaryToStr[index])
        if index < cidr:
            netPart += element + ("." if (dotIndex % 8 == 0 and dotIndex < 25) else '')
        else:
            hostPart += element + ("." if (dotIndex % 8 == 0 and dotIndex < 25) else '')
    return netPart, hostPart


def showBinaryInfo(ip, choiceDelimiter, delimiterNetwork, table):
    cidr = __selectChoiceCidr(choiceDelimiter, delimiterNetwork)

    IpTmp = IP(ip, cidr)

    rowsMethodes = [
        "subMask", "network", "ipHost",
        "firstHost", "lastHost", "broadcast"
    ]
    for row in range(0, len(rowsMethodes)):
        methode = rowsMethodes[row]
        targetMethode = getattr(IpTmp, methode)
        targetMethodeB = getattr(IpTmp, methode + "Binary")
        element = QTableWidgetItem(str(targetMethode))
        table.setItem(row, 0, element)
        netPart, hostPart = detectHostPart(targetMethodeB, cidr)
        elementNetPart = QTableWidgetItem(netPart)
        elementHostPart = QTableWidgetItem(hostPart)
        table.setItem(row, 1, elementNetPart)
        table.setItem(row, 2, elementHostPart)
