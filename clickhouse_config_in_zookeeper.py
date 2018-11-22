import logging
import boto3
from kazoo.client import KazooClient
import lxml.etree as et

logger = logging.getLogger('sensu_pagerduty_heartbeat')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Get zookeeper IPs from ec2
    # Get clickhouse-server IPs and shards from ec2
    # Write remote server config to Zookeeper
    # Write graphite-rollup config to Zookeeper

    ec2 = get_ec2_client()
    zookeeper = get_zookeeper_client(ec2)
    remote_server_path = 'clickhouse.config.remote_servers'
    zookeeper.ensure_path(remote_server_path)

    xml = et.Element('hmrc_data_cluster')
    cluster_definition = get_clickhouse_cluster_definition(ec2)
    for key, replicas in cluster_definition.items():
        shard_element = et.SubElement(xml, 'shard')
        internal_replication_element = et.SubElement(shard_element, 'internal_replication')
        internal_replication_element.text = 'true'
        for replica in replicas:
            host_element = et.SubElement(shard_element, 'host')
            host_element.text = replica


    xmlstr = et.tostring(xml, encoding='utf8', method='xml', pretty_print=True)

    zookeeper.set(remote_server_path, xmlstr)

    return 'Hello World'

def get_clickhouse_cluster_definition(ec2_client):
    response = ec2_client.describe_instances(Filters=[
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

    shards_to_instances = {}

    for r in response['Reservations']:
        for i in r['Instances']:
            shard_tag = next(tag for tag in i['Tags'] if tag['Key'] == 'shard_name')
            shard_name = shard_tag['Value']
            ips = shards_to_instances.get(shard_name, list())
            ips.append(i['PrivateIpAddress'])
            shards_to_instances[shard_name] = ips
    return shards_to_instances


def get_zookeeper_client(ec2_client):
    response = ec2_client.describe_network_interfaces(Filters=[
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
    ips = [ i['PrivateIpAddress'] for i in response['NetworkInterfaces']]
    zk = KazooClient(hosts=ips)
    zk.start()
    return zk

def get_ec2_client():
    return boto3.client('ec2')
