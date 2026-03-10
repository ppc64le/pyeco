# sub-test1.py

import unittest
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.batch import BatchManagementClient
from azure.mgmt.cdn import CdnManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.devtestlabs import DevTestLabsClient
from azure.mgmt.dns import DnsManagementClient
from azure.mgmt.hdinsight import HDInsightManagementClient
from azure.mgmt.iothub import IotHubClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.marketplaceordering import MarketplaceOrderingAgreements
from azure.mgmt.marketplaceordering import MarketplaceOrderingAgreements  # SDK uses this pattern
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.trafficmanager import TrafficManagerManagementClient
from azure.mgmt.web import WebSiteManagementClient

class TestAzureClientProperties(unittest.TestCase):

    def setUp(self):
        """Setup fake credentials and subscription id for all clients"""
        self.fake_cred = "fake-cred"
        self.fake_sub_id = "fake-sub"

    def test_authorization_client(self):
        client = AuthorizationManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "role_definitions"))

    def test_batch_client(self):
        client = BatchManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "batch_account"))

    def test_cdn_client(self):
        client = CdnManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "profiles"))

    def test_containerregistry_client(self):
        client = ContainerRegistryManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "registries"))

    def test_containerservice_client(self):
        client = ContainerServiceClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "managed_clusters"))

    def test_cosmosdb_client(self):
        client = CosmosDBManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "database_accounts"))

    def test_devtestlabs_client(self):
        client = DevTestLabsClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "labs"))

    def test_dns_client(self):
        client = DnsManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "zones"))

    def test_hdinsight_client(self):
        client = HDInsightManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "clusters"))

    def test_iothub_client(self):
        client = IotHubClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "iot_hub_resource"))

    def test_keyvault_client(self):
        client = KeyVaultManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "vaults"))

    def test_loganalytics_client(self):
        client = LogAnalyticsManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "workspaces"))

    def test_marketplaceordering_client(self):
        client = MarketplaceOrderingAgreements(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "marketplace_agreements"))
        self.assertTrue(callable(getattr(client.marketplace_agreements, "list", None)))

    def test_monitor_client(self):
        client = MonitorManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "metrics"))

    def test_network_client(self):
        client = NetworkManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "virtual_networks"))

    def test_mysql_client(self):
        client = MySQLManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "servers"))

    def test_redis_client(self):
        client = RedisManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "redis"))

    def test_resource_client(self):
        client = ResourceManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "resource_groups"))

    def test_servicebus_client(self):
        client = ServiceBusManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "namespaces"))

    def test_sql_client(self):
        client = SqlManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "servers"))

    def test_storage_client(self):
        client = StorageManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "storage_accounts"))

    def test_trafficmanager_client(self):
        client = TrafficManagerManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "profiles"))

    def test_web_client(self):
        client = WebSiteManagementClient(self.fake_cred, self.fake_sub_id)
        self.assertTrue(hasattr(client, "web_apps"))

if __name__ == "__main__":
    unittest.main()
