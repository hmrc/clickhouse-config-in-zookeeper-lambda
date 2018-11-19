from clickhouse_config_in_zookeeper import lambda_handler
import unittest

class TestSensuPagerdutyHeartbeat(unittest.TestCase):
    def test_hello_world_returned(self):
        self.assertEquals(lambda_handler({}, {}), 'Hello World')
