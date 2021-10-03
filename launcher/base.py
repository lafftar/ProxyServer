"""
this just launches proxy servers
will wait to receive good IPs, then will launch sequentially
will handle ACLs, which IPs are allowed to access which ports
"""
from asyncio import sleep

from base_classes.base_launcher import BaseLauncher


class ProxyServerLauncher(BaseLauncher):
    def __init__(self):
        super().__init__()

    async def make_current_config(self):
        self.current_config = ''
        for line in self.base_config:
            # the proxies we forward to
            if 'parent' in line:
                self.current_config += 'parent 1000 '
                # the actual proxy
                proxy = f"http {self.proxy_ip} {self.proxy_port} {self.proxy_user} {self.proxy_passwd}"
                self.current_config += proxy
                self.current_config += '\n'
                continue

            # change the port
            if 'proxy' in line:
                self.current_config += f'proxy -a -p{self.port} -osTCP_NODELAY -ocTCP_NODELAY\n'
                continue
            self.current_config += f'{line}\n'
        self.debug(f'\n'
                  f'Current Config\n\n'
                  f'{self.current_config}')

    async def wait_for_good_proxy(self):
        await self.make_port_files()
        self.debug('Waiting for good proxy.')
        gateway= await self.proxy_q_holder.gateways.get()
        gateway = ":".join(gateway.split('@'))
        gateway = gateway.split(':')
        self.proxy_user, self.proxy_passwd = None, None
        self.proxy_ip, self.proxy_port = gateway
        await self.make_current_config()
        await self.edit_port_cfg()
        await self.start_port()
        self.proxy_q_holder.proxy_servers.append(self)
        await sleep(604800)
