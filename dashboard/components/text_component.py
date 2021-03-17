from typing import Dict

import dash_bootstrap_components as dbc
import dash_html_components as html

from lf_utils.config_utils import instantiate


def build_row(**row_conf: Dict) -> html.Div:
    """Builds text row component from config

    Parameters
    ----------
    row_conf : Dict
        configuration for row text component
        contains information on parent as well as children

    Returns
    -------
    html.Div
        the HTML div constructed from the config
    """
    return html.Div(children=[
        html.H3(children=row_conf["name"], style={"text-decoration": "underline"}),
        dbc.Row([*(dbc.Col(instantiate(text_conf)) for text_conf in row_conf["fields"])])
    ])


def build_text_component(**text_conf: Dict) -> html.Pre:
    """Builds text component from config

    Parameters
    ----------
    text_conf : Dict
        configuration for text component

    Returns
    -------
    html.Pre
        the HTML Pre component constructed from the config
    """
    return html.Pre(children=f"{text_conf['name']}: {text_conf['data']} {text_conf['postfix']}")
