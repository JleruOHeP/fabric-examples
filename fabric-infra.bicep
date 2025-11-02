// =====================================================
// Bicep template: fabric-infra.bicep
// Purpose: Create RG, Managed Identity, and Fabric Capacity
// Author: Mikhail Koptelov
// =====================================================

// ===============
// PARAMETERS
// ===============
@description('Azure region for all resources')
param location string = 'australiaeast'

@description('Name of the Fabric capacity')
param fabricCapacityName string = 'fabric-capacity-demo'

@description('Fabric SKU: F2, F4, F8, F16, etc.')
param fabricSkuName string = 'F2'

@description('Fabric admin user principal (email or objectId)')
param adminUser string

@description('Name of the managed identity to create')
param miName string = 'fabric-demo-identity'

// ===============
// MANAGED IDENTITY
// ===============
resource fabricIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: miName
  location: location
}

// ===============
// FABRIC CAPACITY
// ===============
// Resource type: Microsoft.Fabric/capacities
resource fabricCapacity 'Microsoft.Fabric/capacities@2023-11-01' = {
  name: fabricCapacityName
  location: location
  sku: {
    name: fabricSkuName
    tier: 'Fabric'
  }
  properties: {
    administration: {
      members: [
        adminUser
      ]
    }
  }
}

// ===============
// OUTPUTS
// ===============
output capacityId string = fabricCapacity.id
output managedIdentityId string = fabricIdentity.id
output managedIdentityClientId string = fabricIdentity.properties.clientId
