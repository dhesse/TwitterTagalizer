"""The daemon listening to Twitter."""
import argparse

class ConfigError(Exception):
    pass

def getConfig(mongo_client):
    result = mongo_client.tagalizer.config.find()
    if result == None:
        raise ConfigError
    options = {}
    for option in result:
        if option['option_name'] in options:
            raise ConfigError
        options[option['option_name']] = option['value']
    return options

def storeConfig(mongo_client, config):
    for option in config:
        mongo_client.tagalizer.config.insert_one(
            {'option_name': option,
             'value': config[option]})
