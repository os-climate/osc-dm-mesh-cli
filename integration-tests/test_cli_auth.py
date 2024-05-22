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
# PREPARATION
#####


def test_preparation():
    # Create and save(global state) user UUIDs for
    # guest, subscriber, and publisher user ids
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
    guest_user_uuid = result[0]["uuid"]
    state.gstate(STATE_USER_GUEST_UUID, guest_user_uuid)

    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve",
        "--email", SUBSCRIBER_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    assert "uuid" in result[0]
    subscriber_user_uuid = result[0]["uuid"]
    state.gstate(STATE_USER_SUBSCRIBER_UUID, subscriber_user_uuid)

    result = main([
        "--host", HOST,
        "--port", PORT,
        "users",
        "--retrieve",
        "--email", PUBLISHER_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    assert "uuid" in result[0]
    publisher_user_uuid = result[0]["uuid"]
    state.gstate(STATE_USER_PUBLISHER_UUID, publisher_user_uuid)


#####
# AUTH (login/logout)
#####


# GUEST_EMAIL="guest.user@brodagroupsoftware.com" ;
# ROLE="guest" ;
# PASSWORD="a-fake-password" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
#     --login \
#     --role "$ROLE" \
#     --email "$GUEST_EMAIL" \
#     --password "$PASSWORD"
def test_cli_auth_login():
    PASSWORD="a-fake-password"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--login",
        "--email", GUEST_EMAIL,
        "--role", GUEST_ROLE,
        "--password", PASSWORD
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("status" in result)
    status = result["status"]
    assert status == "OK"

    PASSWORD="a-fake-password"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--login",
        "--email", SUBSCRIBER_EMAIL,
        "--role", SUBSCRIBER_ROLE,
        "--password", PASSWORD
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("status" in result)
    status = result["status"]
    assert status == "OK"

    PASSWORD="a-fake-password"
    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--login",
        "--email", PUBLISHER_EMAIL,
        "--role", PUBLISHER_ROLE,
        "--password", PASSWORD
    ])
    assert(result is not None)
    result = json.loads(result)
    assert("status" in result)
    status = result["status"]
    assert status == "OK"

# GUEST_EMAIL="guest.user@brodagroupsoftware.com"
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
#     --status \
#     --email "$GUEST_EMAIL"
def test_cli_auth_status():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--status",
        "--email", GUEST_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) == 1
    assert "email" in result[0]
    email = result[0]["email"]
    expected_email = GUEST_EMAIL
    assert email == expected_email

    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--status",
        "--email", SUBSCRIBER_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) == 1
    assert "email" in result[0]
    email = result[0]["email"]
    expected_email = SUBSCRIBER_EMAIL
    assert email == expected_email

    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--status",
        "--email", PUBLISHER_EMAIL
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) == 1
    assert "email" in result[0]
    email = result[0]["email"]
    expected_email = PUBLISHER_EMAIL
    assert email == expected_email


# python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
#     --statistics
def test_cli_auth_statistics():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--statistics"
    ])
    assert(result is not None)
    result = json.loads(result)
    assert len(result) >= 1
    assert "email" in result[0]
    email = result[0]["email"]
    expected_email = GUEST_EMAIL
    assert email == expected_email


# EMAIL="guest.user@brodagroupsoftware.com" ;
# ROLE="guest" ;
# python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
#     --logout \
#     --role "$ROLE" \
#     --email "$EMAIL"
def test_cli_auth_logout():
    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--logout",
        "--email", GUEST_EMAIL,
        "--role", GUEST_ROLE

    ])
    assert(result is not None)
    result = json.loads(result)
    assert("status" in result)
    status = result["status"]
    assert status == "OK"

    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--logout",
        "--email", SUBSCRIBER_EMAIL,
        "--role", SUBSCRIBER_ROLE

    ])
    assert(result is not None)
    result = json.loads(result)
    assert("status" in result)
    status = result["status"]
    assert status == "OK"

    result = main([
        "--host", HOST,
        "--port", PORT,
        "auth",
        "--logout",
        "--email", PUBLISHER_EMAIL,
        "--role", PUBLISHER_ROLE

    ])
    assert(result is not None)
    result = json.loads(result)
    assert("status" in result)
    status = result["status"]
    assert status == "OK"