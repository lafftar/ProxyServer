import asyncio
import shutil
import sys
from asyncio import sleep, subprocess
from aiofiles import open as aopen
from os import getcwd, chdir
from aioshutil import copytree
from typing import Union

from base_classes.base import Base
from base_classes.port_counter import PortCounter
from base_classes.proxy_q_holder import ProxyQ
from utils.root import get_project_root

PATH, EXEC_PATH = None, None

if sys.platform == 'win32':
    PATH = 'bin64'
    EXEC_PATH = '3proxy.exe'

if sys.platform == 'linux':
    PATH = 'bin'
    EXEC_PATH = '3proxy 3proxy.cfg'


with open(f'{get_project_root()}/base_3proxy/3proxy/{PATH}/3proxy.cfg', 'r') as file:
    BASE_CONFIG = [line.strip() for line in file.readlines()]


class BaseLauncher(Base):
    def __init__(self):
        super().__init__()
        self.proxy_ip, self.proxy_port, self.proxy_user, self.proxy_passwd, self.actual_ip = (None for _ in range(5))
        self.proxy_q_holder: ProxyQ = ProxyQ.instance()
        self.port_counter: PortCounter = PortCounter.instance()
        self.port_counter.current_port_number += 1
        self.port = self.port_counter.current_port_number
        self.current_config: str = ''
        self.port_process: Union[asyncio.subprocess.Process, None] = None
        self.port_directory = f'{get_project_root()}/_PORTS_/{self.port}'
        self.base_config = BASE_CONFIG

    def prnt_frmt(self, text):
        return f'[Port {self.port}]: {text}'

    async def make_port_files(self):
        """
        copy all the files from base to this directory
        copytree() makes the directories needed recursively.
        """
        while True:
            try:
                await copytree(
                    src=f'{get_project_root()}/base_3proxy/3proxy/',
                    dst=self.port_directory,
                    dirs_exist_ok=True
                )
                break
            except shutil.Error as esx:
                # self.exception(f'{esx}')
                # input()
                # print('failed')
                await self.stop_port()
                continue
        self.debug('All Port Files Created')

    async def edit_port_cfg(self):
        cfg_file = f'{self.port_directory}/{PATH}/3proxy.cfg'
        async with aopen(cfg_file, 'w') as file:
            await file.write(self.current_config)
        self.debug('Config Edited Successfully')

    async def start_port(self):
        cwd = getcwd()
        chdir(f'{self.port_directory}/{PATH}/')
        if sys.platform == 'linux':
            self.port_process = await asyncio.create_subprocess_shell(f'{EXEC_PATH}',
                                                                     stdout=subprocess.PIPE)
        if sys.platform == 'win32':
            self.port_process = await asyncio.create_subprocess_exec(f'{EXEC_PATH}',
                                                                      stdout=subprocess.PIPE)
        self.debug('Port Started')
        chdir(cwd)
        await sleep(0.5)

    async def stop_port(self):
        if self.port_process:
            self.port_process.kill()
            self.debug('Port Killed')
            # just waiting for the port to actually die.
            await sleep(5)
