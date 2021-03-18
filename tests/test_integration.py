"""Tests integration with mocked LF server."""
from typing import Any, Dict, Type
import copy
import random
import string
import time

import pytest
import threading
import yaml
import zmq

from dashboard.dash_app import DashApp
import lf_utils


class MockLFServer(threading.Thread):
    """Mocks LFServer digital dashboard output."""
    def __init__(self, data_port: int, machine_configs: Dict[str, Dict], update_interval: float):
        """Initializes mock LF server

        Parameters
        ----------
        data_port : int
            port to publish data to
        machine_configs : Dict[str, Dict]
            machine configs to send
        update_interval : float
            interval to send data at
        """
        # init thread
        super().__init__()

        # set orig machine configs
        self.orig_machine_configs = machine_configs

        # create digital dashboard, virtual factory sockets
        self._context = zmq.Context()

        digital_dash_address = f"tcp://127.0.0.1:{data_port}"
        self._digital_dash_socket = self._context.socket(zmq.PUSH)
        lf_utils.retry_utils.retry(
            self._digital_dash_socket.connect,
            digital_dash_address,
            handled_exceptions=zmq.error.ZMQError
        )

        self.update_interval = update_interval

        self.stopped = False

    def run(self):
       """Sends randomized data over socket at update rate."""
       while not self.stopped:
           generated_data = self._gen_data(copy.deepcopy(self.orig_machine_configs))
           self._digital_dash_socket.send_pyobj(generated_data)

           time.sleep(self.update_interval)

    def stop(self):
        """Asynchonously stops mock lf server thread."""
        self.stopped = True

    def _gen_data(self, machine_configs: Dict[str, Any]) -> Dict[str, Any]:
        """Generates randomized data

        Parameters
        ----------
        machine_configs : Dict[str, Any]
            machine configs, to use to generate data

        Returns
        ----------
        Dict[str, Any]
            machine configs with generated data
        """
        for k, v in machine_configs.items():
            if isinstance(v, dict):
                machine_configs[k] = self._gen_data(v)

            elif isinstance(v, list):
                for ii, el in enumerate(v):
                    if isinstance(el, dict):
                        v[ii] = self._gen_data(el)

            elif k == "data":
                machine_configs[k] = self._gen_random_val(type(v))

        return machine_configs

    def _gen_random_val(self, data_type: Type) -> Any:
        """Generates random value of type <data_type>

        Parameters
        ----------
        data_type : Type
            type of random val to generate

        Returns
        -------
        Any
            random value, of type <data_type>

        Raises
        ------
        TypeError
            If data type is not one of [str, bool, int, float]
        """
        if data_type is str:
            return "".join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 20)))

        elif data_type is bool:
            return random.choice([True, False])

        elif data_type in [int, float]:
            return random.gauss(0, 10)

        else:
            raise TypeError(f"Type {data_type} cannot be used to generate a random value")


def test_integration(update_interval: float):
    """Runs dash app, mock LF server

    Parameters
    ----------
    update_interval : float
        update interval for MockLFServer
    """
    # load machine configs from file
    with open("learning-factory-machine-configs/conf.yaml", "r") as machine_conf_file:
        machine_configs = yaml.load(machine_conf_file, Loader=lf_utils.yaml_loader.Loader)

    # init dash app
    dash_app = DashApp(49160, copy.deepcopy(machine_configs))

    # init mock lf server
    mock_lf_server = MockLFServer(49160, copy.deepcopy(machine_configs), update_interval=update_interval)

    # start dash app
    dash_app.start()

    # start mock lf server
    mock_lf_server.start()

    # wait for user to exit
    input("Press any key to go to next test")

    # stop lf server
    mock_lf_server.stop()


if __name__ == "__main__":
    update_interval = 1.0

    test_integration(update_interval)
