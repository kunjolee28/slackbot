from app.utils.get_config import get_config
from app.mocks.mock_config import mock_config

def test_get_config():
    keys = list(mock_config.keys())
    CONFIG = get_config()
    config_keys = CONFIG.keys()
    assert all([key in keys for key in config_keys])