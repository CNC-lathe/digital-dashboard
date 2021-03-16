from typing import Dict

import dash_html_components as html

from lf_utils.config_utils import instantiate


def build_section(**section_conf: Dict) -> html.Div:
    """Builds section component from config

    Parameters
    ----------
    section_conf : Dict
        configuration for section component
        contains information on parent as well as children

    Returns
    -------
    html.Div
        the HTML Div constructed from the config
    """
    return html.Div(children=[
        html.H1(children=section_conf["name"]),
        *(instantiate(component_conf) for component_conf in section_conf["fields"]),
        html.Hr()
    ])