## Purpose: Creates instances of various Azure management clients using mock values and prints whether expected client properties exist.

### Packages used:
- azure-mgmt-authorization 
- azure-mgmt-batch 
- azure-mgmt-cdn 
- azure-mgmt-containerregistry 
- azure-mgmt-containerservice 
- azure-mgmt-cosmosdb 
- azure-mgmt-devtestlabs 
- azure-mgmt-dns 
- azure-mgmt-hdinsight 
- azure-mgmt-iothub 
- azure-mgmt-keyvault 
- azure-mgmt-loganalytics 
- azure-mgmt-marketplaceordering 
- azure-mgmt-monitor 
- azure-mgmt-network 
- azure-mgmt-rdbms 
- azure-mgmt-redis 
- azure-mgmt-resource 
- azure-mgmt-servicebus 
- azure-mgmt-sql 
- azure-mgmt-storage 
- azure-mgmt-trafficmanager 
- azure-mgmt-web

### Functionality:
- Creates mock credentials and subscription ID values.
- Initializes a wide range of Azure management clients.
- Verifies existence of common properties (e.g., profiles, servers, metrics) on each client.
- Prints validation results to the console.

### How to run the example :
```
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses