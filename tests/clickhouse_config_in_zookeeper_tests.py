from clickhouse_config_in_zookeeper import lambda_handler, get_zookeeper_client, get_ec2_client
from unittest.mock import patch, MagicMock
import unittest

class GetZookeeperClient(unittest.TestCase):

    @patch('clickhouse_config_in_zookeeper.KazooClient')
    def test_gets_network_interfaces_for_telemetry_zookeeper_and_creates_kazoo_client_with_ips(self, mock_kazoo_constructor):
        mock_kazzoo_client = MagicMock()
        mock_kazoo_constructor.return_value = mock_kazzoo_client
        ec2_client = MagicMock()
        sample_response = {
            'NetworkInterfaces': [
                { 'PrivateIpAddress': '172.26.35.126' },
                { 'PrivateIpAddress': '172.26.101.56' },
                { 'PrivateIpAddress': '172.26.38.168' }
            ]
        }
        ec2_client.describe_network_interfaces = MagicMock(return_value=sample_response)

        self.assertEqual(get_zookeeper_client(ec2_client), mock_kazzoo_client)

        ec2_client.describe_network_interfaces.assert_called_with(Filters=[
            {
                'Name': 'tag:Component',
                'Values': [
                    'telemetry-zookeeper'
                ]
            }
        ])
        mock_kazzoo_client.start.assert_called_once()
        mock_kazoo_constructor.assert_called_with(hosts=['172.26.35.126', '172.26.101.56', '172.26.38.168'])



# class GetClickhouseClusterDefinition(unittest.TestCase):
#
#     def test_get_all_clickhouse_shards_to_instances(self):
#         ec2_client = MagicMock()
#         sample_response = {
#             'NetworkInterfaces': [
#                 { 'PrivateIpAddress': '172.26.35.126' },
#                 { 'PrivateIpAddress': '172.26.101.56' },
#                 { 'PrivateIpAddress': '172.26.38.168' }
#             ]
#         }
#         ec2_client.describe_instances = MagicMock(return_value=sample_response)
#
#         ec2_client.describe_instances.assert_called_with(Filters=[
#             {
#                 'Name': 'tag-key',
#                 'Values': [
#                     'clickhouse-server'
#                 ]
#             }
#         ])

class LambdaHandler(unittest.TestCase):

    @patch('clickhouse_config_in_zookeeper.boto3')
    def test_get_all_clickhouse_instances(self, mock_boto3):
        mock_client=MagicMock()
        mock_boto3.client = MagicMock(return_value=mock_client)

        lambda_handler({}, {})

        mock_client.describe_instances.assert_called_with(Filters=[
            {
                'Name': 'tag-key',
                'Values': [
                    'clickhouse-server'
                ]
            }
        ])

    @patch('clickhouse_config_in_zookeeper.boto3')
    def test_all_private_ips_and_shards_matching_clickhouse_server_added_to_zookeeper(self, mock_boto3):
        mock_client=MagicMock()
        mock_boto3.client = MagicMock(return_value=mock_client)

        sampleResponse = {}
        mock_client.describe_instances = MagicMock(return_value=sampleResponse)

