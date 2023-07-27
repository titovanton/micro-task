from loguru import logger

from . import settings


if settings.TEST_MODE:
    logger.add(
        'logs/pytest.log',
        level='DEBUG',
        colorize=True,
        rotation='100 KB',
    )
else:
    logger.add(
        'logs/application.log',
        level='DEBUG',
        colorize=True,
        rotation='100 KB',
    )

log = logger
