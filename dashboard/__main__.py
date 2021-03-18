import yaml
from .dash_app import DashApp

import lf_utils.yaml_loader


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Runs the digital dashboard server")
    parser.add_argument(
        "--machine_config_path", default="learning-factory-machine-configs/conf.yaml"
    )
    parser.add_argument("--data_port", default=41952, type=int)

    args = parser.parse_args()

    # load machine config
    with open(args.machine_config_path, "r") as machine_conf_file:
        machine_config = yaml.load(
            machine_conf_file, Loader=lf_utils.yaml_loader.Loader
        )

    # instantiate dash app
    dash_app = DashApp(args.data_port, machine_config)

    # run dash server
    dash_app.run()
