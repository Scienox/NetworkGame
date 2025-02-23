from ip_untils.ip import IP
from ip_untils.vlsm import VLSM
from ip_untils.helpfunction import cidrRequiermentForHost, cidrRequiermentForSubnetMask
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView


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
            netPart += element + (" ." if (dotIndex % 8 == 0 and dotIndex < 25) else '') + ' '
        else:
            hostPart += element + (" ." if (dotIndex % 8 == 0 and dotIndex < 25) else '') + ' '
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


def addNetwork(table):
    columnCount = table.columnCount()
    table.insertColumn(columnCount)
    table.setColumnWidth(columnCount, 100)


def removeNetwork(table):
    columnCurrent = table.currentColumn()
    table.removeColumn(columnCurrent)
    

def readTable(table):
    rows = table.rowCount()
    columns = table.columnCount()
    for row in range(rows):
        for column in range(columns):
            yield table.item(row, column)


def readColumnTable(table, row):
    columns = table.columnCount()
    for column in range(columns):
        yield table.item(row, column)


def getNameNetwork(table):
    columns = table.columnCount()
    for column in range(columns):
        name, numberHost = table.item(0, column), table.item(1, column)
        yield name, numberHost


def readVlsm(vlsm):
    for subNetwork in vlsm.subNetworks:
        yield subNetwork


def makeVlsm(tableNetwork, tableVlsm, subDivisedNetwork, choiceDelimiter, delimiterNetwork):
    tableVlsm.setRowCount(0)
    updateRowSizeTable(tableVlsm, 20)
    subNetwork = ","
    subNetwork = subNetwork.join(f"{name.text() if name != None else ''}:{numberHost.text()}" for name,
                                  numberHost in getNameNetwork(tableNetwork))
    cidr = __selectChoiceCidr(choiceDelimiter, delimiterNetwork)
    vlsm = VLSM(subDivisedNetwork, cidr, subNetwork)
    rowCurrent = tableVlsm.rowCount()
    methodes = ["name", "subMask", "network", "totalHost", "cidr"]

    for subnet_work in readVlsm(vlsm):
        tableVlsm.insertRow(rowCurrent)
        updateRowSizeTable(tableVlsm, 20)
        for methodeCurrent in range(len(methodes)):
            methode = methodes[methodeCurrent]
            ipInfo = getattr(subnet_work, methode)
            newItem = QTableWidgetItem(str(ipInfo))
            tableVlsm.setItem(rowCurrent, methodeCurrent, newItem)
        rowCurrent += 1


def updateRowSizeTable(table, labelSize=0):
    table.setFixedHeight(table.rowHeight(0) * table.rowCount() + labelSize)


def tableNoResizeRow(table):
    verticalHeader = table.verticalHeader()
    verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
