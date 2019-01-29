from .devenv import DevConfig
from .testenv import TestingConfig
from .prodenv import ProdConfig


config = {
    "dev":DevConfig,
    "test":TestingConfig,
    "prod":ProdConfig,
    "default":DevConfig
}