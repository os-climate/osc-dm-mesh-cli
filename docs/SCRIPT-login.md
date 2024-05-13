# CLI Script - Login/Logout

This script demonstrates how to:
- create a guest users
- login a user (the previously created guest user)
- logout a user
- view login status for all users
- view the login status of a user


## Register a User (guest)

Let's register a guest:
~~~~
ROLE="guest" ;
EMAIL="guest.user@brodagroupsoftware.com" ;
NAME="Guest User" ;
PHONE="+1 647.555.1212" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT users \
    --register \
    --role "$ROLE" \
    --name "$NAME" \
    --email "$EMAIL" \
    --phone "$PHONE"

{"uuid": "76a7cf04-81e8-4d0d-8488-7a055db22b34"}
~~~~

## Login a User

Note that a user can login in several different roles,
which means we need to specify the desired role
at login.

Login the previously created guest user:
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
ROLE="guest" ;
PASSWORD="a-fake-password" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --login \
    --role "$ROLE" \
    --email "$EMAIL" \
    --password "$PASSWORD"

{"uuid": "76a7cf04-81e8-4d0d-8488-7a055db22b34", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-23 15:13:23.894", "updatetimestamp": "2024-03-23 15:13:23.894", "role": "guest"}
~~~~

## Logout a User

Logout the previously logged in guest user:
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
ROLE="guest" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --logout \
    --role "$ROLE" \
    --email "$EMAIL"

{"uuid": "76a7cf04-81e8-4d0d-8488-7a055db22b34", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-23 15:13:23.894", "updatetimestamp": "2024-03-23 15:13:23.894", "role": "guest"}
~~~~

## Get User Status for All Users

Let's look at user status for users:
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --statistics

[{"role": "guest", "email": "guest.user@brodagroupsoftware.com", "status": "unauthorized"}]
~~~~

Presumably you have followed the steps so far and your user has been logged out.
Now, to view a change in status, try to login the user again:
~~~~
EMAIL="guest.user@brodagroupsoftware.com" ;
ROLE="guest" ;
PASSWORD="a-fake-password" ;
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --login \
    --role "$ROLE" \
    --email "$EMAIL" \
    --password "$PASSWORD"

{"uuid": "76a7cf04-81e8-4d0d-8488-7a055db22b34", "contact": {"name": "Guest User", "email": "guest.user@brodagroupsoftware.com", "phone": "+1 647.555.1212"}, "createtimestamp": "2024-03-23 15:18:11.000", "updatetimestamp": "2024-03-23 15:18:11.000", "role": "guest"}
~~~~

Again, let's look at user activity statistics for users (the
user's status should be "authorized"):
~~~~
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --statistics

[{"role": "guest", "email": "guest.user@brodagroupsoftware.com", "status": "authorized"}]
~~~~

## Get a User's Login Status

Note that a user can be logged in using multiple roles
and hence a list of status are returned instead of a single item.

Let's look at the login status of our guest user:
~~~~
EMAIL="guest.user@brodagroupsoftware.com"
python ./src/cli.py $VERBOSE --host $HOST --port $PORT auth \
    --status \
    --email "$EMAIL"

[{"role": "guest", "email": "guest.user@brodagroupsoftware.com", "status": "authorized"}]
~~~~

