from typing import Any, Dict

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import flask
import zmq

from lf_utils.config_utils import instantiate
import lf_utils


class DashApp:
    """Digital Dashboard web app class -- handles data ingestion and visualization"""
    def __init__(self, data_port: int, machine_configs: Dict[str, Dict]):
        """Initializes Dash app and layout, connects to data socket, sets up Dash callbacks

        Parameters
        ----------
        data_port : int
            port to receive data on
        machine_configs : Dict[str, Dict]
            configuration dictionaries for each machine
        """
        # set up data socket
        self.context = zmq.Context()
        self.data_socket = self.context.socket(zmq.PULL)
#        lf_utils.retry_utils.retry(
#            self.data_socket.bind, f"tcp://*:{data_port}", handled_exceptions=zmq.error.ZMQError
#        )

        # get machine configs
        self.machine_configs = machine_configs

        # create dash app
        self.dash_app = dash.Dash("Digital Dashboard", external_stylesheets=[dbc.themes.DARKLY])
        self.dash_app.layout = html.Div(children=[
            instantiate(machine_section)
            for machine_section in self.machine_configs.values()
        ])

    def run(self):
        """Runs dash server."""
        self.dash_app.run_server(debug=True)

    def shutdown(self):
        """Stops dash server."""
        flask.request.enviorn.get("werkzeug.server.shutdown")()
