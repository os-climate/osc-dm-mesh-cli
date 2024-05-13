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
STATE_SUBSCRIBER_UUID="subscriber-uuid"
STATE_PRODUCT_UUID="product-uuid"
STATE_ARTIFACT_UUID="artifact-uuid"
STATE_CART_UUID="cart-uuid"
STATE_ORDER_UUID="order-uuid"

# Common for all CLI commands
HOST="localhost"
PORT="20000"
SUBSCRIBER_EMAIL="subscriber.user@brodagroupsoftware.com"
SUBSCRIBER_ROLE="subscriber"


#####
# PREPARATION
#####


def test_preparation():
    # Create and save (global state) subscriber UUID
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve",
        "--role", SUBSCRIBER_ROLE,
        "--email", SUBSCRIBER_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    subscriber = result
    assert "uuid" in subscriber
    subscriber_uuid = subscriber["uuid"]
    assert "contact" in subscriber
    contact = subscriber["contact"]
    assert "email" in contact
    subscriber_email = contact["email"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    state.gstate(STATE_SUBSCRIBER_UUID, subscriber_uuid)

    # Get and save a product UUID
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

    # Get and save an artifact UUID
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
    state.gstate(STATE_ARTIFACT_UUID, artifact_uuid)


#####
# CARTS
#####


# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --retrieve
def test_cli_carts_retrieve():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--retrieve"
    ])
    assert(result is not None)
    result = json.loads(result)
    carts = result
    assert len(carts) >= 1
    cart = carts[0]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    state.gstate(STATE_CART_UUID, cart_uuid)


# CART_UUID="24be71ef-3cd1-4a15-9599-f82cb64fb4d8" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --retrieve \
#     --uuid "$CART_UUID"
def test_cli_carts_retrieve_uuid():
    UUID = state.gstate(STATE_CART_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--retrieve",
        "--uuid", UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL


# EMAIL="subscriber.user@brodagroupsoftware.com" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --retrieve \
#     --email "$EMAIL"
def test_cli_carts_retrieve_email():
    EMAIL = SUBSCRIBER_EMAIL
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--retrieve",
        "--email", EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL


# PRODUCT_UUID="9b45de19-d688-4fd1-b5d3-872598a0293e" ;
# ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708" ;
# CART_UUID="aa62de43-b5b2-44ac-8d19-90e880a26586" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --add \
#     --uuid "$CART_UUID" \
#     --productuuid "$PRODUCT_UUID" \
#     --artifactuuid "$ARTIFACT_UUID"
def test_cli_carts_add_uuid():
    CART_UUID = state.gstate(STATE_CART_UUID)
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    ARTIFACT_UUID = state.gstate(STATE_ARTIFACT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--add",
        "--uuid", CART_UUID,
        "--productuuid", PRODUCT_UUID,
        "--artifactuuid", ARTIFACT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    assert "items" in cart
    items = cart["items"]
    assert len(items) == 1


# PRODUCT_UUID="9b45de19-d688-4fd1-b5d3-872598a0293e" ;
# ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708" ;
# EMAIL="subscriber.user@brodagroupsoftware.com" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --add \
#     --email "$EMAIL" \
#     --productuuid "$PRODUCT_UUID" \
#     --artifactuuid "$ARTIFACT_UUID"
def test_cli_carts_add_email():
    EMAIL = SUBSCRIBER_EMAIL
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    ARTIFACT_UUID = state.gstate(STATE_ARTIFACT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--add",
        "--email", EMAIL,
        "--productuuid", PRODUCT_UUID,
        "--artifactuuid", ARTIFACT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    assert "items" in cart
    items = cart["items"]
    assert len(items) == 2

# PRODUCT_UUID="9b45de19-d688-4fd1-b5d3-872598a0293e" ;
# ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708" ;
# CART_UUID="aa62de43-b5b2-44ac-8d19-90e880a26586" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --remove \
#     --uuid "$CART_UUID" \
#     --productuuid "$PRODUCT_UUID" \
#     --artifactuuid "$ARTIFACT_UUID"
def test_cli_carts_remove_uuid():
    CART_UUID = state.gstate(STATE_CART_UUID)
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    ARTIFACT_UUID = state.gstate(STATE_ARTIFACT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--remove",
        "--uuid", CART_UUID,
        "--productuuid", PRODUCT_UUID,
        "--artifactuuid", ARTIFACT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    assert "items" in cart
    items = cart["items"]
    assert len(items) == 1


# PRODUCT_UUID="9b45de19-d688-4fd1-b5d3-872598a0293e" ;
# ARTIFACT_UUID="cd9ac396-eff1-4c0c-afc7-001a98d36708" ;
# EMAIL="subscriber.user@brodagroupsoftware.com" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT carts \
#     --remove \
#     --email "$EMAIL" \
#     --productuuid "$PRODUCT_UUID" \
#     --artifactuuid "$ARTIFACT_UUID"
def test_cli_carts_remove_email():
    EMAIL = SUBSCRIBER_EMAIL
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    ARTIFACT_UUID = state.gstate(STATE_ARTIFACT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--remove",
        "--email", EMAIL,
        "--productuuid", PRODUCT_UUID,
        "--artifactuuid", ARTIFACT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    assert "items" in cart
    items = cart["items"]
    assert len(items) == 0


# CART_UUID="aa62de43-b5b2-44ac-8d19-90e880a26586" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
#     --purchase \
#     --cartuuid "$CART_UUID"
def test_cli_orders_purchase():

    # Add item to the cart
    CART_UUID = state.gstate(STATE_CART_UUID)
    PRODUCT_UUID = state.gstate(STATE_PRODUCT_UUID)
    ARTIFACT_UUID = state.gstate(STATE_ARTIFACT_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "carts",
        "--add",
        "--uuid", CART_UUID,
        "--productuuid", PRODUCT_UUID,
        "--artifactuuid", ARTIFACT_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    cart = result
    assert "uuid" in cart
    cart_uuid = cart["uuid"]
    assert "subscriber" in cart
    subscriber_email = cart["subscriber"]
    assert subscriber_email == SUBSCRIBER_EMAIL
    assert "items" in cart
    items = cart["items"]
    assert len(items) == 1

    # Purchase the cart to create an order
    result = main([
        "--host", HOST,
        "--port", PORT,
        "orders",
        "--purchase",
        "--cartuuid", CART_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    order = result
    assert "uuid" in order
    order_uuid = order["uuid"]
    state.gstate(STATE_ORDER_UUID, order_uuid)


# ORDER_UUID="d4ff42fd-4f7b-4ab5-840a-30d7c8ff8a23" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT orders \
#     --retrieve \
#     --uuid "$ORDER_UUID"
def test_cli_orders_retrieve_uuid():
    ORDER_UUID = state.gstate(STATE_ORDER_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "orders",
        "--retrieve",
        "--uuid", ORDER_UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    order = result
    assert "uuid" in order
    order_subscriber = order["subscriber"]
    assert order_subscriber == SUBSCRIBER_EMAIL
    cart = order["cart"]
    cart_uuid = cart["uuid"]
    assert cart_uuid == state.gstate(STATE_CART_UUID)
    items = cart["items"]
    assert len(items) >= 1

