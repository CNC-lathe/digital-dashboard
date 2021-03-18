from typing import Dict

import dash_bootstrap_components as dbc
import dash_html_components as html

from lf_utils.config_utils import instantiate


def build_section(**section_conf: Dict) -> dbc.Container:
    """Builds section component from config

    Parameters
    ----------
    section_conf : Dict
        configuration for section component
        contains information on parent as well as children

    Returns
    -------
    dbc.Container
        the DBC container constructed from the config
    """
    return dbc.Container(
        children=[
            html.H1(
                children=section_conf["name"], style={"text-decoration": "underline"}
            ),
            *(instantiate(component_conf) for component_conf in section_conf["fields"]),
            html.Hr(),
        ]
    )
