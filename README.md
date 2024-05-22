# osc-dm-mesh-cli - Ecosystem Platform Command Line Interface

This is a command line interface (CLI) for
Broda Group Software's Ecosystem Platform.

The CLI interacts with any component in the Ecosystem Platform and
allows the user to execute the following:
- Register, view, and manage users (guests, subscribers,
and publishers)
- Generate UUIDs for products, and then register, view, and manage
those registered products
- Discover data products, and view their artifacts, metadata, and
sample data
- View with carts and orders
- Various administrative capabilities
- Run test cases to verify system capabilities

The remaining sections explain how to run the CLI, illustrating
commands and parameters required to interact with the Ecosystem
Platform.

Full documentation is available in in the
[osc-dm-mesh-doc](https://github.com/brodagroupsoftware/osc-dm-mesh-doc)
repo.

This application interacts with other applications. You can run
the full set of applications by following instructions in the
[osc-dm-mesh-doc](https://github.com/brodagroupsoftware/osc-dm-mesh-doc)
repo.

## Prerequisites

Python must be available, preferably in a virtual environment (venv).

## Setting up your Environment

Some environment variables are used by various source code and scripts.
Setup your environment as follows (note that "source" is used)
~~~~
source ./bin/environment.sh
~~~~

It is recommended that a Python virtual environment be created.
We have provided several convenience scripts to create and activate
a virtual environment. To create a new virtual environment using
these convenience scripts, execute the following (this will
create a directory called "venv" in your current working directory):
~~~~
$PROJECT_DIR/bin/venv.sh
~~~~

Once your virtual enviornment has been created, it can be activated
as follows (note: you *must* activate the virtual environment
for it to be used, and the command requires "source" to ensure
environment variables to support venv are established correctly):
~~~~
source $PROJECT_DIR/bin/vactivate.sh
~~~~

Install the required libraries as follows:
~~~~
pip install -r requirements.txt
~~~~

Note that if you wish to run test cases then you will need
to also install "pytest" (it is not installed by default as
it is a development rather than product dependency).
~~~~
pip install pytest
~~~~

## Configuring the CLI

The CLI communicates with a Ecosystem Platform proxy
and hence requries a host and port. For your convenience,
this tutorial uses HOST and PORT variables to contain
these values.

Also, verbose logging can be enabled using the "--verbose" tag.
For your convenience, each of the examples in this tutorial
use an environment variable, VERBOSE, which if set to
"--verbose" will permit extended logging in the CLI.

Setup your environment as follows:
~~~~
HOST=localhost ;
PORT=20000 ;
VERBOSE="--verbose"
~~~~

To disable verbose logging, unset VERBOSE:
~~~~
VERBOSE=""
~~~~

## Basic Concepts

There are several key concepts that the CLI acts upon:
- Users: Can be registered, logged in/out, and viewed
- Products: can have UUIDs generated, be registered, and viewed
- Carts and Orders: Users can put products of interest into
carts which can then be ordered (to create an order); both carts can be
viewed as well as individual orders or list of orders in an order
history

### Data Product Configuration

The data product configuration as well as artifact
configuration are contained in the following directory:
~~~~
config
~~~~

TODO: Configuration should be structured to allow
domains, then data product names:
~~~~
config/domain/name
~~~~

#### Data Products (Configuration)

A sample data product is available in the data product
configuration directory, called "rmi".  The full
set of data product assets are located in:
~~~~
config/rmi
~~~~

The configuration for this data product is located in:
~~~~
config/rmi/product.yaml
~~~~

Each data product has several attributes:
- domain: the data product domain; domains are unique across all
data products
- name: The data product name; names must be unique in a domain
- description: 1-2 sentence description of the data product
- tags: Used for searching
- publisher: The data product publisher, or data product owner

The sample product configuration is as follows:
- domain: brodagroupsoftware.com
- name: rmi.dataproduct
- description: US Utility data provided by RMI
- tags: ["utilities", "emissions"]
- publisher: publisher.user@brodagroupsoftware.com

#### Artifacts (Configuration) and Other Data Product Characteristics

Numerous artifacts are available for the sample data product:
~~~~
config/rmi/artifacts
~~~~

Each artifact has several attributes:
- name: Unique name within the set of artifacts
- description: 1-2 sentnece description
- tags: Used to augment searching
- license: Defines Defines how artifact can be used or shared
- securitypolicy: Access policy for the artifact
- data: URLs to the artifact

There are several other configuration files:
- bundles: groups of artifacts treated as a single entity
- metadata: API specifications to "discover" the data product
- provenance: Lineage information for the data product
- queries: vetted queries permitted by the data product

### User: Publishers, Subscribers, Guest Users, and Adminstrators

There are several types of users that can interact
with the Ecosystem Platform:
- Guest Users: Lowest previlege users; Genera users
can view the marketplace but are not able to subscribe
to or download data, nor publish data products
- Publishers: Can do all of the things a general user
can do but are also able to publish data products (which makes
them available in the Marketplace/Registry)
- Subscribers: Can do all of the things a general user
can do but are also able to subscribe to and download data products
- Administrators: Can do all of the things a general user
can do but are also able to administer the Ecosystem Platform
and Marketplace/Registry, and create users.

## Getting Started

In this tutorial, we will perform several steps:
- Start the Data Marketplace/Registry
- Initialize services, using the administration CLI
- Register users, using the administration CLI
- Publish a sample data product, using the publisher CLI
- View the data product in the Marketplace/Registry, using
the subscriber CLI
- Discover the interfaces made available by the
data product, using the subscriber CLI
- Download data from the data product, using the subscriber CLI
- View the data product data (TODO: Geospatial Ecosystem Platform
integration), using the subscriber CLI


## Starting the Ecosystem Platform

The Ecosystem Platform components interact with each other
so the simplest way to get all of them running is
to use the full Ecosystem Platform docker-compose.

The Ecosystem Platform docker compose is in a different directory
and hence must be started in a separate terminal window:
~~~~
cd $HOME_DIR/bgssrv-dm

source ./bin/environment.sh

$PROJECT_DIR/app/startd.sh
~~~~

At this point the full set of services should be running.
This can be verified by running the following docker command:
~~~~
docker ps
CONTAINER ID   IMAGE                                          COMMAND                  CREATED         STATUS         PORTS                              NAMES
28639179566e   brodagroupsoftware/bgssrv-dmproxy:latest       "python3 /app/server…"   6 seconds ago   Up 4 seconds   0.0.0.0:20000->8000/tcp            docker-bgssrv-dmproxy-1
c36fae20722e   brodagroupsoftware/bgssrv-dmui:latest          "docker-entrypoint.s…"   6 seconds ago   Up 4 seconds   0.0.0.0:3000->3000/tcp             docker-bgssrv-dmui-1
4a8858c09e9f   brodagroupsoftware/bgssrv-dmregistrar:latest   "python3 /app/server…"   6 seconds ago   Up 4 seconds   0.0.0.0:21000->8000/tcp            docker-bgssrv-dmregistrar-1
0838a1bd37f0   quay.io/coreos/etcd:v3.5.0                     "/usr/local/bin/etcd"    6 seconds ago   Up 4 seconds   2379-2380/tcp                      docker-etcd2-1
f86bb447829f   quay.io/coreos/etcd:v3.5.0                     "/usr/local/bin/etcd"    6 seconds ago   Up 4 seconds   2379-2380/tcp                      docker-etcd3-1
f4aec44f8ef7   quay.io/coreos/etcd:v3.5.0                     "/usr/local/bin/etcd"    6 seconds ago   Up 4 seconds   0.0.0.0:2379-2380->2379-2380/tcp   docker-etcd1-1
~~~~

## Starting a Data Product

A data product interacts with the Ecosystem Platform
so the simplest way of running one is
to use the data product docker-compose.

A data product docker compose is in a different directory
and hence must be started in a separate terminal window:
~~~~
cd $HOME_DIR/bgssrv-dmproduct

source ./bin/environment.sh

$PROJECT_DIR/app/startd.sh
~~~~

At this point the full set of services as well as the
data product instance should be running.
This can be verified by running the following docker command:
~~~~
docker ps
CONTAINER ID   IMAGE                                          COMMAND                  CREATED         STATUS         PORTS                              NAMES
6a1a62f1b9d4   brodagroupsoftware/bgssrv-dmproduct:latest     "python3 /app/server…"   5 seconds ago   Up 4 seconds   0.0.0.0:24000->8000/tcp            docker-bgssrv-dmproduct-1
28639179566e   brodagroupsoftware/bgssrv-dmproxy:latest       "python3 /app/server…"   3 minutes ago   Up 3 minutes   0.0.0.0:20000->8000/tcp            docker-bgssrv-dmproxy-1
c36fae20722e   brodagroupsoftware/bgssrv-dmui:latest          "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   0.0.0.0:3000->3000/tcp             docker-bgssrv-dmui-1
4a8858c09e9f   brodagroupsoftware/bgssrv-dmregistrar:latest   "python3 /app/server…"   3 minutes ago   Up 3 minutes   0.0.0.0:21000->8000/tcp            docker-bgssrv-dmregistrar-1
0838a1bd37f0   quay.io/coreos/etcd:v3.5.0                     "/usr/local/bin/etcd"    3 minutes ago   Up 3 minutes   2379-2380/tcp                      docker-etcd2-1
f86bb447829f   quay.io/coreos/etcd:v3.5.0                     "/usr/local/bin/etcd"    3 minutes ago   Up 3 minutes   2379-2380/tcp                      docker-etcd3-1
f4aec44f8ef7   quay.io/coreos/etcd:v3.5.0                     "/usr/local/bin/etcd"    3 minutes ago   Up 3 minutes   0.0.0.0:2379-2380->2379-2380/tcp   docker-etcd1-1
~~~~

Note the very first line with the data product (NAME is docker-bgssrv-dmproduct-1).

## Working with Users

User can be registered.  Once registered, you can view
all users or a specific user.

User must be registered in a role, either "guest", "subscriber",
"publisher", or "administrator".

### Register a Guest

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

{"uuid": "7eec771b-6140-4741-9845-2e52857c1cb3"}
~~~~

### View Users

View all users:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve

[{"uuid": "7eec771b-6140-4741-9845-2e52857c1cb3", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-28 23:13:19.375", "updatetimestamp": "2024-03-28 23:13:19.375", "role": "guest"}]
~~~~

### View a User by UUID

View a user by their UUID (we will use the same UUID that was
returned in the previous steps):
~~~~
UUID="7eec771b-6140-4741-9845-2e52857c1cb3" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --uuid "$UUID"

{"uuid": "7eec771b-6140-4741-9845-2e52857c1cb3", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}
~~~~

### View a User by Email

View all user roles by email (note that user can have multiple roles):
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --email "$EMAIL"

[{"uuid": "7eec771b-6140-4741-9845-2e52857c1cb3", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}, {"uuid": "d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 14:53:27.378", "updatetimestamp": "2024-03-17 14:53:27.378", "role": "guest"}]
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

[{"uuid": "7eec771b-6140-4741-9845-2e52857c1cb3", "contact": {"name": "guest.user@brodagroupsoftware.com", "email": "Guest User", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 15:24:07.411", "updatetimestamp": "2024-03-17 15:24:07.411", "role": "guest"}, {"uuid": "d6e1fcc4-943a-491e-9dbb-a1ea190e9fb0", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-17 14:53:27.378", "updatetimestamp": "2024-03-17 14:53:27.378", "role": "guest"}]
~~~~

## Logging In/Out and Statistics

To login a guest:
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
ROLE="guest" ;
PASSWORD="a-fake-password" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --login \
    --role "$ROLE" \
    --email "$EMAIL" \
    --password "$PASSWORD"

{"uuid": "e32961f4-d871-4faf-98c2-4f44476a42a1", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-04 18:41:05.797", "updatetimestamp": "2024-03-04 18:41:05.797", "role": "guest"}
~~~~

To logout a guest:
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
ROLE="guest" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --logout \
    --role "$ROLE" \
    --email "$EMAIL"

{"uuid": "e32961f4-d871-4faf-98c2-4f44476a42a1", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-04 18:41:05.797", "updatetimestamp": "2024-03-04 18:41:05.797", "role": "guest"}
~~~~

To retrieve auth statistics for all users:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --statistics

[{"role": "guest", "email": "guest.user@brodagroupsoftware.com", "status": "authorized"}, {"role": "guest", "email": "x@brodagroupsoftware.com", "status": "authorized"}]
~~~~

To retrieve auth statistics for a specific user:
~~~~
EMAIL="guest.user@brodagroupsoftware.com"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --status \
    --email "$EMAIL"

~~~~

## Working with Data Products

Products and their artifacts must have a unique identifier (UUID)
such that they can be recognized and registered in the
Ecosystem Platform.  Once UUIDs have been generated then
products can be registered.  Once registered products and
their artifacts can be viewed.

### Generating a Data Product

[Documentation for generating data products](/docs/product-generation.md)

### Assigning UUIDs to a Data Product

UUIDs are assigned by the data product owner.  To generate
UUIDs, execute the following command:

~~~~
DATAPRODUCT_DIR="$SAMPLES_DIR/dataproducts/rmi";
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --assign \
    --directory "$DATAPRODUCT_DIR"

{"uuids": "/Users/ericbroda/Development/scratch/bgsdat-samples/dataproducts/rmi/uuids.yaml", "product_uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "artifact_uuids": [{"Assets Earnings Investments": "0586c61c-9aac-4202-aeda-d3e3dfad384c"}, {"Customer Sales": "352a37b1-9fae-4df4-bcef-a5eb68bab9d4"}, {"Debit Equity Returns": "f47d3792-6995-4958-af38-3d7385632a32"}, {"Emissions Targets": "63071083-541b-472d-91ea-6325f214f2c8"}, {"Employees": "7ba33722-596c-493e-8c6f-58b1748f3de6"}, {"Expenditure Bills Burden": "6e889d55-ef19-4a4c-a3c9-c9fe2c9744fd"}, {"Expenditure Bills Burden Detail": "07497ece-7a47-4c4e-8fdb-409b3817e46c"}, {"Housing Units Income": "96bed246-1123-450a-aeea-94d72b9f7bc2"}, {"Net Plant Balance": "70177ae9-f886-496d-a9c8-82d483822e24"}, {"Operations Emissions by Fuel": "1a17518b-fb95-4573-831c-15218e2e8e90"}, {"Operations Emissions by Tech": "0f9b60cb-e18f-4e38-9e1f-cd890098d2e9"}, {"Revenue by Tech": "2bc48809-a916-43dc-bf82-907859e72bc2"}, {"State Targets": "d6b7a49d-9a3f-43e6-a56a-33795c7ffd30"}, {"State Utility Polcies": "423eb06b-cd79-4a52-a864-eca1f4ce79b8"}, {"Uneconomic Dispatch": "d81dcf27-7df3-4b80-8182-5dce58096f77"}, {"Utility Information": "e9273326-6848-4859-beb8-10c1949af89e"}, {"Utility State Map": "262fcfab-c06c-4559-ab1e-65bfd1903ddb"}]}
~~~~

Note that the UUIDs provided for your data product at the
time of registration are stored in a file called
"uuids.yaml" in the data product directory.  This file
is used extensively by data product services and
is an item of record for your data product.  An example of
the contents of the file is shown below:
~~~~
#####
#
# This file contains the UUIDs for your product and artifacts (by name)
#
# -----
#
# Registered on: 11-Apr-2024 11:55:33
# Registered by: ericbroda
#
#####
product_uuid: 65bf83f8-3e00-4d7a-9553-db1491fd577c
artifact_uuids:
- Assets Earnings Investments: 0586c61c-9aac-4202-aeda-d3e3dfad384c
- Customer Sales: 352a37b1-9fae-4df4-bcef-a5eb68bab9d4
- Debit Equity Returns: f47d3792-6995-4958-af38-3d7385632a32
- Emissions Targets: 63071083-541b-472d-91ea-6325f214f2c8
- Employees: 7ba33722-596c-493e-8c6f-58b1748f3de6
- Expenditure Bills Burden: 6e889d55-ef19-4a4c-a3c9-c9fe2c9744fd
- Expenditure Bills Burden Detail: 07497ece-7a47-4c4e-8fdb-409b3817e46c
- Housing Units Income: 96bed246-1123-450a-aeea-94d72b9f7bc2
- Net Plant Balance: 70177ae9-f886-496d-a9c8-82d483822e24
- Operations Emissions by Fuel: 1a17518b-fb95-4573-831c-15218e2e8e90
- Operations Emissions by Tech: 0f9b60cb-e18f-4e38-9e1f-cd890098d2e9
- Revenue by Tech: 2bc48809-a916-43dc-bf82-907859e72bc2
- State Targets: d6b7a49d-9a3f-43e6-a56a-33795c7ffd30
- State Utility Polcies: 423eb06b-cd79-4a52-a864-eca1f4ce79b8
- Uneconomic Dispatch: d81dcf27-7df3-4b80-8182-5dce58096f77
- Utility Information: e9273326-6848-4859-beb8-10c1949af89e
- Utility State Map: 262fcfab-c06c-4559-ab1e-65bfd1903ddb

~~~~

### Register a Data Product

Each data product has a service that serves
data product information.  This service's address
must be registered with the basic data product
information.  At that point, all artifact
requests are handled directly by the data product.

Note that a publisher must be created/registered *before* you
can register the product.

The data product service can be found using
docker commands:
~~~~
docker ps

CONTAINER ID   IMAGE                                          COMMAND                  CREATED          STATUS          PORTS                              NAMES
:
416324234b60   brodagroupsoftware/bgssrv-dmproduct:latest     "python3 /app/server…"   34 minutes ago   Up 34 minutes   0.0.0.0:24000->8000/tcp            docker-bgssrv-dmproduct-1
:
~~~~
Examine the "NAMES" column (above: "docker-bgssrv-dmproduct-1") for your
data product instance and use the ports info.  Since the
data product will be running inside the docker compose environment
we need to advertise it as the internal docker port (the number after "->"
which in our case is 8000).

Now, as we register the product we need to also provide
a location for the configuration ("DATAPRODUCT_DIR") and
also the previously identified address where it can be
accessed.

Register a Product:
~~~~
DATAPRODUCT_DIR="$SAMPLES_DIR/dataproducts/rmi";
ADDRESS="http://bgssrv-dmproduct-0:8000" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --register \
    --directory "$DATAPRODUCT_DIR" \
    --address "$ADDRESS"

{"product": {"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-04-11 20:07:58.026", "updatetimestamp": "2024-04-11 20:07:58.026"}, "fqfilename": "/Users/ericbroda/Development/scratch/bgsdat-samples/dataproducts/rmi/registration.yaml"}
~~~~

Note that the address provided for your data product at the
time of registration is stored, for your records, in a file called
"registration.yaml" in the data product directory.  An example of
the contents of the file is shown below:
~~~~
#####
#
# Data Product Address Registration
#
# This file contains the address for your product
#
# -----
#
# Registered on: 11-Apr-2024 16:07:57
# Registered by: ericbroda
#
#####
address: http://bgssrv-dmproduct-0:8000
~~~~

### View all Products

~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve

[{"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-05-03 21:43:07.674", "updatetimestamp": "2024-05-03 21:43:07.674"}]
~~~~

### View a Products for List of UUIDs

Let's get information for a list of products (note
that for simplicity sake we will use the same UUIDs
in the list)
~~~~
UUID1="65bf83f8-3e00-4d7a-9553-db1491fd577c"
UUID2="65bf83f8-3e00-4d7a-9553-db1491fd577c"
UUIDS="$UUID1 $UUID2"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --uuids "$UUIDS"

{"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}
~~~~

### View a Product for single UUID

Let's get information for single product:
~~~~
UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --uuid "$UUID"

{"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}
~~~~

### View a Product by Namespace/Name

~~~~
NAMESPACE="brodagroupsoftware.com" ;
NAME="rmi.dataproduct" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --namespace "$NAMESPACE" \
    --name "$NAME"

{"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}
~~~~

### View all Product in a Namespace

~~~~
NAMESPACE="brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --namespace "$NAMESPACE"

[{"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-03-17 16:26:23.144", "updatetimestamp": "2024-03-17 16:26:23.144"}]
~~~~

### Searching Products

~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --search \
    --query "find all temperature products"

~~~~


## Working with Data Product Artifacts

### Discover Data Product Instances (connect directly to Data Product Instance)

NOTE: The data product must be registered and then running for this
capability to work properly.

Discover is like view/retrieve, except discover gets
more details directly from the product:
~~~~
UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --discover \
    --uuid "$UUID"

{"product": {"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": null, "createtimestamp": "2024-04-28 15:24:56.535", "updatetimestamp": "2024-04-28 15:24:56.535"}, "artifacts": [{"uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Assets Earnings Investments", "description": "Detailed breakdown of utility assets in electric rate base, earnings on these assets, and annual investments (capital additions) by technology.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/assets_earnings_investments.csv"}, {"relationship": "sample", "mimetype": "text/csv", "url": "https://localhost:8000/samples/artifact-001.csv"}, {"relationship": "metadata", "mimetype": "text/csv", "url": "https://localhost:8000/metadata/artifact-001.json"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "fa614c23-f91b-46b1-9ba8-0718d761af93", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Customer Sales", "description": "Number of customers, MWh electricity sales, and revenues by customer type.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/customers_sales.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "26d49b15-9313-4b0e-95b3-7a173c024ec8", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Debit Equity Returns", "description": "Rate base, equity, debt, returns, earnings, interest expense, tax expense, and the rates of return used for earnings and revenue calculations.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/debt_equity_returns.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "3f00e58d-3125-44e6-9a8e-399d49517c60", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Emissions Targets", "description": "CO2 emissions and projections, as well as electricity generation and projections and comparison to RMI 1.5\u00b0C decarbonization pathway for the US electricity sector.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/emissions_targets.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "549c248a-732f-450f-ab83-7419f8ebb671", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Employees", "description": "Number of employees that work at large power plants, by technology, for each utility", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/employees.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "4385f285-2558-4f81-a26a-7dd2b642aa7f", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "7fd0bf8c-b9cb-473b-9a94-086904e3d073", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden Detail", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group. Broken down into additional components and details compared to expenditure_bills_burden, leading a large file size (575 MB) that cannot be opened in Excel.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden_detail.csv.zip"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "a06b39e6-4e45-4884-ac1f-1b1447777f3b", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "79d5aea0-98fc-4294-a5d9-fcbea6fa22f7", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Net Plant Balance", "description": "Original cost, accumulated depreciation, and remaining net plant balance of electric plants in service, by FERC classification.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/net_plant_balance.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "2aedca34-539b-4b67-8e87-9346c2874907", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Fuel", "description": "Generation, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Within each generator and for purchased power, data values are differentiated by fuel type.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_fuel.zip"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "aa800b61-2509-467b-88a9-fe87dcd5f5a5", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Tech", "description": "Capacity, generation, capacity factor, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Each generator is identified by a single technology.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_tech.zip"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "f9045f7c-3840-420e-bbd3-5997e791d36a", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Revenue by Tech", "description": "Revenues for each utility, by technology and component, for each utility.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/revenue_by_tech.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "7757225d-d79a-42c9-9c38-8932a4b7b927", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Targets", "description": "Greenhouse gas (GHG) and renewable portfolio standard (RPS) data by state, including baseline, interim, and final target years", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_targets.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "89ad6ed7-79b5-493f-b78f-6eb52f47f301", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Utility Polcies", "description": "Policy data shown on the \"Policy & Regulations\" dashboard of the Utility Transition Hub Portal, by state and utility.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_utility_policies.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "70ad811a-8c89-4a2c-bcbb-35e10457fce9", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Uneconomic Dispatch", "description": "Capacity and monthly cash flows used for monthly net revenues and gross losses for all operating coal plants above 5 MWs in the nation", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "url": "https://utilitytransitionhub.rmi.org/static/data_download/uneconomic_dispatch_monthly_cash_flow.xlsx"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "f70c9d81-c74e-4beb-8d94-e6fcfbacf4a8", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility Information", "description": "Utility identifiers such as name, ID numbers from various sources, and utility type. Includes connections from operating companies to parent companies.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_information.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "b9eed26c-be23-47c8-87f2-ff3cba4c7862", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility State Map", "description": "A list of states that each utility operates in, including capacity owned in state, capacity operated in state, and energy sales in state.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_state_map.csv"}], "createtimestamp": null, "updatetimestamp": null}]}
~~~~

### Discover all Artifacts for a Product (directly to Product)

~~~~
PRODUCT_UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --discover \
    --productuuid "$PRODUCT_UUID"

[{"uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Assets Earnings Investments", "description": "Detailed breakdown of utility assets in electric rate base, earnings on these assets, and annual investments (capital additions) by technology.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/assets_earnings_investments.csv"}, {"relationship": "sample", "mimetype": "text/csv", "url": "https://localhost:8000/samples/artifact-001.csv"}, {"relationship": "metadata", "mimetype": "text/csv", "url": "https://localhost:8000/metadata/artifact-001.json"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "fa614c23-f91b-46b1-9ba8-0718d761af93", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Customer Sales", "description": "Number of customers, MWh electricity sales, and revenues by customer type.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/customers_sales.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "26d49b15-9313-4b0e-95b3-7a173c024ec8", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Debit Equity Returns", "description": "Rate base, equity, debt, returns, earnings, interest expense, tax expense, and the rates of return used for earnings and revenue calculations.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/debt_equity_returns.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "3f00e58d-3125-44e6-9a8e-399d49517c60", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Emissions Targets", "description": "CO2 emissions and projections, as well as electricity generation and projections and comparison to RMI 1.5\u00b0C decarbonization pathway for the US electricity sector.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/emissions_targets.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "549c248a-732f-450f-ab83-7419f8ebb671", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Employees", "description": "Number of employees that work at large power plants, by technology, for each utility", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/employees.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "4385f285-2558-4f81-a26a-7dd2b642aa7f", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "7fd0bf8c-b9cb-473b-9a94-086904e3d073", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Expenditure Bills Burden Detail", "description": "Expenditure, average residential customer energy bill, and average residential customer energy burden for each utility by technology and customer group. Broken down into additional components and details compared to expenditure_bills_burden, leading a large file size (575 MB) that cannot be opened in Excel.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/expenditure_bills_burden_detail.csv.zip"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "a06b39e6-4e45-4884-ac1f-1b1447777f3b", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "79d5aea0-98fc-4294-a5d9-fcbea6fa22f7", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Net Plant Balance", "description": "Original cost, accumulated depreciation, and remaining net plant balance of electric plants in service, by FERC classification.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/net_plant_balance.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "2aedca34-539b-4b67-8e87-9346c2874907", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Fuel", "description": "Generation, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Within each generator and for purchased power, data values are differentiated by fuel type.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_fuel.zip"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "aa800b61-2509-467b-88a9-fe87dcd5f5a5", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Operations Emissions by Tech", "description": "Capacity, generation, capacity factor, fuel consumption, and emissions of CO2, NOx, and SOx for each generator owned by each utility, and for power purchased by each utility. Each generator is identified by a single technology.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/zip", "url": "https://utilitytransitionhub.rmi.org/static/data_download/operations_emissions_by_tech.zip"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "f9045f7c-3840-420e-bbd3-5997e791d36a", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Revenue by Tech", "description": "Revenues for each utility, by technology and component, for each utility.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/revenue_by_tech.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "7757225d-d79a-42c9-9c38-8932a4b7b927", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Targets", "description": "Greenhouse gas (GHG) and renewable portfolio standard (RPS) data by state, including baseline, interim, and final target years", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_targets.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "89ad6ed7-79b5-493f-b78f-6eb52f47f301", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "State Utility Polcies", "description": "Policy data shown on the \"Policy & Regulations\" dashboard of the Utility Transition Hub Portal, by state and utility.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/state_utility_policies.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "70ad811a-8c89-4a2c-bcbb-35e10457fce9", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Uneconomic Dispatch", "description": "Capacity and monthly cash flows used for monthly net revenues and gross losses for all operating coal plants above 5 MWs in the nation", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "url": "https://utilitytransitionhub.rmi.org/static/data_download/uneconomic_dispatch_monthly_cash_flow.xlsx"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "f70c9d81-c74e-4beb-8d94-e6fcfbacf4a8", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility Information", "description": "Utility identifiers such as name, ID numbers from various sources, and utility type. Includes connections from operating companies to parent companies.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_information.csv"}], "createtimestamp": null, "updatetimestamp": null}, {"uuid": "b9eed26c-be23-47c8-87f2-ff3cba4c7862", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Utility State Map", "description": "A list of states that each utility operates in, including capacity owned in state, capacity operated in state, and energy sales in state.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/utility_state_map.csv"}], "createtimestamp": null, "updatetimestamp": null}]
~~~~

### Discover a Specific Artifact for a Product (directly to Product)

~~~~
PRODUCT_UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c"
ARTIFACT_UUID="e6ac3592-5764-443c-a45e-39c801f01e9a"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --discover \
    --productuuid "$PRODUCT_UUID" \
    --uuid "$ARTIFACT_UUID"

{"uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a", "productuuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Assets Earnings Investments", "description": "Detailed breakdown of utility assets in electric rate base, earnings on these assets, and annual investments (capital additions) by technology.", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/assets_earnings_investments.csv"}, {"relationship": "sample", "mimetype": "text/csv", "url": "https://localhost:8000/samples/artifact-001.csv"}, {"relationship": "metadata", "mimetype": "text/csv", "url": "https://localhost:8000/metadata/artifact-001.json"}], "createtimestamp": null, "updatetimestamp": null}
~~~~

## Working with Carts and Orders

Note that only subscribers (ie. users that have
been registered in role "subscriber") can have a cart.

### Register a Subscriber

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

{"uuid": "2e8da4bb-fa34-4dcb-9971-29ee93eb5ad3"}
~~~~

### View all Carts

Let's view the carts available (there should only be one if you are following
these steps).  The cart UUID will be used in subsequent steps):
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve

[{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-05-08 20:47:33.908", "updatetimestamp": "2024-05-08 20:47:33.908"}]
~~~~

### View a Cart by UUID

~~~~
CART_UUID="ff5150ac-a484-4b64-8b23-047a66f450e9" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve \
    --uuid "$CART_UUID"

{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-18 20:44:37.301", "updatetimestamp": "2024-03-18 20:44:37.301"}
~~~~

### View a Cart by User (email)

~~~~
EMAIL="subscriber.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve \
    --email "$EMAIL"

{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-18 20:44:37.301", "updatetimestamp": "2024-03-18 20:44:37.301"}
~~~~

### Add an Item to a Cart (using UUID)

Add an item (defined by a product uuid and artifact uuid)
to a cart:
~~~~
PRODUCT_UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c" ;
ARTIFACT_UUID="e6ac3592-5764-443c-a45e-39c801f01e9a" ;
CART_UUID="ff5150ac-a484-4b64-8b23-047a66f450e9" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --add \
    --uuid "$CART_UUID" \
    --productuuid "$PRODUCT_UUID" \
    --artifactuuid "$ARTIFACT_UUID"

{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product_uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "artifact_uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a"}], "createtimestamp": "2024-03-21 12:26:04.269", "updatetimestamp": "2024-03-21 12:26:04.269"}
~~~~

### Add an Item to a Cart (using EMAIL)

Add an item (defined by a product uuid and artifact uuid)
to a cart:
~~~~
PRODUCT_UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c" ;
ARTIFACT_UUID="e6ac3592-5764-443c-a45e-39c801f01e9a" ;
EMAIL="subscriber.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --add \
    --email "$EMAIL" \
    --productuuid "$PRODUCT_UUID" \
    --artifactuuid "$ARTIFACT_UUID"

{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product_uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "artifact_uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a"}], "createtimestamp": "2024-03-21 12:26:04.269", "updatetimestamp": "2024-03-21 12:26:04.269"}
~~~~

### Removing an Item from a Cart (Using UUID)

Remove an item (defined by a product uuid and artifact uuid)
that exists in a cart:
~~~~
PRODUCT_UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c" ;
ARTIFACT_UUID="e6ac3592-5764-443c-a45e-39c801f01e9a" ;
CART_UUID="ff5150ac-a484-4b64-8b23-047a66f450e9" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --remove \
    --uuid "$CART_UUID" \
    --productuuid "$PRODUCT_UUID" \
    --artifactuuid "$ARTIFACT_UUID"

{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-19 20:55:28.662", "updatetimestamp": "2024-03-19 20:55:28.662"}
~~~~

### Removing an Item from a Cart (Using EMAIL)

Remove an item (defined by a product uuid and artifact uuid)
that exists in a cart:
~~~~
PRODUCT_UUID="65bf83f8-3e00-4d7a-9553-db1491fd577c" ;
ARTIFACT_UUID="e6ac3592-5764-443c-a45e-39c801f01e9a" ;
EMAIL="subscriber.user@brodagroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --remove \
    --email "$EMAIL" \
    --productuuid "$PRODUCT_UUID" \
    --artifactuuid "$ARTIFACT_UUID"

{"uuid": "ff5150ac-a484-4b64-8b23-047a66f450e9", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-03-19 20:55:28.662", "updatetimestamp": "2024-03-19 20:55:28.662"}
~~~~

### Create an order (ie. Purchase a Cart)

To create an order and purchase a cart:
~~~~
CART_UUID="ff5150ac-a484-4b64-8b23-047a66f450e9" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --purchase \
    --cartuuid "$CART_UUID"

{"uuid": "c7cb0dd2-0cd4-4fc7-9faa-a547ee116a75"}
~~~~

### View an Order

To view an existing order:
~~~~
ORDER_UUID="c7cb0dd2-0cd4-4fc7-9faa-a547ee116a75" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --retrieve \
    --uuid "$ORDER_UUID"

{"uuid": "c7cb0dd2-0cd4-4fc7-9faa-a547ee116a75", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "ab55bcdd-6a7e-4c7c-940b-9d1c198ffede", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-03-23 14:42:51.026", "updatetimestamp": "2024-03-23 14:42:51.026"}, "artifact": {"uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}}], "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}, "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}
~~~~

### View a User's Order History

To view a user's order history:
~~~~
EMAIL="subscriber.user@brodadgroupsoftware.com" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --retrieve \
    --email "$EMAIL"

[{"uuid": "c7cb0dd2-0cd4-4fc7-9faa-a547ee116a75", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "ab55bcdd-6a7e-4c7c-940b-9d1c198ffede", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "65bf83f8-3e00-4d7a-9553-db1491fd577c", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://bgssrv-dmproduct-0:8000", "createtimestamp": "2024-03-23 14:42:51.026", "updatetimestamp": "2024-03-23 14:42:51.026"}, "artifact": {"uuid": "e6ac3592-5764-443c-a45e-39c801f01e9a", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Housing Units Income", "description": "Number of housing units and income by customer group for each utility.", "tags": ["utilities", "emissions"], "license": "Creative Commons 4.0", "securitypolicy": "public", "data": {"mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/housing_units_income.csv"}, "createtimestamp": null, "updatetimestamp": null}}], "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}, "createtimestamp": "2024-03-23 14:44:22.995", "updatetimestamp": "2024-03-23 14:44:22.995"}]
~~~~

## Monitoring Components

To monitor ecosystem platform health:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT monitor \
    --health

{"osc-dm-proxy-srv": "OK", "osc-dm-registrar-srv": "OK", "osc-dm-search-srv": "OK", "http://osc-dm-product-srv-0:8000": "OK"}
~~~~

To monitor ecosystem platform metrics:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT monitor \
    --metrics

{"osc-dm-proxy-srv": {"osc-dm-search-srv": {"http://osc-dm-proxy-srv:8000/api/registrar/products": {"200": 9, "500": 1}, "http://osc-dm-proxy-srv:8000/api/proxy/health": {"200": 7}, "http://osc-dm-proxy-srv:8000/api/registrar/health": {"200": 7}, "http://osc-dm-proxy-srv:8000/api/search/health": {"503": 2, "200": 5}, "http://osc-dm-proxy-srv:8000/api/proxy/metrics": {"200": 6}, "http://osc-dm-proxy-srv:8000/api/registrar/metrics": {"200": 6}, "http://osc-dm-proxy-srv:8000/api/search/metrics": {"503": 2, "200": 4}, "http://osc-dm-proxy-srv:8000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/health": {"200": 5}, "http://osc-dm-proxy-srv:8000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/metrics": {"200": 4}}, "ericbroda": {"http://localhost:20000/api/registrar/users": {"200": 4}, "http://localhost:20000/api/registrar/users/uuid/b2c8fac1-0a6d-4632-902f-10986ab9bbce": {"200": 1}, "http://localhost:20000/api/registrar/users/email/guest.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/users/role/guest/email/guest.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/products": {"200": 4}, "http://localhost:20000/api/registrar/products/uuids/": {"200": 1}, "http://localhost:20000/api/registrar/products/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a": {"200": 1}, "http://localhost:20000/api/registrar/products/namespace/brodagroupsoftware.com/name/rmi.dataproduct": {"200": 1}, "http://localhost:20000/api/registrar/products/namespace/brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/search/query": {"200": 1}, "http://localhost:20000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a": {"200": 2}, "http://localhost:20000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/artifacts": {"200": 3}, "http://localhost:20000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/artifacts/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 2}, "http://localhost:20000/api/registrar/users/role/subscriber/email/subscriber.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/carts": {"200": 1}, "http://localhost:20000/api/registrar/carts/uuid/788122b1-9150-4e96-a1df-204ee06f8869": {"200": 1}, "http://localhost:20000/api/registrar/carts/email/subscriber.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/carts/uuid/788122b1-9150-4e96-a1df-204ee06f8869/b6e05972-fe25-44aa-b5a0-db6e100ca95a/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 3}, "http://localhost:20000/api/registrar/carts/email/subscriber.user@brodagroupsoftware.com/b6e05972-fe25-44aa-b5a0-db6e100ca95a/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 2}, "http://osc-dm-proxy-srv:8000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/artifacts/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 1}, "http://localhost:20000/api/registrar/orders": {"200": 1}, "http://localhost:20000/api/registrar/orders/uuid/764b3e72-d38b-4d66-8763-2c20e2f8cbb0": {"200": 1}, "http://localhost:20000/api/monitor/health": {"200": 2}, "http://localhost:20000/api/monitor/metrics": {"200": 2}}}, "osc-dm-registrar-srv": {"osc-dm-search-srv": {"http://osc-dm-proxy-srv:8000/api/registrar/products": {"200": 9, "500": 1}, "http://osc-dm-proxy-srv:8000/api/registrar/health": {"200": 7}, "http://osc-dm-proxy-srv:8000/api/registrar/metrics": {"200": 6}, "http://osc-dm-registrar-srv:8000/api/registrar/products": {"200": 6}, "http://osc-dm-registrar-srv:8000/api/registrar/products/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a": {"200": 9}}, "ericbroda": {"http://localhost:20000/api/registrar/users": {"200": 4}, "http://localhost:20000/api/registrar/users/uuid/b2c8fac1-0a6d-4632-902f-10986ab9bbce": {"200": 1}, "http://localhost:20000/api/registrar/users/email/guest.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/users/role/guest/email/guest.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/products": {"200": 4}, "http://localhost:20000/api/registrar/products/uuids/": {"200": 1}, "http://localhost:20000/api/registrar/products/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a": {"200": 1}, "http://localhost:20000/api/registrar/products/namespace/brodagroupsoftware.com/name/rmi.dataproduct": {"200": 1}, "http://localhost:20000/api/registrar/products/namespace/brodagroupsoftware.com": {"200": 1}, "http://osc-dm-registrar-srv:8000/api/registrar/products/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a": {"200": 8}, "http://localhost:20000/api/registrar/users/role/subscriber/email/subscriber.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/carts": {"200": 1}, "http://localhost:20000/api/registrar/carts/uuid/788122b1-9150-4e96-a1df-204ee06f8869": {"200": 1}, "http://localhost:20000/api/registrar/carts/email/subscriber.user@brodagroupsoftware.com": {"200": 1}, "http://localhost:20000/api/registrar/carts/uuid/788122b1-9150-4e96-a1df-204ee06f8869/b6e05972-fe25-44aa-b5a0-db6e100ca95a/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 3}, "http://localhost:20000/api/registrar/carts/email/subscriber.user@brodagroupsoftware.com/b6e05972-fe25-44aa-b5a0-db6e100ca95a/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 2}, "http://localhost:20000/api/registrar/orders": {"200": 1}, "http://localhost:20000/api/registrar/orders/uuid/764b3e72-d38b-4d66-8763-2c20e2f8cbb0": {"200": 1}}}, "osc-dm-search-srv": {"ericbroda": {"http://localhost:20000/api/search/query": {"200": 1}}, "osc-dm-search-srv": {"http://osc-dm-proxy-srv:8000/api/search/health": {"200": 5}, "http://osc-dm-proxy-srv:8000/api/search/metrics": {"200": 4}}}, "http://osc-dm-product-srv-0:8000": {"ericbroda": {"http://localhost:20000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a": {"200": 1}, "http://localhost:20000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/artifacts": {"200": 1}, "http://localhost:20000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/artifacts/2df6d005-8fb3-444c-b347-7bfc7ca541df": {"200": 1}}, "osc-dm-search-srv": {"http://osc-dm-proxy-srv:8000/api/dataproducts/uuid/b6e05972-fe25-44aa-b5a0-db6e100ca95a/health": {"200": 1}}}}
~~~~

## Utilities

Dump the registrar information:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT utility \
    --dump

[{"key": "/carts/399e1fec-0b66-4570-a84c-8f41ba8e53c4", "value": {"uuid": "399e1fec-0b66-4570-a84c-8f41ba8e53c4", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2024-05-19 13:58:09.241", "updatetimestamp": "2024-05-19 13:58:09.241"}}, {"key": "/orders/31705e97-d955-43f8-80ac-fe87e618b9d3", "value": {"uuid": "31705e97-d955-43f8-80ac-fe87e618b9d3", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "19e317b5-7069-4d5a-848f-3a95dd912ba1", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "b6e05972-fe25-44aa-b5a0-db6e100ca95a", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-05-19 13:57:52.702", "updatetimestamp": "2024-05-19 13:57:52.702"}, "artifact": {"uuid": "2df6d005-8fb3-444c-b347-7bfc7ca541df", "productuuid": "b6e05972-fe25-44aa-b5a0-db6e100ca95a", "productnamespace": "brodagroupsoftware.com", "productname": "rmi.dataproduct", "name": "Assets Earnings Investments", "description": "Detailed breakdown of utility assets in electric rate base, earnings\non these assets, and annual investments (capital additions) by technology.\n", "tags": ["utilities", "emissions"], "license": "CDLA 2.0, Permissive, Version 2.0", "securitypolicy": "public", "links": [{"relationship": "artifact", "mimetype": "text/csv", "url": "https://utilitytransitionhub.rmi.org/static/data_download/assets_earnings_investments.csv"}, {"relationship": "sample", "mimetype": "text/csv", "url": "placeholder-sample.csv"}, {"relationship": "metadata", "mimetype": "application/json", "url": "placeholder-metadata.json"}], "createtimestamp": "2024-05-19 13:57:22.450", "updatetimestamp": "2024-05-19 13:57:22.450"}}], "createtimestamp": "2024-05-19 13:58:09.237", "updatetimestamp": "2024-05-19 13:58:09.237"}, "createtimestamp": "2024-05-19 13:58:09.238", "updatetimestamp": "2024-05-19 13:58:09.238"}}, {"key": "/products/b6e05972-fe25-44aa-b5a0-db6e100ca95a", "value": {"uuid": "b6e05972-fe25-44aa-b5a0-db6e100ca95a", "namespace": "brodagroupsoftware.com", "name": "rmi.dataproduct", "publisher": "publisher.user@brodagroupsoftware.com", "description": "US Utility data provided by RMI", "tags": ["utilities", "emissions"], "address": "http://osc-dm-product-srv-0:8000", "createtimestamp": "2024-05-19 14:00:52.027", "updatetimestamp": "2024-05-19 14:00:52.027"}}, {"key": "/users/guest/8e79c805-c206-42ee-91e0-30923f8b2987", "value": {"uuid": "8e79c805-c206-42ee-91e0-30923f8b2987", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-05-19 13:57:38.470", "updatetimestamp": "2024-05-19 13:57:38.470", "role": "guest"}}, {"key": "/users/publisher/a2734f5f-b9d1-40a1-96db-6194dc7b10d5", "value": {"uuid": "a2734f5f-b9d1-40a1-96db-6194dc7b10d5", "contact": {"name": "Publisher User", "email": "publisher.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-05-19 13:57:38.578", "updatetimestamp": "2024-05-19 13:57:38.578", "role": "publisher"}}, {"key": "/users/subscriber/279e2d55-0ac5-48ac-a4e3-c8dec3f55419", "value": {"uuid": "279e2d55-0ac5-48ac-a4e3-c8dec3f55419", "contact": {"name": "Subscriber User", "email": "subscriber.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-05-19 13:57:38.519", "updatetimestamp": "2024-05-19 13:57:38.519", "role": "subscriber"}}]
~~~~

## Running Test Cases

There are several test cases that can be run but they
rely on other services to be available and hence must be
run in a particular order with some manual intervention.

### Preparation: Start Ecosystem Platform

Start the Ecosystem Platform services (see previous
section "Start Ecosystem Platform").

Start the service for your data product (see previous
section "Start Data Products").

### Step 1: Run User Registration Test Cases

To test user registration capabilities:
~~~~
pytest ./integration-tests/test_cli_users.py
~~~~

### Step 2: Run Auth Test Cases

To test user authorization (login/out) capabilities:
~~~~
pytest ./integration-tests/test_cli_auth.py
~~~~

### Step 3: Generate Product Configurations

To test product configuration generation capabilities:
~~~~
pytest ./integration-tests/test_cli_products_generate.py
~~~~

### Step 4: Assign Product UUIDs

To test product UUID assignment capabilities (note
that you will need to remove the current data product
"uuids.yaml" file or you will receive an error - if this
file already exists then you can safely ignore this test):
~~~~
pytest ./integration-tests/test_cli_products_assign.py
~~~~

### Step 5: Run Product Test Cases

To test product registration capabilities:
~~~~
pytest ./integration-tests/test_cli_products.py
~~~~

### Step 6: Run Product Discovery Test Cases

To test data product capabilities:
~~~~
pytest ./integration-tests/test_cli_discover.py
~~~~

### Step 7: Run Cart and Order Test Cases

To test carts and order management capabilities:
~~~~
pytest ./integration-tests/test_cli_carts_orders.py
~~~~

### Step 8: Run Monitor (Health/Metrics) Test Cases

To test carts and order management capabilities:
~~~~
pytest ./integration-tests/test_cli_monitor.py
~~~~



