import asyncio
from os import system

from base_classes.proxy_q_holder import ProxyQ
from launcher.base import ProxyServerLauncher
from utils.custom_logger import logger


async def run(num_tasks_to_run: int = 5):
    proxy_q: ProxyQ = ProxyQ.instance()
    proxy_q.populate_to_chk_gateways()
    tasks = (
        *(ProxyServerLauncher().wait_for_good_proxy() for _ in range(num_tasks_to_run)),
    )
    try:
        await asyncio.gather(*tasks)
    finally:
        for proxy_server in proxy_q.proxy_servers:
            await proxy_server.stop_port()
        logger().info('All Servers Closed.')


if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        import win32file

        # asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        win32file._setmaxstdio(8192)

    system('taskkill /F /IM 3proxy.exe')
    asyncio.get_event_loop().run_until_complete(run(10))