from ip_untils.ip import IP


class Subnet:
    def __init__(self, ipHost, totalHost, cidr, subMask, network, firstHost, lastHost, broadcast, nextNetwork, reservation, classIP):
        self.score_ = 0
        self.feedBack = []
        self.ipHost = ipHost
        self.totalHost = int(totalHost)
        self.cidr = int(cidr)
        self.subMask = subMask
        self.network = network
        self.firstHost = firstHost
        self.lastHost = lastHost
        self.broadcast = broadcast
        self.nextNetwork = nextNetwork
        self.reservation = reservation
        self.classIP = classIP

    def __eq__(self, ip):
        feedBack = []
        self.score_ = 0
        if isinstance(ip, IP):
            if not self.ifHost(ip):
                feedBack.append(f"- Error @Ipv4: {self.ipHost}\n\tCorrect -> {ip.ipHost}\n")
            if not self.ifTotalHost(ip):
                feedBack.append(f"- Error total host: {self.totalHost}\n\tCorrect -> {ip.totalHost}\n")
            if not self.ifCidr(ip):
                feedBack.append(f"- Error CIDR: {self.cidr}\n\tCorrect -> {ip.cidr}\n")
            if not self.ifSubNetMask(ip) :
                feedBack.append(f"- Error Subnet Mask: {self.subMask}\n\tCorrect -> {ip.subMask}\n")
            if not self.ifNetwork(ip):
                feedBack.append(f"- Error @network: {self.network}\n\tCorrect -> {ip.network}\n")
            if not self.ifFirstHost(ip):
                feedBack.append(f"- Error first host: {self.firstHost}\n\tCorrect -> {ip.firstHost}\n")
            if not self.ifLastHost(ip):
                feedBack.append(f"- Error last host: {self.lastHost}\n\tCorrect -> {ip.lastHost}\n")
            if not self.ifBroadcast(ip):
                feedBack.append(f"- Error @broadcast: {self.broadcast}\n\tCorrect -> {ip.broadcast}\n")
            if not self.ifNextNetwork(ip):
                feedBack.append(f"- Error next @network: {self.nextNetwork}\n\tCorrect -> {ip.get_next_network(30).network}\n")
            if not self.ifClassIP(ip):
                feedBack.append(f"- Error class ip: {self.classIP}\n\tCorrect -> {ip.classIP}\n")
            if not self.ifReservation(ip):
                feedBack.append(f"- Error reservation: {self.reservation}\n\tCorrect -> {ip.reservation}\n")

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

    def ifCidr(self, ip):
        if self.cidr == ip.cidr:
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

    def ifNextNetwork(self, ip):
        if self.nextNetwork == ip.get_next_network(30).network:
            self.score_ += 1
            return True
        return False

    def ifClassIP(self, ip):
        if self.classIP == ip.classIP:
            self.score_ += 1
            return True
        return False

    def ifReservation(self, ip):
        if self.reservation == ip.reservation:
            self.score_ += 1
            return True
        return False
