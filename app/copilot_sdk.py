#!/usr/bin/env python
# coding: utf-8

import json
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, Optional, Union

import pandas as pd
import rpy2.robjects as robjects
from loguru import logger


class MissingSourceDataError(Exception):
    pass


class PyCopilotSDK:

    def __init__(self, config_file: str = '/config/cfg.json'):
        self.config_file = config_file

    def load_config(self) -> Optional[dict]:
        """Loads the config file and returns a dictionary.

        Returns:
            dict: The config dictionary.
        """
        if not Path(self.config_file).exists():
            logger.warning(
                'Could not find a config file in the app/ directory!')
            return
        with open(self.config_file) as j:
            return json.load(j)

    def load_data(self,
                  source_file: Optional[Union[Iterable, str]] = None,
                  save_raw_csv: bool = False,
                  save_compressed_csv: bool = False) -> pd.DataFrame:
        """Loads the data from the source file(s) and returns a pandas
        dataframe.

        Args:
            source_file (Union[Iterable, str], optional): The source file(s)
                to be loaded. If None, the source file(s) specified in the
                config file will be loaded. Defaults to None.
            save_raw_csv (bool, optional): Whether to save the raw csv file.
                Defaults to False.
            save_compressed_csv (bool, optional): Whether to save the
                compressed csv file. Defaults to False.

        Returns:
            pandas.DataFrame: The dataframe containing the data.
        """
        cfg = self.load_config()
        if not source_file and cfg:
            if cfg.get('source_file'):
                source_file = cfg['source_file']
        if not source_file:
            raise MissingSourceDataError(
                'You need to specify a data source! Pass the `.rds` file path '
                'as a parameter to this method or add it to `cfg.json` under '
                'the "source_file" key.')

        with tempfile.NamedTemporaryFile(suffix='.csv') as tmp:
            robjects.r(f'''library('move', warn.conflicts = FALSE)
                library('lubridate', warn.conflicts = FALSE)
                df <- readRDS("{source_file}")
                write.csv(df, "{tmp.name}", row.names=FALSE)
            ''')
            tmp.seek(0)

            df = pd.read_csv(tmp.name)
            dest = Path(source_file).with_suffix('.csv')

            if save_raw_csv and not save_compressed_csv:
                with open(dest, 'w') as f:
                    f.write(tmp.read().decode())
                logger.info(f'File was saved to {dest}')

            elif save_compressed_csv:
                dest = dest.with_suffix('.csv.zip')
                with zipfile.ZipFile(dest,
                                     mode='w',
                                     compression=zipfile.ZIP_DEFLATED,
                                     compresslevel=9) as zf:
                    zf.write(tmp.name)
                logger.info(f'File was saved to {dest}')
        return df
