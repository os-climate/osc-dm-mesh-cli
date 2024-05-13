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
STATE_USER_GUEST_UUID="guest-user-uuid"
STATE_USER_SUBSCRIBER_UUID="subscriber-user-uuid"
STATE_USER_PUBLISHER_UUID="publisher-user-uuid"

# Common for all CLI commands
HOST="localhost"
PORT="20000"
GUEST_EMAIL="guest.user@brodagroupsoftware.com"
GUEST_ROLE="guest"
SUBSCRIBER_EMAIL="subscriber.user@brodagroupsoftware.com"
SUBSCRIBER_ROLE="subscriber"
PUBLISHER_EMAIL="publisher.user@brodagroupsoftware.com"
PUBLISHER_ROLE="publisher"


#####
# USERS
#####


# ROLE="guest" ;
# GUEST_EMAIL="guest.user@brodagroupsoftware.com" ;
# NAME="Guest User" ;
# PHONE="+1 647.555.1212" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
#     --register \
#     --role "$ROLE" \
#     --name "$NAME" \
#     --email "$GUEST_EMAIL" \
#     --phone "$PHONE"
def test_cli_users_register():
    # GUEST USER
    NAME="Guest User"
    PHONE="+1 647.555.1212"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--register",
        "--role", GUEST_ROLE,
        "--name", NAME,
        "--email", GUEST_EMAIL,
        "--phone", PHONE
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    user_uuid = result["uuid"]
    state.gstate(STATE_USER_GUEST_UUID, user_uuid)

    # SUBSCRIBER USER
    NAME="Subscriber User"
    PHONE="+1 647.555.1212"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--register",
        "--role", SUBSCRIBER_ROLE,
        "--name", NAME,
        "--email", SUBSCRIBER_EMAIL,
        "--phone", PHONE
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    user_uuid = result["uuid"]
    state.gstate(STATE_USER_SUBSCRIBER_UUID, user_uuid)

    # PUBLISHER USER
    NAME="Publisher User"
    PHONE="+1 647.555.1212"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--register",
        "--role", PUBLISHER_ROLE,
        "--name", NAME,
        "--email", PUBLISHER_EMAIL,
        "--phone", PHONE
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    user_uuid = result["uuid"]
    state.gstate(STATE_USER_PUBLISHER_UUID, user_uuid)


# python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
#     --retrieve
def test_cli_users_retrieve():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve"
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    user_uuid = result[0]["uuid"]
    expected_uuid = state.gstate(STATE_USER_GUEST_UUID)
    assert user_uuid == expected_uuid


# UUID="7eec771b-6140-4741-9845-2e52857c1cb3" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
#     --retrieve \
#     --uuid "$UUID"
def test_cli_users_retrieve_uuid():
    UUID=state.gstate(STATE_USER_GUEST_UUID)
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve",
        "--uuid", UUID
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    user_uuid = result["uuid"]
    expected_uuid = state.gstate(STATE_USER_GUEST_UUID)
    assert user_uuid == expected_uuid


# GUEST_EMAIL="guest.user@brodagroupsoftware.com" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
#     --retrieve \
#     --email "$GUEST_EMAIL"
def test_cli_users_retrieve_email():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve",
        "--email", GUEST_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    assert "uuid" in result[0]
    user_uuid = result[0]["uuid"]
    expected_uuid = state.gstate(STATE_USER_GUEST_UUID)
    assert user_uuid == expected_uuid


# ROLE="guest" ;
# GUEST_EMAIL="guest.user@brodagroupsoftware.com" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
#     --retrieve \
#     --role "$ROLE" \
#     --email "$GUEST_EMAIL"
def test_cli_users_retrieve_role_email():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve",
        "--role", GUEST_ROLE,
        "--email", GUEST_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("uuid" in result)
    user_uuid = result["uuid"]
    expected_uuid = state.gstate(STATE_USER_GUEST_UUID)
    assert user_uuid == expected_uuid
