from ip_untils.ip import IP
from ip_untils.helpfunction import cidrRequiermentForHost, cidrRequiermentForSubnetMask
from PySide6.QtWidgets import QTableWidgetItem


def showIpConfig(ip, choiceDelimiter, delimiterNetwork, table):
    if choiceDelimiter == 0:
        cidr = int(delimiterNetwork)
    elif choiceDelimiter == 1:
        cidr = cidrRequiermentForSubnetMask(delimiterNetwork)
    elif choiceDelimiter == 2:
        delimiterTmp = int(delimiterNetwork)
        cidr = cidrRequiermentForHost(delimiterTmp)

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
