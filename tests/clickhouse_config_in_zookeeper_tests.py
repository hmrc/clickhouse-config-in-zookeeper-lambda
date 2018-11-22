from clickhouse_config_in_zookeeper import lambda_handler, get_zookeeper_client, get_ec2_client, get_clickhouse_cluster_definition
from unittest.mock import patch, MagicMock
import unittest

class GetZookeeperClient(unittest.TestCase):

    @patch('clickhouse_config_in_zookeeper.KazooClient')
    def test_gets_network_interfaces_for_telemetry_zookeeper_and_creates_kazoo_client_with_ips(self, mock_kazoo_constructor):
        mock_kazzoo_client = MagicMock()
        mock_kazoo_constructor.return_value = mock_kazzoo_client
        ec2_client = MagicMock()
        ec2_client.describe_network_interfaces = MagicMock(return_value={
            'NetworkInterfaces': [
                {'PrivateIpAddress': '172.26.35.126'},
                {'PrivateIpAddress': '172.26.101.56'},
                {'PrivateIpAddress': '172.26.38.168'}
            ]
        })

        self.assertEqual(get_zookeeper_client(ec2_client), mock_kazzoo_client)

        ec2_client.describe_network_interfaces.assert_called_with(Filters=[
            {
                "Name": "tag:Component",
                "Values": [
                    "telemetry-zookeeper"
                ]
            },
            {
                "Name": "status",
                "Values": [
                    "in-use"
                ]
            }
        ])
        mock_kazzoo_client.start.assert_called_once()
        mock_kazoo_constructor.assert_called_with(hosts=['172.26.35.126', '172.26.101.56', '172.26.38.168'])



class GetClickhouseClusterDefinition(unittest.TestCase):

    def test_get_all_clickhouse_shards_to_instances(self):
        ec2_client = MagicMock()
        ec2_client.describe_instances = MagicMock(return_value={
            'Reservations': [
                {
                    'Instances': [
                        {
                            'PrivateIpAddress': '172.26.39.30',
                            'Tags': [
                                {
                                    'Value': 'integration',
                                    'Key': 'Env'
                                },
                                {
                                    'Value': '1',
                                    'Key': 'clickhouse-server'
                                },
                                {
                                    'Value': 'clickhouse-server-shard_1_replica_1-asg-2018102612411970390000000d',
                                    'Key': 'aws:autoscaling:groupName'
                                },
                                {
                                    'Value': 'webops_engineer',
                                    'Key': 'iam-groups'
                                },
                                {
                                    'Value': 'clickhouse-server-shard_1_replica_1',
                                    'Key': 'Name'
                                },
                                {
                                    'Value': 'team-webops',
                                    'Key': 'sensu-team-handler'
                                },
                                {
                                    'Value': 'shard_1',
                                    'Key': 'shard_name'
                                },
                                {
                                    'Value': 'false',
                                    'Key': 'tls'
                                },
                                {
                                    'Value': 'arn:aws:iam::638924580364:role/RoleCrossAccountSSH',
                                    'Key': 'auth-account-arn'
                                }
                            ]
                        }
                    ],
                },
                {
                    'Instances': [
                        {
                            'PrivateIpAddress': '172.26.32.16',
                            'Tags': [
                                {
                                    'Value': 'clickhouse-server-shard_2_replica_1-asg-2018102612415581190000000f',
                                    'Key': 'aws:autoscaling:groupName'
                                },
                                {
                                    'Value': 'integration',
                                    'Key': 'Env'
                                },
                                {
                                    'Value': 'webops_engineer',
                                    'Key': 'iam-groups'
                                },
                                {
                                    'Value': 'team-webops',
                                    'Key': 'sensu-team-handler'
                                },
                                {
                                    'Value': 'false',
                                    'Key': 'tls'
                                },
                                {
                                    'Value': 'clickhouse-server-shard_2_replica_1',
                                    'Key': 'Name'
                                },
                                {
                                    'Value': 'arn:aws:iam::638924580364:role/RoleCrossAccountSSH',
                                    'Key': 'auth-account-arn'
                                },
                                {
                                    'Value': 'shard_2',
                                    'Key': 'shard_name'
                                },
                                {
                                    'Value': '1',
                                    'Key': 'clickhouse-server'
                                }
                            ],
                            'AmiLaunchIndex': 0
                        }
                    ],
                },
                {
                    'Instances': [
                        {
                            'PrivateIpAddress': '172.26.99.237',
                            'Tags': [
                                {
                                    'Value': 'team-webops',
                                    'Key': 'sensu-team-handler'
                                },
                                {
                                    'Value': 'arn:aws:iam::638924580364:role/RoleCrossAccountSSH',
                                    'Key': 'auth-account-arn'
                                },
                                {
                                    'Value': 'webops_engineer',
                                    'Key': 'iam-groups'
                                },
                                {
                                    'Value': 'false',
                                    'Key': 'tls'
                                },
                                {
                                    'Value': 'clickhouse-server-shard_1_replica_2-asg-2018102612412156150000000e',
                                    'Key': 'aws:autoscaling:groupName'
                                },
                                {
                                    'Value': 'integration',
                                    'Key': 'Env'
                                },
                                {
                                    'Value': 'clickhouse-server-shard_1_replica_2',
                                    'Key': 'Name'
                                },
                                {
                                    'Value': '1',
                                    'Key': 'clickhouse-server'
                                },
                                {
                                    'Value': 'shard_1',
                                    'Key': 'shard_name'
                                }
                            ],
                            'AmiLaunchIndex': 0
                        }
                    ]
                },
                {
                    'Instances': [
                        {
                            'PrivateIpAddress': '172.26.97.29',
                            'Tags': [
                                {
                                    'Value': 'clickhouse-server-shard_2_replica_2-asg-20181026124228126900000010',
                                    'Key': 'aws:autoscaling:groupName'
                                },
                                {
                                    'Value': 'clickhouse-server-shard_2_replica_2',
                                    'Key': 'Name'
                                },
                                {
                                    'Value': '1',
                                    'Key': 'clickhouse-server'
                                },
                                {
                                    'Value': 'arn:aws:iam::638924580364:role/RoleCrossAccountSSH',
                                    'Key': 'auth-account-arn'
                                },
                                {
                                    'Value': 'webops_engineer',
                                    'Key': 'iam-groups'
                                },
                                {
                                    'Value': 'team-webops',
                                    'Key': 'sensu-team-handler'
                                },
                                {
                                    'Value': 'shard_2',
                                    'Key': 'shard_name'
                                },
                                {
                                    'Value': 'false',
                                    'Key': 'tls'
                                },
                                {
                                    'Value': 'integration',
                                    'Key': 'Env'
                                }
                            ],
                        }
                    ]
                }
            ]
        })

        self.assertEqual(get_clickhouse_cluster_definition(ec2_client),
                         {'shard_1': ['172.26.39.30', '172.26.99.237'],
                          'shard_2': ['172.26.32.16', '172.26.97.29']})

        ec2_client.describe_instances.assert_called_with(Filters=[
            {
                "Name": "tag-key",
                "Values": [
                    "clickhouse-server"
                ]
            },
            {
                "Name": "instance-state-name",
                "Values": [
                    "running"
                ]
            }
        ])

