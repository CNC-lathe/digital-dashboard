from typing import Dict

import dash_bootstrap_components as dbc
import dash_html_components as html

from lf_utils.config_utils import instantiate


def build_table(**table_conf: Dict) -> html.Div:
    """Builds table component from config

    Parameters
    ----------
    table_conf : Dict
        configuration for table component
        contains information on parent as well as children

    Returns
    -------
    html.Div
        the HTML Div constructed from the config
    """
    return html.Div(children=[
        html.H3(children=table_conf["name"], style={"text-decoration": "underline"}),
        dbc.Table(
            [html.Tr([html.Th(col["name"]) for col in table_conf["fields"]])] +
            [html.Tr([html.Td(f"{col['data']} {col['postfix']}") for col in table_conf["fields"]])],
            bordered=True
        )
    ])