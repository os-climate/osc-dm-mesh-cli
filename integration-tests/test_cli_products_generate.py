import json

from cli import main
import state

# Common for all CLI commands
HOST="localhost"
PORT="20000"

# NAMESPACE="brodagroupsoftware.com" ;
# NAME="rmi.dataproduct" ;
# TAGS="utilities,emissions" ;
# DESCRIPTION="Some short description" ;
# DATA_URL="Some data url" ;
# OUTPUT_DIRECTORY="./output" ;
# PRODUCT_YAML="product.yaml" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --generate \
#     --namespace "$NAMESPACE" \
#     --name "$NAME" \
#     --tags "$TAGS" \
#     --data "$DATA_URL" \
#     --description "$DESCRIPTION" \
#     --directory "$OUTPUT_DIRECTORY" \
#     --filename "$PRODUCT_YAML"
def test_generate_product_manual():
    TAGS = "tag1,tag2,tag3"
    NAMESPACE = "test-space"
    NAME = "test-name"
    DIRECTORY = "./output"
    FILENAME = "test_product.yaml"
    DESCRIPTION = "A short description"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--generate",
        "--namespace", NAMESPACE,
        "--name", NAME,
        "--tags", TAGS,
        "--description", DESCRIPTION,
        "--directory", DIRECTORY,
        "--filename", FILENAME
    ])
    assert(result is not None)
    result = json.loads(result)
    assert "product" in result

# NAMESPACE="brodagroupsoftware.com" ;
# NAME="rmi.dataproduct" ;
# TAGS="utilities,emissions" ;
# URL="https://data.catalyst.coop/pudl" ;
# OUTPUT_DIRECTORY="./output" ;
# PRODUCT_YAML="product.yaml" ;
# VENDOR="OpenAI" ;
# MODEL="gpt-3.5-turbo" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --generate \
#     --namespace "$NAMESPACE" \
#     --name "$NAME" \
#     --tags "$TAGS" \
#     --url "$URL" \
#     --vendor "$VENDOR" \
#     --model "$MODEL" \
#     --directory "$OUTPUT_DIRECTORY" \
#     --filename "$PRODUCT_YAML"
def test_generate_product_llm():
    TAGS = "tag1,tag2,tag3"
    NAMESPACE = "test-space"
    NAME = "test-name"
    DIRECTORY = "./output"
    FILENAME = "test_product.yaml"
    URL = "https://data.catalyst.coop/pudl"
    VENDOR = "OpenAI"
    MODEL = "gpt-3.5-turbo"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--generate",
        "--namespace", NAMESPACE,
        "--name", NAME,
        "--tags", TAGS,
        "--url", URL,
        "--vendor", VENDOR,
        "--model", MODEL,
        "--directory", DIRECTORY,
        "--filename", FILENAME
    ])
    assert(result is not None)
    result = json.loads(result)
    assert "product" in result


# NAME="artifact-001" ;
# TAGS="utilities,emissions" ;
# DESCRIPTION="Some short description" ;
# DATA_URL="https://data.catalyst.coop/pudl/core_eia__entity_plants.csv?_size=max" ;
# OUTPUT_DIRECTORY="./output" ;
# ARTIFACT_YAML="$NAME.yaml" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --generate \
#     --name "$NAME" \
#     --tags "$TAGS" \
#     --data "$DATA_URL" \
#     --description "$DESCRIPTION" \
#     --directory "$OUTPUT_DIRECTORY" \
#     --filename "$ARTIFACT_YAML"
def test_generate_product_artifact_manual():
    TAGS = "tag1,tag2,tag3"
    NAME = "test-name"
    URL = "https://data.catalyst.coop/pudl/core_eia__entity_plants"
    DATA_URL = URL + ".csv?_size=max"
    DESCRIPTION = "Some short description"
    DIRECTORY = "./output"
    FILENAME = NAME + ".yaml"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--generate",
        "--name", NAME,
        "--tags", TAGS,
        "--data", DATA_URL,
        "--description", DESCRIPTION,
        "--directory", DIRECTORY,
        "--filename", FILENAME
    ])
    assert(result is not None)
    result = json.loads(result)
    assert "artifact" in result

# NAME="artifact-001" ;
# TAGS="utilities,emissions" ;
# URL="https://data.catalyst.coop/pudl/core_eia__entity_plants" ;
# DATA_URL="$URL.csv?_size=max" ;
# OUTPUT_DIRECTORY="./output" ;
# ARTIFACT_YAML="$NAME.yaml" ;
# VENDOR="OpenAI" ;
# MODEL="gpt-3.5-turbo" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --generate \
#     --name "$NAME" \
#     --tags "$TAGS" \
#     --data "$DATA_URL" \
#     --url "$URL" \
#     --vendor "$VENDOR" \
#     --model "$MODEL" \
#     --directory "$OUTPUT_DIRECTORY" \
#     --filename "$ARTIFACT_YAML"
def test_generate_product_artifact_ai():
    TAGS = "tag1,tag2,tag3"
    NAME = "test-name"
    URL = "https://data.catalyst.coop/pudl/core_eia__entity_plants"
    DATA_URL = URL + ".csv?_size=max"
    DIRECTORY = "./output"
    FILENAME = NAME + ".yaml"
    VENDOR = "OpenAI"
    MODEL = "gpt-3.5-turbo"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--generate",
        "--name", NAME,
        "--tags", TAGS,
        "--data", DATA_URL,
        "--url", URL,
        "--vendor", VENDOR,
        "--model", MODEL,
        "--directory", DIRECTORY,
        "--filename", FILENAME
    ])
    assert(result is not None)
    result = json.loads(result)
    assert "artifact" in result