class LambdaHandler(unittest.TestCase):

    @patch('clickhouse_config_in_zookeeper.get_clickhouse_cluster_definition')
    @patch('clickhouse_config_in_zookeeper.get_zookeeper_client')
    @patch('clickhouse_config_in_zookeeper.get_ec2_client')
    def test_should_ensure_zookeeper_path_exists_for_remote_servers(self,
                                                                    mock_get_ec2_client,
                                                                    mock_get_zookeeper_client,
                                                                    mock_get_clickhouse_cluster_definition):
        zookeeper = MagicMock()
        mock_get_zookeeper_client.return_value = zookeeper

        lambda_handler({}, {})

        zookeeper.ensure_path.assert_called_with('clickhouse.config.remote_servers')

    @patch('clickhouse_config_in_zookeeper.get_clickhouse_cluster_definition', return_value='pumpkins')
    @patch('clickhouse_config_in_zookeeper.get_zookeeper_client')
    @patch('clickhouse_config_in_zookeeper.get_ec2_client')
    def test_all_private_ips_and_shards_matching_clickhouse_server_added_to_zookeeper(self,
                                                                                      mock_get_ec2_client,
                                                                                      mock_get_zookeeper_client,
                                                                                      mock_get_clickhouse_cluster_definition):
        ec2_client = MagicMock()
        mock_get_ec2_client.return_value = ec2_client
        shard_config = {'shard_1': ['172.26.39.30', '172.26.99.237'],
                               'shard_2': ['172.26.32.16', '172.26.97.29']}
        mock_get_clickhouse_cluster_definition.return_value = shard_config
        zookeeper = MagicMock()
        mock_get_zookeeper_client.return_value = zookeeper

        lambda_handler({}, {})

        remote_servers_xml = b"""<hmrc_data_cluster>
  <shard>
    <internal_replication>true</internal_replication>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.39.30</host>
      <port>9000</port>
    </replica>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.99.237</host>
      <port>9000</port>
    </replica>
  </shard>
  <shard>
    <internal_replication>true</internal_replication>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.32.16</host>
      <port>9000</port>
    </replica>
    <replica>
      <default_database>graphite</default_database>
      <host>172.26.97.29</host>
      <port>9000</port>
    </replica>
  </shard>
<hmrc_data_cluster>"""

        zookeeper.set.assert_called_with('clickhouse.config.remote_servers', remote_servers_xml)


