"""The daemon listening to Twitter."""

class ConfigError(Exception):
    pass

def getConfig(mongo_client):
    result = mongo_client.tagalizer.config.find()
    if result == None:
        raise ConfigError
