# Background information

## data products
Each data product has several attributes:
- domain: the data product domain; domains are unique across all
data products
- name: The data product name; names must be unique in a domain
- description: 1-2 sentence description of the data product
- tags: Used for searching
- publisher: The data product publisher, or data product owner

## data artifacts
Each artifact has several attributes:
- name: Unique name within the set of artifacts
- description: 1-2 sentence description
- tags: Used to augment searching
- license: Defines how artifact can be used or shared
- securitypolicy: Access policy for the artifact
- data: URLs to the artifact

# Step 1 installation and setup
Setup the CLI

Have the $HOME_DIR environment variable set to the path where the directories used in this guide are stored

~~~
HOME_DIR=<path to directory>
~~~

install the following repo: 
~~~
git@github.com:os-climate/osc-dm-mesh-cli.git
~~~

run the following commands:

~~~

source bin/environment.sh
source bin/venv.sh
source bin/vactivate.sh
pip install -r requirements.txt
~~~

# Step 2 - creating the data product


In whatever location you want, create a directory that will hold the data product. the DATA_DIR value is the directory 
where the data product files will be kept. This can be located anywhere on the local system

~~~
DATA_DIR=<path to data directory>
mkdir $DATA_DIR/dataproducts
mkdir $DATA_DIR/dataproducts/arfima
~~~

from the CLI terminal window, set up your environment as follows:
~~~~
HOST=localhost ;
PORT=20000 ;
VERBOSE="--verbose"
~~~~

create a product by manually specifying parameters

parameters are as follows:

| Parameter        | Description                                                                    |
|------------------|--------------------------------------------------------------------------------|
| NAMESPACE        | Identifier for your groups of products, typically your company name            | 
| NAME             | Name of the data product being created                                         | 
| TAGS             | comma separated list of tags, no spaces, from the 'config/hierarchy.yaml' file | 
| DESCRIPTION      | Text Description of the data product                                           | 
| OUTPUT_DIRECTORY | directory where output files will be placed                                    | 
| PRODUCT_YAML     | name of the product yaml file that will be created                             | 


~~~
NAMESPACE="arfima.com" ;
NAME="arfima.floods" ;
TAGS="population,buildings" ;
DESCRIPTION="Some short description" ;
OUTPUT_DIRECTORY="$DATA_DIR/dataproducts/arfima" ;
PRODUCT_YAML="product.yaml" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --generate \
    --namespace "$NAMESPACE" \
    --name "$NAME" \
    --tags "$TAGS" \
    --description "$DESCRIPTION" \
    --directory "$OUTPUT_DIRECTORY" \
    --filename "$PRODUCT_YAML"
~~~

you should have an output file with the following contents in your data directory:
~~~
product:
  description: Some short description
  endpoints:
    administration: http://localhost:9999/administration
    discovery: http://localhost:9999/discovery
    observability: http://localhost:9999/observability
  name: arfima.floods
  namespace: arfima.com
  publisher: publisher.user@brodagroupsoftware.com
  tags:
  - population
  - buildings
~~~


create artifact by manually specifying parameters

parameters are as follows:

| Parameter        | Description                                                                    |
|------------------|--------------------------------------------------------------------------------|
| ARTIFACT_TYPE    | current options are: "data" and "service"                                      | 
| NAME             | Name of the data product being created                                         | 
| TAGS             | comma separated list of tags, no spaces, from the 'config/hierarchy.yaml' file | 
| DATA_URL         | a valid URL pointing to the actual artifact                                    | 
| DESCRIPTION      | Text Description of the data product                                           | 
| OUTPUT_DIRECTORY | directory where output files will be placed                                    | 
| ARTIFACT_YAML    | name of the artifact yaml file that will be created                            | 

