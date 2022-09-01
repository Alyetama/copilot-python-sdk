#!/usr/bin/env python
# coding: utf-8
"""
You must have a function named `main` that runs this module.
This file is the equivalent to `rFunction.R`
"""

import pandas as pd
from loguru import logger

from copilot_sdk import PyCopilotSDK


def hello_world(data: pd.DataFrame):
    """
    This is an example funciton that plots ground_speed over time and export it
    to a pdf file `hello_world.pdf`. You can use this as a template for your
    own functions. Remember that any keyword argument you specify here
    should have a key-value pair in `cfg.json`.

    Args:
        data (pandas.DataFrame): The dataframe containing the data to be
            plotted.
    """

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    p = data.plot(x='timestamp', y='ground_speed')
    p.figure.savefig('hello-world.pdf')
    logger.info('Exported the plot to: hello-world.pdf')


def main():
    # -------------------------------------------------------------------------
    # Initialize the SDK class object
    sdk = PyCopilotSDK()
    # Load your config
    config = sdk.load_config()
    logger.info(f'Current configuration: {config}')
    # Load the rds data, as specified in cfg.json, into a pandas dataframe.
    # Note: If you want to load multiple data files, you can simply call the
    #    method multiple times on each data file key you have in `cfg.json`,
    #    and pass the key name to the method
    #    (e.g., `data2 = sdk.load_data('source_file_2')`).
    data = sdk.load_data()
    # -------------------------------------------------------------------------

    # Add your function(s) here:
    hello_world(data)


if __name__ == '__main__':
    main()
    logger.info('Done!')
