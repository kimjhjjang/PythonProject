# -*- coding: utf-8 -*-
import yaml

from src.util import DictHelper


def read_config_yaml():

    try:
        with open("./config/config.yaml", 'r') as stream:
            return DictHelper(yaml.safe_load(stream))
    except FileNotFoundError as e:
        print(e)
        exit()
