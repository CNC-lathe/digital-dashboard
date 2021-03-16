from typing import Dict

import dash_html_components as html

from lf_utils.config_utils import instantiate


def build_nested_text_component(**nested_text_conf: Dict) -> html.Div:
    """Builds nested text component from config

    Parameters
    ----------
    nested_text_conf : Dict
        configuration for nested text component
        contains information on parent as well as children

    Returns
    -------
    html.Div
        the HTML Div constructed from the config
    """
    return html.Div(children=[
        html.H2(children=nested_text_conf["name"]),
        *(instantiate(text_conf) for text_conf in nested_text_conf["fields"])
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
