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

# Common for all CLI commands
HOST="localhost"
PORT="20000"
SAMPLES_DIR = os.environ.get("SAMPLES_DIR")
DATAPRODUCT_DIR=os.path.join(SAMPLES_DIR, "dataproducts", "rmi")


#####
# PRODUCTS
#####


# DATAPRODUCT_DIR="$SAMPLES_DIR/dataproducts/rmi";
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT products \
#     --generate \
#     --directory "$DATAPRODUCT_DIR"
def test_cli_products_generate():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "products",
        "--generate",
        "--directory", DATAPRODUCT_DIR
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuids" in result)
    assert("product_uuid" in result)
    assert("artifact_uuids" in result)
