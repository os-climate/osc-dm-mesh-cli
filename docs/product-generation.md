## Prerequisites

Python must be available, preferably in a virtual environment (venv).


## Setting up your Environment

Some environment variables are used by various source code and scripts.
Setup your environment as follows (note that "source" is used)
~~~~
source ./bin/environment.sh
~~~~

Additionally, you will need and openAI API key, which needs to be set to the following environment variable, either in
your bash profile, or system variables:

~~~
OPENAI_API_KEY=<your openAI API key>
~~~

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

### Generating a Data Product

Data product files can be generated in a manual fashion
where you provide a description, or using AI-enablement
that creates a description for you based upon a provided
URL site's content.

#### Generating a Data Product (Manual approach)

Data product yaml files can be generated as follows.  In
this case we will provide a description:
~~~~
NAMESPACE="dummyvalue.com" ;
NAME="rmi.dataproduct" ;
TAGS="population,buildings" ;
DESCRIPTION="Some short description" ;
DATA_URL="Some data url" ;
OUTPUT_DIRECTORY="./output" ;
PRODUCT_YAML="product_1.yaml" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --generate \
    --namespace "$NAMESPACE" \
    --name "$NAME" \
    --tags "$TAGS" \
    --data "$DATA_URL" \
    --description "$DESCRIPTION" \
    --directory "$OUTPUT_DIRECTORY" \
    --filename "$PRODUCT_YAML"

{"product": "./output/product_1.yaml"}
~~~~

The contents of your "product_1.yaml" file will look something like this:
~~~~
product:
  description: Some short description
  endpoints:
    administration: http://localhost:9999/administration
    discovery: http://localhost:9999/discovery
    observability: http://localhost:9999/observability
  name: rmi.dataproduct
  namespace: brodagroupsoftware.com
  publisher: publisher.user@brodagroupsoftware.com
  tags:
  - utilities
  - emissions
~~~~

#### Generating a Data Product (AI-enabled approach)

Now, lets have an AI generate a comprehensive and
details description based upon a URL we provide.  A few things
to note: the "DESCRIPTION" variable is replace with a URL parameter,
and a LLM vendor and model.  Since we are generating a description based upon the provided
URL (the site is 'scraped'), it may take about a minute to complete:
~~~~
NAMESPACE="dummyvalue.com" ;
NAME="rmi.dataproduct" ;
TAGS="utilities,emissions" ;
URL="https://data.catalyst.coop/pudl" ;
OUTPUT_DIRECTORY="./output" ;
PRODUCT_YAML="product_2.yaml" ;
VENDOR="OpenAI" ;
MODEL="gpt-4o" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --generate \
    --namespace "$NAMESPACE" \
    --name "$NAME" \
    --tags "$TAGS" \
    --url "$URL" \
    --vendor "$VENDOR" \
    --model "$MODEL" \
    --directory "$OUTPUT_DIRECTORY" \
    --filename "$PRODUCT_YAML"

{"product": "./output/product_2.yaml"}
~~~~



#### Generating a Data Product Artifact (Manual approach)

Data product artifact yaml files can be generated as follows.  In
this case we will provide a description:
~~~~
NAME="artifact-001" ;
TAGS="utilities,emissions" ;
DESCRIPTION="Some short description" ;
DATA_URL="https://data.catalyst.coop/pudl/core_eia__entity_plants.csv?_size=max" ;
OUTPUT_DIRECTORY="./output" ;
ARTIFACT_YAML="$NAME.yaml" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --generate \
    --name "$NAME" \
    --tags "$TAGS" \
    --data "$DATA_URL" \
    --description "$DESCRIPTION" \
    --directory "$OUTPUT_DIRECTORY" \
    --filename "$ARTIFACT_YAML"

{"artifact": "./output/artifacts/artifact-001.yaml"}
~~~~

#### Generating a Data Product Artifact (AI-enabled approach)

Now, lets have an AI generate a comprehensive and
details description based upon a URL we provide.  A few things
to note: the "DESCRIPTION" variable is replace with a URL parameter,
and a LLM vendor and model.  Since we are generating a description based upon the provided
URL (the site is 'scraped'), it may take about a minute to complete:
~~~~
NAME="artifact-002" ;
TAGS="utilities,emissions" ;
URL="https://data.catalyst.coop/pudl/core_eia__entity_plants" ;
DATA_URL="$URL.csv?_size=max" ;
OUTPUT_DIRECTORY="./output" ;
ARTIFACT_YAML="$NAME.yaml" ;
VENDOR="OpenAI" ;
MODEL="gpt-4o" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
    --generate \
    --name "$NAME" \
    --tags "$TAGS" \
    --data "$DATA_URL" \
    --url "$URL" \
    --vendor "$VENDOR" \
    --model "$MODEL" \
    --directory "$OUTPUT_DIRECTORY" \
    --filename "$ARTIFACT_YAML"

{"artifact": "./output/artifacts/artifact-002.yaml"}
~~~~

The contents of your "artifact-001.yaml" file will look something like this:
~~~~
artifact:
  description: The dataset "core_eia__entity_plants" contains static plant attributes
    compiled from EIA-860 and EIA-923 data. It includes information such as plant
    ID, plant name, city, county, latitude, longitude, state, street address, zip
    code, and timezone for 16,847 rows of plant data. The data is licensed under CC-BY-4.0.
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
  - utilities
  - emissions
~~~~

## Running Test Cases
in order to run the test cases, ensure that you have your "OPENAI_API_KEY" environment variable set.

To test product configuration generation capabilities:
~~~~
pytest ./integration-tests/test_cli_products_generate.py
~~~~
