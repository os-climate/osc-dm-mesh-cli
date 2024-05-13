# CLI Script - End-to-End Flow

This script demonstrates how to:
- register a user
- view users
- register a product
- view a product
- discover product information (artifacts)
- create a subscriber and their cart
- view a cart
- add and remove items from a cart
- create an order (from a cart)
- view an order and order history

## Working with Users

User can be registered.  Once registered, you can view
all users or a specific user.

User must be registered in a role, either "guest", "subscriber",
"publisher", or "administrator".

### Register a User

Let's register a guest:
~~~~
ROLE="guest" ;
EMAIL="guest.user@brodagroupsoftware.com" ;
NAME="Guest User" ;
PHONE="+1 647.555.1212" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --register \
    --role "$ROLE" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "44740067-4131-44e7-b347-2e2d13b1d6c5"}
~~~~

### View Users

View all users:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve

[{"uuid": "44740067-4131-44e7-b347-2e2d13b1d6c5", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}, {"uuid": "d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 14:53:27.378", "updatetimestamp": "2024-03-17 14:53:27.378", "role": "guest"}]
~~~~

### View a User by UUID

View all users:
~~~~
UUID="44740067-4131-44e7-b347-2e2d13b1d6c5" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --uuid "$UUID"

{"uuid": "44740067-4131-44e7-b347-2e2d13b1d6c5", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}
~~~~

### View a User by Email

View all user roles by email (note that user can have multiple roles):
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --email "$EMAIL"

[{"uuid": "44740067-4131-44e7-b347-2e2d13b1d6c5", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}, {"uuid": "d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 14:53:27.378", "updatetimestamp": "2024-03-17 14:53:27.378", "role": "guest"}]
~~~~

### View a User by Role/Email

NOTE: Not sure this works properly... should only return SINGLE item, not LIST

View specific role/email:
~~~~
ROLE="guest" ;
EMAIL="guest.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --role "$ROLE" \
    --email "$EMAIL"

[{"uuid": "44740067-4131-44e7-b347-2e2d13b1d6c5", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}, {"uuid": "d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 14:53:27.378", "updatetimestamp": "2024-03-17 14:53:27.378", "role": "guest"}]
~~~~

## Working with Products

Products can be registered.  Once registered they can
be viewed, all their artifacts can be viewed, or an
individual artifact can be viewed

### Registering a Product

~~~~
DATAPRODUCT_DIR="$SAMPLES_DIR/dataproducts/rmi";
ADDRESS="http://osc-dm-product-srv-0:8000" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --register \
    --directory "$DATAPRODUCT_DIR" \
    --address "$ADDRESS"

