import logging
import boto3
from kazoo.client import KazooClient
import lxml.etree as et

log = logging.getLogger('clickhouse_config_in_zookeeper')
log.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    # Get zookeeper IPs from ec2
    # Get clickhouse-server IPs and shards from ec2
    # Write remote server config to Zookeeper

    ec2 = get_ec2_client()
    log.debug('get_ec2_client successful')

    zookeeper = get_zookeeper_client(ec2)

    remote_server_path = ensure_path_exists(zookeeper)

    remote_server_xml, cluster_definition = generate_remote_servers_xml(ec2)

    zookeeper.set(remote_server_path, remote_server_xml)
    log.info(
        'remote_servers added to Zookeeper successfully for cluster definition'
    )

    zookeeper.stop()
    log.debug('Disconnected from zookeeper.')
    return {
        'cluster_definition': cluster_definition
    }


def ensure_path_exists(zookeeper):
    remote_server_path = 'clickhouse.config.remote_servers'
    zookeeper.ensure_path(remote_server_path)
    log.debug("{0} exists: {1}".format(remote_server_path,
                                       zookeeper.exists(remote_server_path)))
    return remote_server_path


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
            shard_tag = next(tag for tag in i['Tags']
                             if tag['Key'] == 'shard_name')
            shard_name = shard_tag['Value']
            ips = shards_to_instances.get(shard_name, list())
            ips.append(i['PrivateIpAddress'])
            shards_to_instances[shard_name] = ips
    return shards_to_instances


def get_zookeeper_client(ec2_client):
    response = ec2_client.describe_network_interfaces(
        Filters=[
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
        ]
    )
    ips = [i['PrivateIpAddress'] for i in response['NetworkInterfaces']]
    log.debug("Found Zookeeper clients {0}".format(ips))
    zk = KazooClient(hosts=ips)
    log.debug('Created Zookeeper kazoo client')
    zk.start()
    log.debug('Connection to zookeeper established.')
    return zk


def generate_remote_servers_xml(ec2):
    remote_servers = et.Element('hmrc_data_cluster')
    cluster_definition = get_clickhouse_cluster_definition(ec2)
    for _, replicas in cluster_definition.items():
        shard_tag = et.SubElement(remote_servers, 'shard')
        internal_replication_tag = et.SubElement(shard_tag,
                                                 'internal_replication')
        internal_replication_tag.text = 'true'
        for replica in replicas:
            replica_tag = et.SubElement(shard_tag, 'replica')
            default_database_tag = et.SubElement(replica_tag,
                                                 'default_database')
            default_database_tag.text = 'graphite'
            host_tag = et.SubElement(replica_tag, 'host')
            host_tag.text = replica
            port_tag = et.SubElement(replica_tag, 'port')
            port_tag.text = '9000'

    remote_server_xml = et.tostring(remote_servers, encoding='utf8',
                                    method='xml', pretty_print=True).rstrip()
    log.info("Generated remote_servers xml for cluster {0}"
             .format(cluster_definition))
    return remote_server_xml, cluster_definition

def get_ec2_client():
    return boto3.client('ec2', 'eu-west-2')
