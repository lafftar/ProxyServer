"""
This class simply holds the good_gateways and gateways_to_check Q. It's a singleton, so it should return the
same instance for all calling classes.

@todo
Save good proxies, maybe we can track what it takes to get proxies banned.
And what it takes to get them unbanned.
"""
import asyncio
from dataclasses import dataclass
from os import listdir
from random import shuffle

from base_classes.base import Base
from utils.root import get_project_root
from utils.singleton import Singleton


@Singleton
class ProxyQ(Base):
    def __init__(self):
        """

        :param mode: the folder to grab gateways from, possible gateways
        are in the dataclass @ProxyQModes
        """
        super().__init__()
        self.gateways: asyncio.Queue = asyncio.Queue()
        self.proxy_servers: list = []

    def prnt_frmt(self, text):
        return f'[--ProxyQ--]: {text}'

    def populate_to_chk_gateways(self):
        # build a shuffled q to pull proxies from.
        with open(fr'{get_project_root()}/gateways/isps.txt') as file:
            proxies = [line.strip() for line in file.readlines()]
        shuffle(proxies)
        for gateway in proxies:
            self.gateways.put_nowait(gateway)
        self.debug(f'There are {self.gateways.qsize()} gateways in Q')


if __name__ == "__main__":
    ProxyQ.instance().populate_to_chk_gateways()