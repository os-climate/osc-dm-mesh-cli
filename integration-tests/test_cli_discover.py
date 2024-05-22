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
STATE_PRODUCT_NAME="product-name"
STATE_ARTIFACT_UUID="artifact-uuid"

# Common for all CLI commands
HOST="localhost"
PORT="20000"

def test_preparation():
    # Create and save (global state) product UUIDs
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--retrieve"
    ])
    assert(result is not None)
    result = json.loads(result)
    products = result
    assert len(products) >= 1
    product = products[0]
    assert "uuid" in product
    product_uuid = product["uuid"]
    state.gstate(STATE_PRODUCT_UUID, product_uuid)


# UUID="9b45de19-d688-4fd1-b5d3-872598a0293e"
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --discover \
#     --uuid "$UUID"
def test_cli_products_discover():
    UUID = state.gstate(STATE_PRODUCT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--discover",
        "--uuid", UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    assert "product" in result
    product = result["product"]
    assert "uuid" in product
    product_uuid = product["uuid"]
    assert product_uuid == UUID

    assert "artifacts" in result
    artifacts = result["artifacts"]
    assert len(artifacts) >= 1
    artifact = artifacts[0]
    assert "uuid" in artifact
    artifact_uuid = artifact["uuid"]
    state.gstate(STATE_ARTIFACT_UUID, artifact_uuid)


# PRODUCT_UUID="9b45de19-d688-4fd1-b5d3-872598a0293e"
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
#     --discover \
#     --productuuid "$PRODUCT_UUID"
def test_cli_artifacts_discover():
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "artifacts",
        "--discover",
        "--productuuid", PRODUCT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    artifacts = result
    assert len(artifacts) >= 1
    artifact = artifacts[0]
    assert "uuid" in artifact
    artifact_uuid = artifact["uuid"]
    expected_uuid = state.gstate(STATE_ARTIFACT_UUID)
    assert artifact_uuid == expected_uuid


# PRODUCT_UUID="9b45de19-d688-4fd1-b5d3-872598a0293e"
# ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708"
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT artifacts \
#     --discover \
#     --productuuid "$PRODUCT_UUID" \
#     --uuid "$ARTIFACT_UUID"
def test_cli_artifacts_discover_uuid():
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    ARTIFACT_UUID = state.gstate(STATE_ARTIFACT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "artifacts",
        "--discover",
        "--productuuid", PRODUCT_UUID,
        "--uuid", ARTIFACT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    artifact = result
    assert "uuid" in artifact
    artifact_uuid = artifact["uuid"]
    expected_uuid = state.gstate(STATE_ARTIFACT_UUID)
    assert artifact_uuid == expected_uuid

