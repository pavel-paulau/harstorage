import logging

import pylons.test

from harstorage.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """harstorage setup"""

    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)