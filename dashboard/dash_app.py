from typing import Any, Dict

import zmq


class DashApp:
    """Digital Dashboard web app class -- handles data ingestion and visualization"""
    def __init__(
        self, data_port: int, publish_port: int, machine_configs: Dict[Dict]
    ):
        """Initializes Dash app and layout, connects to data socket, sets up Dash callbacks

        Parameters
        ----------
        data_port : int
            port to receive data on
        machine_configs : Dict[Dict]
            configuration dictionaries for each machine
        """

