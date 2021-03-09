from typing import Any, Dict

import zmq


class DashApp:
    """Digital Dashboard web app class -- handles data ingestion and visualization"""
    def __init__(self, data_port: int, machine_configs: Dict[Dict]):
        """Initializes Dash app and layout, connects to data socket, sets up Dash callbacks

        Parameters
        ----------
        data_port : int
            port to receive data on
        machine_configs : Dict[Dict]
            configuration dictionaries for each machine
        """
        # set up data socket
        self.context = zmq.Context()
        self.data_socket = self.context.socket(zmq.PULL)
        self.data_socket.bind(f"tcp://*:{data_port}")

        # get machine configs
        self.machine_configs = machine_configs
