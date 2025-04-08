class IpManager:
    def __init__(self, klass=None, reservation=None,
                 ttype=None, cidr=None):
        self.klass = klass
        self.reservation = reservation
        self.ttype = ttype
        self.cidr = cidr

        minimal, maximal = self.getRangeAvaible()
        self.minimalRange = minimal
        self.maximalRange = maximal

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
            if self.reservation == 'public':
                return "192.168.0.0", "192.168.255.255"
            else:
                return "192.0.0.0", "192.167.255.255", "193.0.0.0", "223.255.255.255"
    
    def getMinimalCidr(self):
        current = 0 if self.reservation == 'private' else 1
        return self._getMinimalCidr()[current]

    def _getMinimalCidr(self):
        if self.klass == "A":
            return 8, 8
        elif self.klass == "B":
            return 16, 12
        elif self.klass == "C":
            return 24, 16
        else:
            return 4, 4