~~~
ARTIFACT_TYPE="data" ;
NAME="artifact-001" ;
TAGS="population,buildings" ;
DESCRIPTION="Some short description" ;
DATA_URL="https://data.catalyst.coop/pudl/core_eia__entity_plants.csv?_size=max" ;
OUTPUT_DIRECTORY="$DATA_DIR/dataproducts/arfima" ;
ARTIFACT_YAML="$NAME.yaml" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --generate \
    --name "$NAME" \
    --tags "$TAGS" \
    --data "$DATA_URL" \
    --description "$DESCRIPTION" \
    --directory "$OUTPUT_DIRECTORY" \
    --filename "$ARTIFACT_YAML"
~~~

you should have an artifact.yaml file in your data directory with the following content:
~~~
artifact:
  description: Some short description
  license: CDLA 2.0, Permissive, Version 2.0
  links:
  - mimetype: text/csv
    relationship: artifact
    url: https://data.catalyst.coop/pudl/core_eia__entity_plants.csv?_size=max
  - mimetype: text/csv
    relationship: sample
    url: placeholder-sample.csv
  - mimetype: application/json
    relationship: metadata
    url: placeholder-metadata.json
  name: artifact-001
  securitypolicy: public
  tags:
  - population
  - buildings
~~~

# STEP 3 - setting up the data mesh server


You will need have a separate cmd line window for the data mesh server, and will require docker to 
be installed and running. This will download several docker images, and may take several minutes.

clone the following repo:

~~~
https://github.com/os-climate/osc-dm-mesh-srv
~~~

Have the $HOME_DIR environment variable set to the path where the directories used in this guide are stored

~~~
HOME_DIR=<path to directory>
~~~

run the following commands from the repository directory

~~~
source bin/environment.sh
app/startd.sh
~~~

from the osc-dm-mesh-cli terminal run the following command to generate the UUIDs for the product:
~~~
DATAPRODUCT_DIR="$DATA_DIR/dataproducts/arfima";
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --assign \
    --directory "$DATAPRODUCT_DIR"
~~~


you should have an output uuids.yaml file in your data directory with contents similar to the following:

~~~
product_uuid: f8566485-f376-43bb-b381-8885bea9ff92  
artifact_uuids: 
- artifact-001: 6ac3dd44-8831-40ce-856c-3ffb5253c66f
~~~

from the CLI terminal, generate the users with the following command
this is only needed if you want to view your product from the CLI.
~~~
ROLE="subscriber" ;
GUEST_EMAIL="subscriber.user@brodagroupsoftware.com" ;
NAME="Subscriber User" ;
PHONE="+1 647.555.1212" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --register \
    --role "$ROLE" \
    --name "$NAME" \
    --email "$GUEST_EMAIL" \
    --phone "$PHONE"
~~~

additionally, you will have to create a publisher user.
~~~
ROLE="publisher" ;
GUEST_EMAIL="publisher.user@brodagroupsoftware.com" ;
NAME="Publisher User" ;
PHONE="+1 647.555.1212" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --register \
    --role "$ROLE" \
    --name "$NAME" \
    --email "$GUEST_EMAIL" \
    --phone "$PHONE"
~~~

# STEP 4 - setting up the data product server

You will need have a separate cmd line window for the data product server

run the data product server

clone the following repo

~~~
https://github.com/os-climate/osc-dm-product-srv
~~~

Have the $HOME_DIR environment variable set to the path where the directories used in this guide are stored

~~~
HOME_DIR=<path to directory>
~~~

move into the osc-dm-product-srv project folder.

in bin/environment.sh, change the following line:
~~~
export DATA_DIR="$ROOT_DIR/osc-dm-samples-dat"
~~~

to

~~~
export DATA_DIR=<path to data directory>
~~~


copy the following file into config/arfima
~~~
mkdir config/arfima
cp config/rmi/config.yaml config/arfima/config.yaml
~~~

run the product server
~~~
source bin/environment.sh
app/startd.sh 0 arfima
~~~


## Viewing the data product

you should be able to see the new data product registered when you got to localhost:3000 on your browser

if prompted for login, use the following credentials
email/username: subscriber.user@brodagroupsoftware.com
password: any password
role: Subscriber