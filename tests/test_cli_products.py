# Copyright 2024 Broda Group Software Inc.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
# Created:  2024-04-15 by eric.broda@brodagroupsoftware.com
import pytest
import os
import json

from cli import main
import state

# Global state variables
STATE_PRODUCT_UUID="product-uuid"
STATE_PRODUCT_NAMESPACE="product-namespace"
STATE_PRODUCT_NAME="product-name"

# Common for all CLI commands
HOST="localhost"
PORT="20000"
SAMPLES_DIR = os.environ.get("SAMPLES_DIR")
DATAPRODUCT_DIR=os.path.join(SAMPLES_DIR, "dataproducts", "rmi")
DATAPRODUCT_ADDRESS="http://bgssrv-dmproduct-0:8000"


#####
# PRODUCTS
#####


# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --retrieve
def test_cli_products_retrieve():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--retrieve"
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    product = result[0]
    assert "uuid" in result[0]
    product_uuid = product["uuid"]
    state.gstate(STATE_PRODUCT_UUID, product_uuid)
    product_namespace = product["namespace"]
    state.gstate(STATE_PRODUCT_NAMESPACE, product_namespace)
    product_name = product["name"]
    state.gstate(STATE_PRODUCT_NAME, product_name)


# UUID1="9b45de19-d688-4fd1-b5d3-872598a0293e"
# UUID2="9b45de19-d688-4fd1-b5d3-872598a0293e"
# UUIDS="$UUID1 $UUID2"
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --retrieve \
#     --uuids "$UUIDS"
def test_cli_products_retrieve_uuids():
    UUID1 = state.gstate(STATE_PRODUCT_UUID)
    UUID2 = state.gstate(STATE_PRODUCT_UUID)
    UUIDS = UUID1 + " " + UUID2
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--retrieve",
        "--uuids", UUIDS
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    product = result[0]
    assert "uuid" in result[0]


# UUID="9b45de19-d688-4fd1-b5d3-872598a0293e"
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --retrieve \
#     --uuid "$UUID"
def test_cli_products_retrieve_uuid():
    UUID = state.gstate(STATE_PRODUCT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--retrieve",
        "--uuid", UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    product_uuid = result["uuid"]
    assert UUID == product_uuid


# NAMESPACE="brodagroupsoftware.com" ;
# NAME="rmi.dataproduct" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --retrieve \
#     --namespace "$NAMESPACE" \
#     --name "$NAME"
def test_cli_products_retrieve_namespace_name():
    NAMESPACE = state.gstate(STATE_PRODUCT_NAMESPACE)
    NAME = state.gstate(STATE_PRODUCT_NAME)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--retrieve",
        "--namespace", NAMESPACE,
        "--name", NAME
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    product_namespace = result["namespace"]
    product_name = result["name"]
    assert NAMESPACE == product_namespace
    assert NAME == product_name


# NAMESPACE="brodagroupsoftware.com" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --retrieve \
#     --namespace "$NAMESPACE"
def test_cli_products_retrieve_namespace():
    NAMESPACE = state.gstate(STATE_PRODUCT_NAMESPACE)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--retrieve",
        "--namespace", NAMESPACE
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    product = result[0]
    assert "uuid" in product
    product_namespace = product["namespace"]
    assert NAMESPACE == product_namespace


# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --search \
#     --query "find all temperature products"
def test_cli_products_search():
    QUERY = "find all temperature products"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--search",
        "--query", QUERY
    ])
    assert(result is not None)
    result = json.loads(result)


