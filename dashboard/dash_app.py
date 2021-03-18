from typing import Any, Dict, List, Optional

from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import flask
import threading
import zmq

from lf_utils.config_utils import instantiate
import lf_utils


class DashApp(threading.Thread):
    """Digital Dashboard web app class -- handles data ingestion and visualization"""

    def __init__(
        self,
        data_port: int,
        machine_configs: Dict[str, Dict],
        update_interval: Optional[float] = 1,
    ):
        """Initializes Dash app and layout, connects to data socket, sets up Dash callbacks

        Parameters
        ----------
        data_port : int
            port to receive data on
        machine_configs : Dict[str, Dict]
            configuration dictionaries for each machine
        update_interval : Optional[float]
            update interval of dashboard, in seconds (by default 1 second)
        """
        # init thread
        super().__init__()

        # set up data socket
        self.context = zmq.Context()
        self.data_socket = self.context.socket(zmq.PULL)
        lf_utils.retry_utils.retry(
            self.data_socket.bind,
            f"tcp://*:{data_port}",
            handled_exceptions=zmq.error.ZMQError,
        )

        # get machine configs
        self.machine_configs = machine_configs

        # create dash app
        self.dash_app = dash.Dash(
            "Digital Dashboard", external_stylesheets=[dbc.themes.DARKLY]
        )
        self.dash_app.layout = html.Div(
            children=[
                html.Div(
                    [
                        instantiate(machine_section)
                        for machine_section in self.machine_configs.values()
                    ],
                    id="dashboard-id",
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=update_interval * 1000,
                    n_intervals=0,
                ),
            ]
        )

        self.dash_app.callback(
            Output("dashboard-id", "children"),
            Input("interval-component", "n_intervals"),
        )(self.update_page)

    def update_page(self, _: int) -> List[dbc.Container]:
        """Updates page using data from data socket

        Parameters
        ----------
        _ : int
            unused param (needed for dash callback)

        Returns
        -------
        List[dbc.Container]
            updated dbc containers
        """
        # get machine configs from socket
        machine_configs = self.data_socket.recv_pyobj()

        # create dbc containers and return them
        return [
            instantiate(machine_section) for machine_section in machine_configs.values()
        ]

    def run(self):
        """Runs dash server."""
        self.dash_app.run_server()

    def shutdown(self):
        """Stops dash server."""
        flask.request.environ.get("werkzeug.server.shutdown")()
