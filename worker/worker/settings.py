import os
import sys


TEST_MODE = 'pytest' in sys.modules
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv(
    'TEST_REDIS_DB' if TEST_MODE else 'REDIS_DB',
    1 if TEST_MODE else 0
))
TASK_QUEUE = 'TASK_QUEUE'
