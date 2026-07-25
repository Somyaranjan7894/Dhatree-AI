# Database Architecture

The PostgreSQL database relies on the following key entities:

- **Users**: Core authentication model.
- **Farms**: Geographically bounded areas representing user properties.
- **Crops**: Specific crops planted within a farm.
- **Soil Samples**: Historical N, P, K, and pH readings linked to farms.
- **Weather Snapshots**: Captured weather intelligence linked to recommendations.
- **Notifications**: System-generated alerts.

Refer to the Django models in \ackend/modules/*\ for exact field specifications.

