from typing import Any, Dict, List, Optional
import copy

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
        dashboard_configs: Dict[str, Dict],
        update_interval: Optional[float] = 1,
    ):
        """Initializes Dash app and layout, connects to data socket, sets up Dash callbacks

        Parameters
        ----------
        data_port : int
            port to receive data on
        dashboard_configs : Dict[str, Dict]
            configuration dictionaries for each machine's display on dashboard
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

        # get dashboard configs for each machine
        self.dashboard_configs = dashboard_configs

        # create dash app
        self.dash_app = dash.Dash(
            "Digital Dashboard", external_stylesheets=[dbc.themes.DARKLY]
        )
        self.dash_app.layout = html.Div(
            children=[
                html.Div(
                    [
                        instantiate(machine_section)
                        for machine_section in self.dashboard_configs.values()
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
        # get machine data from socket
        machine_data = self.data_socket.recv_pyobj()

        # merge machine data with dashboard configs
        dashboard_configs = self.merge_machine_data(machine_data)

        # create dbc containers and return them
        return [
            instantiate(machine_section) for machine_section in dashboard_configs.values()
        ]

    def run(self):
        """Runs dash server."""
        self.dash_app.run_server()

    def shutdown(self):
        """Stops dash server."""
        flask.request.environ.get("werkzeug.server.shutdown")()

    def merge_machine_data(self, machine_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """Merges machine data with dashboard configs to allow machine data to be displayed.

        Parameters
        ----------
        machine_data : Dict[str, Dict]
            machine data dictionaries (values of machine parameters)

        Returns
        -------
        Dict[str, Dict]
            machine dashboard dictionaries (with data filled out for each field)
        """
        # create copy of dashboard configs
        dashboard_configs = copy.deepcopy(self.dashboard_configs)

        for machine_name, machine_data_dict in machine_data.items():
            # merge machine data into config
            self._merge_machine_data(dashboard_configs[machine_name], machine_data_dict)
        
        return dashboard_configs

    def _merge_machine_data(self, dashboard_config: Dict[str, Dict], machine_data: Dict[str, Any]):
        """Recursive implementation of machine data merging.

        Parameters
        ----------
        dashboard_config : Dict[str, Dict]
            dashboard config to update with machine data
        machine_data : Dict[str, Any]
            machine data dictionary
        """
        for data_id, data_val in machine_data.items():
            if isinstance(data_val, dict):
                self._merge_machine_data(dashboard_config, data_val)

            else:
                self._fill_field_from_id(data_id, data_val, dashboard_config)

    def _fill_field_from_id(self, data_id: str, data_val: Any, dashboard_config: Dict[str, Any]):
        """Fills data id field with data val in dashboard config.

        Parameters
        ----------
        data_id : str
            id to target in dashboard config
        data_val : Any
            value to update with
        dashboard_config : Dict[str, Any]
            dashboard config to mutate
        """
        for k, v in dashboard_config.items():
            if k == "id" and v == data_id:
                dashboard_config["data"] = data_val

            elif isinstance(v, list):
                for conf_dict in v:
                    self._fill_field_from_id(data_id, data_val, conf_dict)

            elif isinstance(v, dict):
                self._fill_field_from_id(data_id, data_val, v)
