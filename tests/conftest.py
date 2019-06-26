import json
import os
from tempfile import NamedTemporaryFile, mkstemp

from click.testing import CliRunner

import delegator

from pytest import fixture

STORYSCRIPT_CONFIG = {
    'id': os.environ['STORYSCRIPT_INT_CONF_USER_ID'],
    'access_token': os.environ['STORYSCRIPT_INT_CONF_ACCESS_TOKEN']
}


@fixture()
def cli():
    def function(*args, logged_in=True):

        tf = NamedTemporaryFile().name

        if logged_in:
            # Create a temporary config file.
            with open(tf, 'w') as f:
                f.write(json.dumps(STORYSCRIPT_CONFIG))

        # Make temporary file.
        args = ' '.join(args)
        c = delegator.run(f'story {args}', env={'STORY_CONFIG_PATH': tf})

        os.remove(tf)
        return c

    return function


@fixture()
def runner(logged_in=True):
    _, config_path = mkstemp()

    if logged_in:
        with open(config_path, 'w') as f:
            json.dump(STORYSCRIPT_CONFIG, f)

    return CliRunner(env={'STORY_CONFIG_PATH': config_path})


@fixture
def patch_init(mocker):
    """
    Makes patching a class' constructor slightly easier
    """
    def patch_init(item):
        mocker.patch.object(item, '__init__', return_value=None)
    return patch_init


@fixture
def patch_many(mocker):
    """
    Makes patching many attributes of the same object simpler
    """
    def patch_many(item, attributes):
        for attribute in attributes:
            mocker.patch.object(item, attribute)
    return patch_many


@fixture
def patch(mocker, patch_init, patch_many):
    mocker.patch.init = patch_init
    mocker.patch.many = patch_many
    return mocker.patch
