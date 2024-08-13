import yaml
import logging

with open('properties.yml') as f:
    PROPERTIES = yaml.load(f, Loader=yaml.FullLoader)

# -- logger setting
LOGGER = logging.getLogger("fresh-trash-recsys")
LOGGER.setLevel(logging.DEBUG)

# -- formatter setting
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
