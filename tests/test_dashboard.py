import copy
import unittest

import yaml

from dashboard.dash_app import DashApp
import lf_utils


class DigitalDashboardTests(unittest.TestCase):
    """Tests digital dashboard methods."""
    def setUp(self):
        with open("tests/test_configs/test_merge_config.yaml", "r") as machine_conf_file:
            self.dashboard_configs = {"example": yaml.load(machine_conf_file, Loader=lf_utils.yaml_loader.Loader)}

        # init dash app
        self.dash_app = DashApp(49160, copy.deepcopy(self.dashboard_configs))

    def test_merge_dashboard_configs(self):
        """Tests merging machine data into dashboard configs."""
        test_machine_data = {
            "example": {
                "example_table": {
                    "a": 5,
                    "b": 6,
                },
                "example_row": {
                    "c": "test",
                    "d": "test2",
                }
            }
        }

        # merge machine data
        merged_dashboard_config = self.dash_app.merge_machine_data(test_machine_data)

        # assert that merged dashboard config has values set correctly
        self.assertEqual(merged_dashboard_config["example"]["fields"][0]["fields"][0]["data"], 5)
        self.assertEqual(merged_dashboard_config["example"]["fields"][0]["fields"][1]["data"], 6)
        self.assertEqual(merged_dashboard_config["example"]["fields"][1]["fields"][0]["data"], "test")
        self.assertEqual(merged_dashboard_config["example"]["fields"][1]["fields"][1]["data"], "test2")

