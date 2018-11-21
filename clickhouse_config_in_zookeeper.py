import logging
import boto3
from kazoo.client import KazooClient

logger = logging.getLogger('sensu_pagerduty_heartbeat')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Get zookeeper IPs from ec2
    # Get clickhouse-server IPs and shards from ec2
    # Write remote server config to Zookeeper
    # Write graphite-rollup config to Zookeeper

    ec2 = get_ec2_client()
    response = ec2.describe_instances(Filters=[
        {
            "Name": "tag-key",
            "Values": [
                "clickhouse-server"
            ]
        }
    ])

    return 'Hello World'

def get_clickhouse_cluster_definition(ec2_client):
    return ""


def get_zookeeper_client(ec2_client):
    response = ec2_client.describe_network_interfaces(Filters=[
        {
            "Name": "tag:Component",
            "Values": [
                "telemetry-zookeeper"
            ]
        }
    ])
    ips = [ i['PrivateIpAddress'] for i in response['NetworkInterfaces']]
    zk = KazooClient(hosts=ips)
    zk.start()
    return zk

def get_ec2_client():
    return boto3.client('ec2')