{"uuids": "/Users/ericbroda/Development/scratch/bgsdat-samples/dataproducts/rmi/uuids.yaml", "confirmation": {"product_uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "artifact_uuids": [{"Housing Units Income": "cd9ac396-eff1-4c0c-afc7-001a98d36708"}, {"Emissions Targets": "448555bd-1689-4841-b927-df8d8a33b196"}, {"Revenue by Tech": "970b1bef-be20-4c6e-8b31-5cbc6cd9900e"}, {"State Targets": "cebd39d7-0fb2-46f8-8a99-e16ecb59b06e"}, {"Employees": "5584f4b6-5ecd-42d9-b1f2-3ed8721996a2"}, {"Net Plant Balance": "19b09852-1e26-4a4b-b432-4a8cf052349c"}, {"Customer Sales": "06309f42-8c2a-4c76-adf2-72e4ca8821ec"}, {"State Utility Polcies": "d6d7fc00-52fc-4429-b35a-57ec3a8941a9"}, {"Uneconomic Dispatch": "73b6bdfb-19b3-4fa3-8870-48269cb72794"}, {"Debit Equity Returns": "1ea085ac-b327-4692-840b-57684bbc21bb"}, {"Utility Information": "36067d4b-75e8-4f8a-a470-b033abb3df7a"}, {"Assets Earnings Investments": "d88a5a79-d8c5-494d-9001-6bfac33b9883"}, {"Utility State Map": "4c76eaee-2598-498b-ac41-8b8972a50167"}, {"Operations Emissions by Fuel": "fad9b546-6801-4519-b0b9-406b8b716eef"}, {"Expenditure Bills Burden": "56f490ac-88a8-41c6-a8c9-c2d8b8ee349e"}, {"Expenditure Bills Burden Detail": "64172178-35d1-49b9-815e-a003f0f9959e"}, {"Operations Emissions by Tech": "a5a59ec5-85f8-49a4-ae59-eabae05e3a53"}]}}
~~~~

### Viewing all Products

~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve

[{"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}]
~~~~

### Viewing a Product by UUID

~~~~
UUID="c4c68ca9-a053-4878-acbf-7ee424ab11e6"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --uuid "$UUID"

{"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}
~~~~

### Viewing a Product by Namespace/Name

~~~~
NAMESPACE="brodagroupsoftware.com" ;
NAME="rmi.dataproduct" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --namespace "$NAMESPACE" \
    --name "$NAME"

{"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}
~~~~

### Viewing all Product in a Namespace

~~~~
NAMESPACE="brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --namespace "$NAMESPACE"

[{"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}]
~~~~

### Discovering Product (directly to Product)

NOTE: The data product must be registered and then running for this
capability to work properly.

Discover is like view/retrieve, except discover gets
more details directly from the product:
~~~~
UUID="c4c68ca9-a053-4878-acbf-7ee424ab11e6"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --discover \
    --uuid "$UUID"

{"product": {"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": null, "createtimestamp": null, "updatetimestamp": null}, "artifacts": [{"uuid": "cd9ac396-eff1-4c0c-afc7-001a98d36708", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Assets Earnings Investments", "description": "Detailed breakdown of utility assets in electric rate base, earnings on these assets, and annual investments (capital additions) by technology.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/assets_earnings_investments.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "42e6977b-b182-46df-88d0-d01eae905bdf", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Customer Sales", "description": "Number of customers, MWh electricity sales, and revenues by customer type.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/customers_sales.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "f17c47fe-2e32-4bc4-84ae-5dfa62bf9767", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Debit Equity Returns", "description": "Rate base, equity, debt, returns, earnings, interest expense, tax expense, and the rates of return used for earnings and revenue calculations.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/debt_equity_returns.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "7eb6174c-e96e-4603-b9c9-f23a3093e06c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Emissions Targets", "description": "CO2 emissions and projections, as well as electricity generation and projections and comparison to RMI 1.5\u00b0C decarbonization pathway for the US electricity sector.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/emissions_targets.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "fb823df5-d127-477e-a6dd-696882f32d76", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Employees", "description": "Number of employees that work at large power plants, by technology, for each utility", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/employees.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "a341ab3a-6bb1-4c53-a3b4-e51080e67805", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "23f2de85-5551-4727-bba3-072280634e56", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden Detail", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group. Broken down into additional components and details compared to expenditure_bills_burden, leading a large file size (575 MB) that cannot be opened in Excel.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden_detail.csv.zip"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "9d03119d-0a54-4749-b089-d873ccdc2d36", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "7c30cadc-4c3a-4ec6-bf5a-78ab1e3d3d68", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Net Plant Balance", "description": "Original cost, accumulated depreciation, and remaining net plant balance of electric plants in service, by FERC classification.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/net_plant_balance.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "80c11d83-21bc-4470-8e3c-2ca1437f31b2", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Fuel", "description": "Generation, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Within each generator and for purchased power, data values are differentiated by fuel type.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_fuel.zip"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "9eb7d257-ca51-4b5f-80b6-b246c8882a2b", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Tech", "description": "Capacity, generation, capacity factor, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Each generator is identified by a single technology.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_tech.zip"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "b156243e-1b19-4657-b208-76d024fe23aa", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Revenue by Tech", "description": "Revenues for each utility, by technology and component, for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/revenue_by_tech.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "ce2d8d34-0b21-4c23-9d25-c7adc8fa6a0b", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Targets", "description": "Greenhouse gas (GHG) and renewable portfolio standard (RPS) data by state, including baseline, interim, and final target years", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_targets.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "725e42e4-4a77-44d8-83cc-cfef97cfe9df", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Utility Polcies", "description": "Policy data shown on the \"Policy & Regulations\" dashboard of the Utility Transition Hub Portal, by state and utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_utility_policies.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "9fb63189-3fda-48f6-994c-f58f31f90cc4", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Uneconomic Dispatch", "description": "Capacity and monthly cash flows used for monthly net revenues and gross losses for all operating coal plants above 5 MWs in the nation", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "url": "https://utilitytransitionhub.rmi.org/static/data_download/uneconomic_dispatch_monthly_cash_flow.xlsx"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "56bc4a83-4c8e-46cc-bd89-83bd6c42b029", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility Information", "description": "Utility identifiers such as name, ID numbers from various sources, and utility type. Includes connections from operating companies to parent companies.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_information.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "8e5536a0-7705-4585-bf7f-4006becbbd79", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility State Map", "description": "A list of states that each utility operates in, including capacity owned in state, capacity operated in state, and energy sales in state.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_state_map.csv"}, "createtimestamp": null, "updatetimestamp": null}]}
~~~~

### Discovering all Artifacts for a Product (directly to Product)

~~~~
PRODUCT_UUID="c4c68ca9-a053-4878-acbf-7ee424ab11e6"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --discover \
    --productuuid "$PRODUCT_UUID"

[{"uuid": "737b4e25-558e-437e-9c60-695571ac0433", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Assets Earnings Investments", "description": "Detailed breakdown of utility assets in electric rate base, earnings on these assets, and annual investments (capital additions) by technology.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/assets_earnings_investments.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "cd9ac396-eff1-4c0c-afc7-001a98d36708", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Customer Sales", "description": "Number of customers, MWh electricity sales, and revenues by customer type.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/customers_sales.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "a04242d9-0336-4df9-9efd-b70c0be63368", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Debit Equity Returns", "description": "Rate base, equity, debt, returns, earnings, interest expense, tax expense, and the rates of return used for earnings and revenue calculations.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/debt_equity_returns.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "3ae124dc-b3d6-4e15-9929-5ef1fcd3c2b6", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Emissions Targets", "description": "CO2 emissions and projections, as well as electricity generation and projections and comparison to RMI 1.5\u00b0C decarbonization pathway for the US electricity sector.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/emissions_targets.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "326a67f7-4861-4a42-a775-a4b788f9b465", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Employees", "description": "Number of employees that work at large power plants, by technology, for each utility", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/employees.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "23a06c19-53f6-4ad3-92bc-605938497149", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "cb6d17d7-cfd9-4145-ac51-beb5b28a24fd", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden Detail", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group. Broken down into additional components and details compared to expenditure_bills_burden, leading a large file size (575 MB) that cannot be opened in Excel.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden_detail.csv.zip"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "31bf723a-a8dd-4ae3-825c-2cae8bd945d8", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "23e6cee4-bcbc-42ee-9a36-6f3bb304004e", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Net Plant Balance", "description": "Original cost, accumulated depreciation, and remaining net plant balance of electric plants in service, by FERC classification.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/net_plant_balance.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "e0c29b72-6dde-4fe8-83bc-4b2638f40d6c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Fuel", "description": "Generation, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Within each generator and for purchased power, data values are differentiated by fuel type.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_fuel.zip"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "65afae80-ec78-4aed-b90b-11e8e904180d", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Tech", "description": "Capacity, generation, capacity factor, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Each generator is identified by a single technology.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_tech.zip"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "0a8bf36e-3269-4a9a-ae0d-66e31756a7c2", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Revenue by Tech", "description": "Revenues for each utility, by technology and component, for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/revenue_by_tech.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "895cde68-395b-4d2c-a4c9-c13b7f6fd78e", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Targets", "description": "Greenhouse gas (GHG) and renewable portfolio standard (RPS) data by state, including baseline, interim, and final target years", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_targets.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "f5ede988-86ed-4bd2-a070-5bf3a918cd66", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Utility Polcies", "description": "Policy data shown on the \"Policy & Regulations\" dashboard of the Utility Transition Hub Portal, by state and utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_utility_policies.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "0a05314c-e09f-428b-83b7-641053994387", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Uneconomic Dispatch", "description": "Capacity and monthly cash flows used for monthly net revenues and gross losses for all operating coal plants above 5 MWs in the nation", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "url": "https://utilitytransitionhub.rmi.org/static/data_download/uneconomic_dispatch_monthly_cash_flow.xlsx"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "496093f1-25f9-41d4-b4bb-2c3f191e5e61", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility Information", "description": "Utility identifiers such as name, ID numbers from various sources, and utility type. Includes connections from operating companies to parent companies.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_information.csv"}, "createtimestamp": null, "updatetimestamp": null}, {"uuid": "cd791e0a-874d-40c9-8fc8-113bf46baed8", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility State Map", "description": "A list of states that each utility operates in, including capacity owned in state, capacity operated in state, and energy sales in state.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_state_map.csv"}, "createtimestamp": null, "updatetimestamp": null}]
~~~~

### Discovering a Specific Artifact for a Product (directly to Product)

~~~~
PRODUCT_UUID="c4c68ca9-a053-4878-acbf-7ee424ab11e6"
ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --discover \
    --productuuid "$PRODUCT_UUID" \
    --uuid "$ARTIFACT_UUID"

{"uuid": "cd9ac396-eff1-4c0c-afc7-001a98d36708", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}
~~~~

## Working with Carts and Orders

Note that only subscribers (ie. users that have
been registered in role "subscriber") can have a cart.

### Registering a Subscriber

Let's register a subscriber (note: this will also create a
cart that we will use in the next steps):
~~~~
ROLE="subscriber" ;
EMAIL="subscriber.user@brodagroupsoftware.com" ;
NAME="Subscriber User" ;
PHONE="+1 647.555.1212" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --register \
    --role "$ROLE" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "2bb4574f-a1a7-4967-b953-980591a7d004"}
~~~~

### Viewing all Carts

Let's view the carts available (there should only be one if you are following
these steps).  The cart UUID will be used in subsequent steps):
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve

[{"uuid": "24be71ef-3cd1-4a15-9599-f82cb64fb4d8", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-19 20:40:45.856", "updatetimestamp": "2024-03-19 20:40:45.856"}]
~~~~

### Viewing a Cart by UUID

~~~~
CART_UUID="24be71ef-3cd1-4a15-9599-f82cb64fb4d8" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve \
    --uuid "$CART_UUID"

{"uuid": "24be71ef-3cd1-4a15-9599-f82cb64fb4d8", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-18 20:44:37.301", "updatetimestamp": "2024-03-18 20:44:37.301"}
~~~~

### Viewing a Cart by User (email)

~~~~
EMAIL="subscriber.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve \
    --email "$EMAIL"

{"uuid": "24be71ef-3cd1-4a15-9599-f82cb64fb4d8", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-18 20:44:37.301", "updatetimestamp": "2024-03-18 20:44:37.301"}
~~~~

### Adding an Item to a Cart

Add an item (defined by a product uuid and artifact uuid)
to a cart:
~~~~
PRODUCT_UUID="c4c68ca9-a053-4878-acbf-7ee424ab11e6" ;
ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708" ;
CART_UUID="24be71ef-3cd1-4a15-9599-f82cb64fb4d8" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --add \
    --uuid "$CART_UUID" \
    --productuuid "$PRODUCT_UUID" \
    --artifactuuid "$ARTIFACT_UUID"

{"uuid": "24be71ef-3cd1-4a15-9599-f82cb64fb4d8", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product_uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "artifact_uuid": "cd9ac396-eff1-4c0c-afc7-001a98d36708"}], "createtimestamp": "2024-03-21 12:26:04.269", "updatetimestamp": "2024-03-21 12:26:04.269"}
~~~~

### Removing an Item from a Cart

Remove an item (defined by a product uuid and artifact uuid)
that exists in a cart:
~~~~
PRODUCT_UUID="c4c68ca9-a053-4878-acbf-7ee424ab11e6" ;
ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708" ;
CART_UUID="24be71ef-3cd1-4a15-9599-f82cb64fb4d8" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --remove \
    --uuid "$CART_UUID" \
    --productuuid "$PRODUCT_UUID" \
    --artifactuuid "$ARTIFACT_UUID"

{"uuid": "24be71ef-3cd1-4a15-9599-f82cb64fb4d8", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-19 20:55:28.662", "updatetimestamp": "2024-03-19 20:55:28.662"}
~~~~

### Create an order (ie. Purchase a Cart)

To create an order and purchase a cart:
~~~~
CART_UUID="24be71ef-3cd1-4a15-9599-f82cb64fb4d8" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --purchase \
    --cartuuid "$CART_UUID"

{"uuid": "d4ff42fd-4f7b-4ab5-840a-30d7c8ff8a23"}
~~~~

### View an Order

To view an existing order:
~~~~
ORDER_UUID="d4ff42fd-4f7b-4ab5-840a-30d7c8ff8a23" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --retrieve \
    --uuid "$ORDER_UUID"

{"uuid": "d4ff42fd-4f7b-4ab5-840a-30d7c8ff8a23", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "ab55bcdd-6a7e-4c7c-940b-9d1c198ffede", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-23 14:42:51.026", "updatetimestamp": "2024-03-23 14:42:51.026"}, "artifact": {"uuid": "cd9ac396-eff1-4c0c-afc7-001a98d36708", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}}], "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}, "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}
~~~~

### View a User's Order History

To view a user's order history:
~~~~
EMAIL="subscriber.user@brodadgroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --retrieve \
    --email "$EMAIL"

[{"uuid": "d4ff42fd-4f7b-4ab5-840a-30d7c8ff8a23", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "ab55bcdd-6a7e-4c7c-940b-9d1c198ffede", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "c4c68ca9-a053-4878-acbf-7ee424ab11e6", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-23 14:42:51.026", "updatetimestamp": "2024-03-23 14:42:51.026"}, "artifact": {"uuid": "cd9ac396-eff1-4c0c-afc7-001a98d36708", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}}], "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}, "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}]
~~~~

## Utility

Dump the registrar information:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT utility \
    --dump

[{"key": "/products/324acdc7-96f7-477b-bd09-343335b7e423", "value": {"uuid": "324acdc7-96f7-477b-bd09-343335b7e423", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-03-17 14:53:52.103", "updatetimestamp": "2024-03-17 14:53:52.103"}}, {"key": "/users/guest/d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "value": {"uuid": "d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 14:53:27.378", "updatetimestamp": "2024-03-17 14:53:27.378", "role": "guest"}}]
~~~~



