import logging

logger = logging.getLogger('sensu_pagerduty_heartbeat')
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    return 'Hello World'
