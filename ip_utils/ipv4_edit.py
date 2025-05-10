from .ipv4 import Ipv4


class Ipv4Edit:
    def __init__(self, classIpv4, typeIpv4, reservation, ipv4Host, subMask, network, totalHost, firstHost, lastHost, broadcast, nextNetwork):
        self.score_ = 0
        self.feedBack = []
        self.ipHost = ipv4Host
        try:
            self.totalHost = int(totalHost)
        except:
            self.totalHost = 'None'
        self.subMask = subMask
        self.network = network
        self.firstHost = firstHost
        self.lastHost = lastHost
        self.broadcast = broadcast
        self.nextNetwork = nextNetwork
        self.reservation = reservation
        self.classIpv4 = classIpv4
        self.typeIpv4 = typeIpv4

    def __eq__(self, ipv4:Ipv4):
        feedBack = []
        self.score_ = 0
        if isinstance(Ipv4, Ipv4):
            if not self.ifHost(ipv4):
                feedBack.append(f"- Wrong @Ipv4: {self.ipHost}\n\tCorrect -> {ipv4.ipHost}\n")
            if not self.ifTotalHost(ipv4):
                feedBack.append(f"- Wrong total host: {self.totalHost}\n\tCorrect -> {ipv4.totalHost}\n")
            if not self.ifSubNetMask(ipv4) :
                feedBack.append(f"- Wrong Subnet Mask: {self.subMask}\n\tCorrect -> {ipv4.subMask}\n")
            if not self.ifNetwork(ipv4):
                feedBack.append(f"- Wrong @network: {self.network}\n\tCorrect -> {ipv4.network}\n")
            if not self.ifFirstHost(ipv4):
                feedBack.append(f"- Wrong first host: {self.firstHost}\n\tCorrect -> {ipv4.firstHost}\n")
            if not self.ifLastHost(ipv4):
                feedBack.append(f"- Wrong last host: {self.lastHost}\n\tCorrect -> {ipv4.lastHost}\n")
            if not self.ifBroadcast(ipv4):
                feedBack.append(f"- Wrong @broadcast: {self.broadcast}\n\tCorrect -> {ipv4.broadcast}\n")
            if not self.ifNextNetwork(ipv4):
                feedBack.append(f"- Wrong next @network: {self.nextNetwork}\n\tCorrect -> {self.get_next_network(ipv4)}\n")
            if not self.ifClassIP(ipv4):
                feedBack.append(f"- Wrong class ip: {self.classIP}\n\tCorrect -> {ipv4.classIP}\n")
            if not self.ifReservation(ipv4):
                feedBack.append(f"- Wrong reservation: {self.reservation}\n\tCorrect -> {ipv4.reservation}\n")
            if not self.ifType(ipv4):
                feedBack.append(f"- Wrong type: {self.typeIp}\n\tCorrect -> {ipv4.type}\n")

            self.feedBack = feedBack.copy()

            if self.score_ == 11:
                return True
            
            return False

        else:
            return NotImplemented

    def ifHost(self, ip):
        if self.ipHost == ip.ipHost:
            self.score_ += 1
            return True
        return False

    def ifTotalHost(self, ip):
        if self.totalHost == ip.totalHost:
            self.score_ += 1
            return True
        return False

    def ifSubNetMask(self, ip):
        if self.subMask == ip.subMask:
            self.score_ += 1
            return True
        return False

    def ifNetwork(self, ip):
        if self.network == ip.network:
            self.score_ += 1
            return True
        return False

    def ifFirstHost(self, ip):
        if self.firstHost == ip.firstHost:
            self.score_ += 1
            return True
        return False

    def ifLastHost(self, ip):
        if self.lastHost == ip.lastHost:
            self.score_ += 1
            return True
        return False

    def ifBroadcast(self, ip):
        if self.broadcast == ip.broadcast:
            self.score_ += 1
            return True
        return False

    def ifNextNetwork(self, ip:Ipv4):
        nextNetwork = ip.get_next_network(30)
        if isinstance(nextNetwork, Ipv4):
            if self.nextNetwork == nextNetwork.network:
                self.score_ += 1
                return True
        else:
            if self.nextNetwork == nextNetwork:
                self.score_ += 1
                return True
            return False


    def ifClassIP(self, ipv4):
        if self.classIP == ipv4.classIP:
            self.score_ += 1
            return True
        return False

    def ifReservation(self, ipv4):
        if self.reservation == ipv4.reservation:
            self.score_ += 1
            return True
        return False
    
    def ifType(self, ipv4:Ipv4):
        if self.typeIp == ipv4.type:
            self.score_ += 1
            return True
        else:
            return False

    def get_next_network(self, ipv4:Ipv4):
        try:
            return ipv4.get_next_network(30).network
        except:
            return ''
        
    @property
    def show_display(self):
        for row in self.feedBack:
            print(row)
