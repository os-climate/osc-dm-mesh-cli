# CLI Reference

Most of the following capabilities are probably suitable
for administrators, and maybe developers to support debugging.

This is provided for reference only (ie. previous commands
should be the ones used on a daily/frequent basis).

## Load Samples

Load sample data products (at Registry):
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT configuration \
    --samples

~~~~

## View OpenAPI Specification

Check out the OpenAPI specification:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT configuration \
    --openapi
~~~~

## Working with Users/Subscribers/Publishers/Administrators/Entities

The Registry supports three types of users:
- Users: Have access to public components of the
Registry; Can view Marketplace but have no carts and cannot
create orders; Do not have a dashboard.
- Subscribers: Can consume products and artifacts in the Registry;
Can view Marketplace and have a cart, and can create
orders; Have a dashboard.
- Publishers: Can publish products and artifacts to the Registry;
Can view Marketplace and no not have a cart, and cannot create
orders; Have a dashboard.
- Adminstrators: Can administer site; they have their own dashboard,
and can execute administrative functions; have no shopping cart and
cannot create orders
- Entities: Represent any type of user; have login/logout events

Users, subscribers, and publishers have a lifecycle:
- A user need to be created (registered and on-boarded); Administrators
can do this
- Once created, a user can login/logout
- At some point a user is retired (unregistered and off-boarded); Administrators
can do this

There is a role mapping for users via an entity.  The
entity maps a user's email (id) to their role.  In other
words, to determine if an id (email) is a user, subscriber,
or publisher, you will need to interogate the entity.

### Creating/Updating/Retrieving Users

Our registry requires users to be created, or registered.
Throughout these examples our user will be "general.user@brodagroupsoftware.com".
So, let's create our user...

To create/register a user, execute the following command (typical response
shown after the command):
~~~~
EMAIL="general.user@brodagroupsoftware.com" ;
NAME="General User" ;
PHONE="+1 647.555.1212" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT users \
    --create \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "a405b700-3b31-4074-ba45-524c5bbd498f", "contact": {"name": "General User", "email": "general.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2023-12-13 09:22:50.653", "updatetimestamp": "2023-12-13 09:22:50.653"}
~~~~

Update an existing user:
~~~~
UUID="a405b700-3b31-4074-ba45-524c5bbd498f"
EMAIL="general.user@brodagroupsoftware.com" ;
NAME="General User" ;
PHONE="+1 647.555.1213" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT users \
    --update \
    --uuid "$UUID" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "a405b700-3b31-4074-ba45-524c5bbd498f", "contact": {"name": "General User", "email": "general.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:22:50.653", "updatetimestamp": "2023-12-13 09:23:54.084"}
~~~~

Retrieving user by UUID:
~~~~
UUID="a405b700-3b31-4074-ba45-524c5bbd498f"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --uuid "$UUID"

