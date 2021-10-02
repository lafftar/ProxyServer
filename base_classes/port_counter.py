from utils.singleton import Singleton

BASE_PORT = 4000


@Singleton
class PortCounter:
    def __init__(self):
        self.current_port_number = BASE_PORT

    def set_base_port(self, base_port):
        self.current_port_number = base_port
