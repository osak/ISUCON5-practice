import os
import os.path
import logging

logging.basicConfig(level=logging.INFO)


def load_json(path):
    import json
    with open(path) as f:
        return json.load(f)


def load_yaml(path):
    import yaml
    with open(path) as f:
        return yaml.load(f.read())


def load_config(app_name):
    logger = logging.getLogger('configloader')
    config_root = os.path.join(os.path.dirname(__file__), '..', 'config')
    env = os.getenv('ISUCON_TOOLS_ENV', 'dev')
    for spec in [{'ext': 'json', 'loader': load_json}, {'ext': 'yml', 'loader': load_yaml}]:
        path = os.path.abspath(os.path.join(config_root, '{app_name}-{env}.{ext}'.format(app_name=app_name, env=env, ext=spec['ext'])))
        if os.path.exists(path):
            logger.info('Loading configuration from ' + path)
            return spec['loader'](path)
    return None