{"uuid": "a405b700-3b31-4074-ba45-524c5bbd498f", "contact": {"name": "General User", "email": "general.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:22:50.653", "updatetimestamp": "2023-12-13 09:23:54.084"}
~~~~

Retrieving user by email:
~~~~
EMAIL="general.user@brodagroupsoftware.com" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve \
    --email "$EMAIL"

{"uuid": "a405b700-3b31-4074-ba45-524c5bbd498f", "contact": {"name": "General User", "email": "general.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:22:50.653", "updatetimestamp": "2023-12-13 09:23:54.084"}
~~~~

Retrieving all users:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT users \
    --retrieve

[{"uuid": "a405b700-3b31-4074-ba45-524c5bbd498f", "contact": {"name": "General User", "email": "general.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:22:50.653", "updatetimestamp": "2023-12-13 09:23:54.084"}]
~~~~

### Creating/Updating/Retrieving Publishers

Our registry requires publishers to be created, or registered.
Throughout these examples our user will be "general.user@brodagroupsoftware.com".
So, let's create our user...

To create/register a user, execute the following command (typical response
shown after the command):
~~~~
EMAIL="publisher.user@brodagroupsoftware.com" ;
NAME="Publisher User" ;
PHONE="+1 647.555.1212" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT publishers \
    --create \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "df4c16f7-2977-4a5f-ab8e-117fee4ee70d", "contact": {"name": "Publisher User", "email": "publisher.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2023-12-13 09:24:48.874", "updatetimestamp": "2023-12-13 09:24:48.874"}
~~~~

Update an existing publishers:
~~~~
UUID="df4c16f7-2977-4a5f-ab8e-117fee4ee70d"
EMAIL="publisher.user@brodagroupsoftware.com" ;
NAME="Publisher User" ;
PHONE="+1 647.555.1213" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT publishers \
    --update \
    --uuid "$UUID" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "df4c16f7-2977-4a5f-ab8e-117fee4ee70d", "contact": {"name": "Publisher User", "email": "publisher.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:24:48.874", "updatetimestamp": "2023-12-13 09:25:07.881"}
~~~~

Retrieving publisher by UUID:
~~~~
UUID="df4c16f7-2977-4a5f-ab8e-117fee4ee70d"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT publishers \
    --retrieve \
    --uuid "$UUID"

{"uuid": "df4c16f7-2977-4a5f-ab8e-117fee4ee70d", "contact": {"name": "Publisher User", "email": "publisher.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:24:48.874", "updatetimestamp": "2023-12-13 09:25:07.881"}
~~~~

Retrieving publisher by email:
~~~~
EMAIL="publisher.user@brodagroupsoftware.com" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT publishers \
    --retrieve \
    --email "$EMAIL"

{"uuid": "df4c16f7-2977-4a5f-ab8e-117fee4ee70d", "contact": {"name": "Publisher User", "email": "publisher.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:24:48.874", "updatetimestamp": "2023-12-13 09:25:07.881"}
~~~~

Retrieving all publishers:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT publishers \
    --retrieve

[{"uuid": "df4c16f7-2977-4a5f-ab8e-117fee4ee70d", "contact": {"name": "Publisher User", "email": "publisher.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:24:48.874", "updatetimestamp": "2023-12-13 09:25:07.881"}]
~~~~

### Creating/Updating/Retrieving Subscribers

Our registry requires subscriber to be created, or registered.
Throughout these examples our user will be "general.user@brodagroupsoftware.com".
So, let's create our user...

To create/register a subscriber, execute the following command (typical response
shown after the command):
~~~~
EMAIL="subscriber.user@brodagroupsoftware.com" ;
NAME="Subscriber User" ;
PHONE="+1 647.555.1212" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscribers \
    --create \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "4c36600f-383d-42bd-941d-45208a92a77b", "contact": {"name": "Subscriber User", "email": "subscriber.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:12.581"}
~~~~

Update an existing subscribers:
~~~~
UUID="4c36600f-383d-42bd-941d-45208a92a77b"
EMAIL="subscriber.user@brodagroupsoftware.com" ;
NAME="Subscriber User" ;
PHONE="+1 647.555.1213" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscribers \
    --update \
    --uuid "$UUID" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "4c36600f-383d-42bd-941d-45208a92a77b", "contact": {"name": "Subscriber User", "email": "subscriber.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:33.916"}
~~~~

Retrieving subscriber by UUID:
~~~~
UUID="4c36600f-383d-42bd-941d-45208a92a77b"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscribers \
    --retrieve \
    --uuid "$UUID"

{"uuid": "4c36600f-383d-42bd-941d-45208a92a77b", "contact": {"name": "Subscriber User", "email": "subscriber.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:33.916"}
~~~~

Retrieving subscriber by email:
~~~~
EMAIL="subscriber.user@brodagroupsoftware.com" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscribers \
    --retrieve \
    --email "$EMAIL"

{"uuid": "4c36600f-383d-42bd-941d-45208a92a77b", "contact": {"name": "Subscriber User", "email": "subscriber.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:33.916"}
~~~~

Retrieving all subscribers:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscribers \
    --retrieve

[{"uuid": "4c36600f-383d-42bd-941d-45208a92a77b", "contact": {"name": "Subscriber User", "email": "subscriber.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:33.916"}]
~~~~

### Creating/Updating/Retrieving Administrators

Our registry requires administrator to be created, or registered.
Throughout these examples our user will be "general.user@brodagroupsoftware.com".
So, let's create our user...

To create/register a administrators, execute the following command (typical response
shown after the command):
~~~~
EMAIL="administrator.user@brodagroupsoftware.com" ;
NAME="Administrator User" ;
PHONE="+1 647.555.1212" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT administrators \
    --create \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "07c531f0-e676-4787-9e31-6da3db571a96", "contact": {"name": "Administrator User", "email": "administrator.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2023-12-13 09:27:22.910", "updatetimestamp": "2023-12-13 09:27:22.910"}
~~~~

Update an existing administrators:
~~~~
UUID="07c531f0-e676-4787-9e31-6da3db571a96"
EMAIL="administrator.user@brodagroupsoftware.com" ;
NAME="Administrator User" ;
PHONE="+1 647.555.1213" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT administrators \
    --update \
    --uuid "$UUID" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "07c531f0-e676-4787-9e31-6da3db571a96", "contact": {"name": "Administrator User", "email": "administrator.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:27:22.910", "updatetimestamp": "2023-12-13 09:27:42.461"}
~~~~

Retrieving administrator by UUID:
~~~~
UUID="07c531f0-e676-4787-9e31-6da3db571a96"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT administrators \
    --retrieve \
    --uuid "$UUID"

{"uuid": "07c531f0-e676-4787-9e31-6da3db571a96", "contact": {"name": "Administrator User", "email": "administrator.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:27:22.910", "updatetimestamp": "2023-12-13 09:27:42.461"}
~~~~

Retrieving administrator by email:
~~~~
EMAIL="administrator.user@brodagroupsoftware.com" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT administrators \
    --retrieve \
    --email "$EMAIL"

{"uuid": "07c531f0-e676-4787-9e31-6da3db571a96", "contact": {"name": "Administrator User", "email": "administrator.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:27:22.910", "updatetimestamp": "2023-12-13 09:27:42.461"}
~~~~

Retrieving all administrators:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT administrators \
    --retrieve

[{"uuid": "07c531f0-e676-4787-9e31-6da3db571a96", "contact": {"name": "Administrator User", "email": "administrator.user@brodagroupsoftware.com", "phone": "+1 647.555.1213"}, "createtimestamp": "2023-12-13 09:27:22.910", "updatetimestamp": "2023-12-13 09:27:42.461"}]
~~~~

### Creating/Updating/Retrieving Entities

NOTE: Generally entities are not created on their own,
but rather the are created when a user, subscriber,
publisher, or administrator is created (registered).

Much more important are the entity login/logout in the
next section.

Nevertheless, for consistency across the CLI,
these commands are available to support testing...

To create/register a entity, execute the following command (typical response
shown after the command):
~~~~
EMAIL="general.user@brodagroupsoftware.com" ;
ROLE="user" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --create \
    --email "$EMAIL" \
    --role "$ROLE"

{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "user", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:28:35.312"}
~~~~

Update an existing entity (change the user to a "subscriber"...
Note that this is a contrived example and would not occur
in real life):
~~~~
UUID="2782b735-46a5-4351-b8c8-c7d4cdf82620"
EMAIL="general.user@brodagroupsoftware.com" ;
ROLE="subscriber" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --update \
    --uuid "$UUID" \
    --email "$EMAIL" \
    --role "$ROLE"

{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "subscriber", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:31:10.287"}
~~~~

Retrieving entity by UUID:
~~~~
UUID="2782b735-46a5-4351-b8c8-c7d4cdf82620"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --retrieve \
    --uuid "$UUID"

{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "subscriber", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:31:10.287"}
~~~~

Retrieving entity by email:
~~~~
EMAIL="general.user@brodagroupsoftware.com" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --retrieve \
    --email "$EMAIL"

{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "subscriber", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:31:10.287"}
~~~~

Retrieving all entities:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --retrieve

[{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "subscriber", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:31:10.287"}]
~~~~

## Logging IN/OUT Entities

Entities play a very specfic role: Once a user, subscriber,
publisher, or admnistrator is created/registered, then entities
are created to support login/logout activities.

Upon successful login, the caller is returned the entity-role mapping
info which will identify the entity role as either a user, subscriber,
publisher, or administrator.

Let's login an existing entity - this will return the entity role map and
create a login event.
~~~~
EMAIL="general.user@brodagroupsoftware.com" ;
PASSWORD="some-password" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --login \
    --email "$EMAIL"\
    --password "$PASSWORD"

{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "subscriber", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:31:10.287"}
~~~~

Logout an existing entity - this will return the entity role map and
create a logout event.
~~~~
EMAIL="general.user@brodagroupsoftware.com" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT entities \
    --logout \
    --email "$EMAIL"

{"uuid": "2782b735-46a5-4351-b8c8-c7d4cdf82620", "email": "general.user@brodagroupsoftware.com", "role": "subscriber", "createtimestamp": "2023-12-13 09:28:35.312", "updatetimestamp": "2023-12-13 09:31:10.287"}
~~~~

## Creating/Updating/Retrieving a Product

A Product is uniquely identified by a UUID or a NAMESPACE/NAME.

Create a product:
~~~~
NAMESPACE="brodagroupsoftware.com" ;
NAME="sample-climate-product" ;
PUBLISHER="publisher.user@brodagroupsoftware.com" ;
DESCRIPTION="Sample climate data product description" ;
TAGS="climate,precipitation,temperature" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT products \
    --create \
    --namespace "$NAMESPACE" \
    --name "$NAME" \
    --publisher "$PUBLISHER" \
    --description "$DESCRIPTION" \
    --tags "$TAGS"

{"uuid": "569694e0-dcd4-44d9-9d95-d43879236e9f", "namespace": "brodagroupsoftware.com", "name": "sample-climate-product", "publisher": "publisher.user@brodagroupsoftware.com", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature"], "createtimestamp": "2023-12-13 09:32:49.506", "updatetimestamp": "2023-12-13 09:32:49.506"}
~~~~

Update an existing product using the UUID created in the previous step:
~~~~
NAMESPACE="brodagroupsoftware.com" ;
NAME="sample-climate-product" ;
PUBLISHER="publisher.user@brodagroupsoftware.com" ;
DESCRIPTION="Sample climate data product description" ;
TAGS="climate,precipitation,temperature,wind" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT products \
    --update \
    --namespace "$NAMESPACE" \
    --name "$NAME" \
    --publisher "$PUBLISHER" \
    --description "$DESCRIPTION" \
    --tags "$TAGS"

{"uuid": "569694e0-dcd4-44d9-9d95-d43879236e9f", "namespace": "brodagroupsoftware.com", "name": "sample-climate-product", "publisher": "publisher.user@brodagroupsoftware.com", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "createtimestamp": "2023-12-13 09:32:49.506", "updatetimestamp": "2023-12-13 09:33:00.235"}
~~~~

Retrieve a product (use the uuid for the product just created in the previous step):
~~~~
UUID="569694e0-dcd4-44d9-9d95-d43879236e9f";
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve \
    --uuid "$UUID"

{"uuid": "569694e0-dcd4-44d9-9d95-d43879236e9f", "namespace": "brodagroupsoftware.com", "name": "sample-climate-product", "publisher": "publisher.user@brodagroupsoftware.com", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "createtimestamp": "2023-12-13 09:32:49.506", "updatetimestamp": "2023-12-13 09:33:00.235"}
~~~~

Retrieve all products:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT products \
    --retrieve

[{"uuid": "569694e0-dcd4-44d9-9d95-d43879236e9f", "namespace": "brodagroupsoftware.com", "name": "sample-climate-product", "publisher": "publisher.user@brodagroupsoftware.com", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "createtimestamp": "2023-12-13 09:32:49.506", "updatetimestamp": "2023-12-13 09:33:00.235"}]
~~~~

View all products for a given publisher:
~~~~
EMAIL="publisher.user@brodagroupsoftware.com";
python ./src/publisher/cli.py $VERBOSE --host $HOST --port $PORT whoami \
    --EMAIL $EMAIL

{"uuid": null, "contact": {"name": "Eric Broda", "email": "general.user@brodagroupsoftware.com", "phone": "+1 416 555 1212"}, "createtimestamp": null, "updatetimestamp": null}
~~~~

## Creating/Updating/Retrieving a Product Artifact

Create a product artifact:
~~~~
PRODUCT_NAMESPACE="brodagroupsoftware.com" ;
PRODUCT_NAME="sample-climate-product" ;
NAME="sample-climate-product" ;
DESCRIPTION="Sample climate data product description" ;
TAGS="climate,precipitation,temperature" ;
DATAMIMETYPE="text/csv" ;
DATAURL="http://localhost:8080/somedata" ;
LICENSE="public" ;
SECURITY_POLICY="public-policy" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --create \
    --productnamespace $PRODUCT_NAMESPACE \
    --productname $PRODUCT_NAME \
    --name $NAME \
    --description "$DESCRIPTION" \
    --tags $TAGS \
    --datamimetype "$DATAMIMETYPE" \
    --dataurl "$DATAURL" \
    --license "$LICENSE" \
    --securitypolicy "$SECURITY_POLICY"

{"uuid": "206a5f3d-5ac9-44cc-b887-ebd36c4d1d64", "productnamespace": "brodagroupsoftware.com", "productname": "sample-climate-product", "name": "sample-climate-product", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature"], "license": "public", "securitypolicy": "public-policy", "data": {"mimetype": "text/csv", "url": "http://localhost:8080/somedata"}, "createtimestamp": "2023-12-13 09:34:07.896", "updatetimestamp": "2023-12-13 09:34:07.896"}
~~~~

Update a product artifact using the using the product uuid and the artifact uuid
created in the previous step:
~~~~
PRODUCT_NAMESPACE="brodagroupsoftware.com" ;
PRODUCT_NAME="sample-climate-product" ;
NAME="sample-climate-product" ;
DESCRIPTION="Sample climate data product description" ;
TAGS="climate,precipitation,temperature,wind" ;
DATAMIMETYPE="text/csv" ;
DATAURL="http://localhost:8080/somedata" ;
LICENSE="public" ;
SECURITY_POLICY="public-policy" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --update \
    --productnamespace $PRODUCT_NAMESPACE \
    --productname $PRODUCT_NAME \
    --name "$NAME" \
    --description "$DESCRIPTION" \
    --tags "$TAGS" \
    --datamimetype "$DATAMIMETYPE" \
    --dataurl "$DATAURL" \
    --license "$LICENSE" \
    --securitypolicy "$SECURITY_POLICY"

{"uuid": "206a5f3d-5ac9-44cc-b887-ebd36c4d1d64", "productnamespace": "brodagroupsoftware.com", "productname": "sample-climate-product", "name": "sample-climate-product", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "license": "public", "securitypolicy": "public-policy", "data": {"mimetype": "text/csv", "url": "http://localhost:8080/somedata"}, "createtimestamp": "2023-12-13 09:34:07.896", "updatetimestamp": "2023-12-13 09:34:20.409"}
~~~~

Retrieve all artifacts:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --retrieve

[{"uuid": "206a5f3d-5ac9-44cc-b887-ebd36c4d1d64", "productnamespace": "brodagroupsoftware.com", "productname": "sample-climate-product", "name": "sample-climate-product", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "license": "public", "securitypolicy": "public-policy", "data": {"mimetype": "text/csv", "url": "http://localhost:8080/somedata"}, "createtimestamp": "2023-12-13 09:34:07.896", "updatetimestamp": "2023-12-13 09:34:20.409"}]
~~~~

Retrieve a product artifact by name (use the product namespace and product name
used in the previous step):
~~~~
PRODUCT_NAMESPACE="brodagroupsoftware.com" ;
PRODUCT_NAME="sample-climate-product" ;
NAME="sample-climate-product" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
    --retrieve \
    --productnamespace $PRODUCT_NAMESPACE \
    --productname $PRODUCT_NAME \
    --name $NAME

[{"uuid": "206a5f3d-5ac9-44cc-b887-ebd36c4d1d64", "productnamespace": "brodagroupsoftware.com", "productname": "sample-climate-product", "name": "sample-climate-product", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "license": "public", "securitypolicy": "public-policy", "data": {"mimetype": "text/csv", "url": "http://localhost:8080/somedata"}, "createtimestamp": "2023-12-13 09:34:07.896", "updatetimestamp": "2023-12-13 09:34:20.409"}]
~~~~

## Creating/Updating/Retrieving a Cart

Create a cart (should not be work if a subscriber has
been created, which is where a cart is, by default, created...
so, this can only be used as a basic a test case).  If
a subscriber has already been created, then a "Cart already exists"
error will be raised:
~~~~
SUBSCRIBER="subscriber.user@brodagroupsoftware.com";
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --create \
    --subscriber "$SUBSCRIBER"

{"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2023-12-10 12:03:53.850", "updatetimestamp": "2023-12-10 12:03:53.850"}
~~~~

Add item to an owner's cart:
~~~~
SUBSCRIBER="subscriber.user@brodagroupsoftware.com"
ARTIFACT_UUID="206a5f3d-5ac9-44cc-b887-ebd36c4d1d64"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --add \
    --subscriber "$SUBSCRIBER" \
    --item "$ARTIFACT_UUID"

{"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": ["206a5f3d-5ac9-44cc-b887-ebd36c4d1d64"], "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:12.581"}
~~~~

Remove item to an owner's cart:
~~~~
SUBSCRIBER="subscriber.user@brodagroupsoftware.com"
ARTIFACT_UUID="206a5f3d-5ac9-44cc-b887-ebd36c4d1d64"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --remove \
    --subscriber "$SUBSCRIBER" \
    --item "$ARTIFACT_UUID"

{"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [], "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:12.581"}
~~~~

Retrieve a cart by uuid (use the cart uuid from the previously created cart):
~~~~
UUID="e888082d-7720-4876-b94f-42aa2f180d0f"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve \
    --uuid "$UUID"

{"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": ["206a5f3d-5ac9-44cc-b887-ebd36c4d1d64"], "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:12.581"}
~~~~

Retrieve a cart by owner (use the cart owner from the previously created cart):
~~~~
SUBSCRIBER="subscriber.user@brodagroupsoftware.com"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve \
    --subscriber "$SUBSCRIBER"

{"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": ["206a5f3d-5ac9-44cc-b887-ebd36c4d1d64"], "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:12.581"}
~~~~

Retrieve all carts:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT carts \
    --retrieve

[{"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": ["206a5f3d-5ac9-44cc-b887-ebd36c4d1d64"], "createtimestamp": "2023-12-13 09:26:12.581", "updatetimestamp": "2023-12-13 09:26:12.581"}]
~~~~

## Creating/Retrieving an Order

Create an order (note: orders are immutable and cannot be updated):
~~~~
SUBSCRIBER="subscriber.user@brodagroupsoftware.com"
CART_UUID="e888082d-7720-4876-b94f-42aa2f180d0f"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --create \
    --subscriber "$SUBSCRIBER" \
    --cartuuid "$CART_UUID"

{"uuid": "1b6f6e1e-32c8-41ab-b9a9-93f30ebaab4d", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "569694e0-dcd4-44d9-9d95-d43879236e9f", "namespace": "brodagroupsoftware.com", "name": "sample-climate-product", "publisher": "publisher.user@brodagroupsoftware.com", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "createtimestamp": "2023-12-13 09:32:49.506", "updatetimestamp": "2023-12-13 09:33:00.235"}, "artifact": {"uuid": "206a5f3d-5ac9-44cc-b887-ebd36c4d1d64", "productnamespace": "brodagroupsoftware.com", "productname": "sample-climate-product", "name": "sample-climate-product", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "license": "public", "securitypolicy": "public-policy", "data": {"mimetype": "text/csv", "url": "http://localhost:8080/somedata"}, "createtimestamp": "2023-12-13 09:34:07.896", "updatetimestamp": "2023-12-13 09:34:20.409"}}], "createtimestamp": "2023-12-13 09:41:04.464", "updatetimestamp": "2023-12-13 09:41:04.464"}, "createtimestamp": "2023-12-13 09:41:04.466", "updatetimestamp": "2023-12-13 09:41:04.466"}
~~~~

Retrieve an order (use the order uuid from the previously created order):
~~~~
UUID="1b6f6e1e-32c8-41ab-b9a9-93f30ebaab4d"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT orders \
    --retrieve \
    --uuid "$UUID"

{"uuid": "1b6f6e1e-32c8-41ab-b9a9-93f30ebaab4d", "subscriber": "subscriber.user@brodagroupsoftware.com", "cart": {"uuid": "e888082d-7720-4876-b94f-42aa2f180d0f", "subscriber": "subscriber.user@brodagroupsoftware.com", "items": [{"product": {"uuid": "569694e0-dcd4-44d9-9d95-d43879236e9f", "namespace": "brodagroupsoftware.com", "name": "sample-climate-product", "publisher": "publisher.user@brodagroupsoftware.com", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "createtimestamp": "2023-12-13 09:32:49.506", "updatetimestamp": "2023-12-13 09:33:00.235"}, "artifact": {"uuid": "206a5f3d-5ac9-44cc-b887-ebd36c4d1d64", "productnamespace": "brodagroupsoftware.com", "productname": "sample-climate-product", "name": "sample-climate-product", "description": "Sample climate data product description", "tags": ["climate", "precipitation", "temperature", "wind"], "license": "public", "securitypolicy": "public-policy", "data": {"mimetype": "text/csv", "url": "http://localhost:8080/somedata"}, "createtimestamp": "2023-12-13 09:34:07.896", "updatetimestamp": "2023-12-13 09:34:20.409"}}], "createtimestamp": "2023-12-13 09:41:04.464", "updatetimestamp": "2023-12-13 09:41:04.464"}, "createtimestamp": "2023-12-13 09:41:04.464", "updatetimestamp": "2023-12-13 09:41:04.464"}
~~~~

## Creating/Retrieving Events

Create an event:
~~~~
NAME="event-sample" ;
DATA='{"userid": "general.user@brodagroupsoftware.com"}' ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT events \
    --create \
    --name "$NAME" \
    --data "$DATA"

{"uuid": "02598231-0678-4cdb-9658-a3b1df711803", "name": "event-sample", "data": {"userid": "general.user@brodagroupsoftware.com"}, "createtimestamp": "2023-12-13 09:41:44.977"}
~~~~

Retrieving all events of specific name:
~~~~
NAME="event-sample" ;
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT events \
    --retrieve \
    --name $NAME

[{"uuid": "02598231-0678-4cdb-9658-a3b1df711803", "name": "event-sample", "data": {"userid": "general.user@brodagroupsoftware.com"}, "createtimestamp": "2023-12-13 09:41:44.977"}]
~~~~

Retrieving all events:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT events \
    --retrieve

[{"uuid": "421e7852-80ef-4c03-a119-deb2f5c10033", "name": "event-login", "data": {"entityid": "general.user@brodagroupsoftware.com"}, "createtimestamp": "2023-12-13 09:32:11.678"}, {"uuid": "3b00916d-3450-4cff-9bbe-fc1c301819e4", "name": "event-logout", "data": {"entityid": "general.user@brodagroupsoftware.com"}, "createtimestamp": "2023-12-13 09:32:22.002"}, {"uuid": "02598231-0678-4cdb-9658-a3b1df711803", "name": "event-sample", "data": {"userid": "general.user@brodagroupsoftware.com"}, "createtimestamp": "2023-12-13 09:41:44.977"}]
~~~~

## Subscribing to Data Changes

TODO: Needs further testing... Not yet ready for prime time...

Get list of all topics:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscription --host $HOST --port $PORT \
        --topics

[{"products": "Changes to products"}, {"artifacts": "Changes to artifacts"}, {"carts": "Changes to carts"}, {"orders": "Changes to orders"}]
~~~~
A list of topics are shown - we will use the topic "products" in the next
set of examples.

Subscribe to data changes:
~~~~
TOPIC="products"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscription --host $HOST --port $PORT \
        --subscribe \
        --topic "$TOPIC"
~~~~

Get list of all subscribers:
~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscription --host $HOST --port $PORT \
        --subscribers
~~~~

Get list of all subscribers to a topic:
~~~~
TOPIC="products"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscription --host $HOST --port $PORT \
        --subscribers \
        --topic "$TOPIC"
~~~~

Get list of all subscribers for a name:
~~~~
NAME="bdae9112-8368-4d4e-89e4-a512049d03ee"
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT subscription --host $HOST --port $PORT \
        --subscribers \
        --name "$NAME"
~~~~

## Searching for Product Data (Provisional)

TODO: Redesign/fix this...

~~~~
python ./src/administrator/cli.py $VERBOSE --host $HOST --port $PORT products --host $HOST --port $PORT \
        --search \
        --collection "$COLLECTION" \
        --query "$QUERY" \
        --k $K
~~~~

