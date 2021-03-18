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
    return html.Div(
        children=[
            html.H3(
                children=table_conf["name"], style={"text-decoration": "underline"}
            ),
            dbc.Table(
                [
                    html.Tr(
                        [
                            html.Th(
                                fixed_width(f"{col['name']}", 25),
                                style={"white-space": "pre-wrap"},
                            )
                            for col in table_conf["fields"]
                        ]
                    )
                ]
                + [
                    html.Tr(
                        [
                            html.Td(
                                fixed_width(f"{col['data']} {col['postfix']}", 25),
                                style={"white-space": "pre-wrap"},
                            )
                            if not isinstance(col["data"], float)
                            else html.Td(
                                fixed_width(f"{col['data']:.3f} {col['postfix']}", 25),
                                style={"white-space": "pre-wrap"},
                            )
                            for col in table_conf["fields"]
                        ]
                    )
                ],
                bordered=True,
            ),
        ]
    )


def fixed_width(in_str: str, width: int) -> str:
    """Creates fixed width string of width <width>

    Parameters
    ----------
    in_str : str
        input string
    width : int
        width of string

    Returns
    -------
    str
        fixed width string
    """
    return f"{in_str:<{width}}"
