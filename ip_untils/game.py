from .ip import IP
from .vlsm import VLSM
from .subnet import Subnet
from random import randint, seed


class Game:
    def __init__(self, steps=1):
        self.steps = steps
        self.ipHost = f"{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"
        self.ipHost = IP(self.ipHost, randint(0, 30))

    def start(self):
        print("\n-------- < Game started > --------")
        print(f"\n@Ip: {self.ipHost.ipHost}\tCIDR: {self.ipHost.cidr} ",end="\n\n")
        ipHost = input("@Ip: ")
        totalHost = input("Max host: ")
        cidr = input("CIDR: ")
        subMask = input("SubNetMask: ")
        network = input("@Network: ")
        firstHost = input("First host: ")
        lastHost = input("Last host: ")
        broadcast = input("@Broadcast: ")
        nextNetwork = input("Next network: ")
        reservation = input("Reservation: ")
        classIP = input("Class: ")
        response = Subnet(
            ipHost,
            totalHost,
            cidr,
            subMask,
            network,
            firstHost,
            lastHost,
            broadcast,
            nextNetwork,
            reservation,
            classIP,
        )
        print("\n", "You win!" if self.ipHost == response else f"You lose! ({response.score_}/11)\n{''.join(str(element) for element in response.feedBack)}")
        print(end="-------- < End game > --------\n")
        