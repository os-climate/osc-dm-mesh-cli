# Copyright 2024 Broda Group Software Inc.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
# Created:  2024-04-15 by eric.broda@brodagroupsoftware.com
#####
#
# Command line interpreter (CLI) to interact with data mesh database
#
#####

import argparse
import logging
import requests
import sys
import json
from typing import List

from cliexec import CliExec
import state

LOGGING_FORMAT = "%(asctime)s - %(module)s:%(funcName)s %(levelname)s - %(message)s"
LOGGING_LEVEL = logging.INFO
logging.basicConfig(format=LOGGING_FORMAT, level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

STATUS_ARGUMENT_MISSING=100
STATUS_ARGUMENT_INVALID=101
STATUS_COMMAND_INVALID=102

STATE_PARSER="parser"

async def utility(args: argparse.Namespace):
    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    if args.dump:
        output = await cliexec.dump()
        output = json.dumps(output)
        return output
    else:
        await usage("Missing argument dump")
        sys.exit(STATUS_COMMAND_INVALID)


async def users(args: argparse.Namespace):
    """
    Function to handle the 'users' command.
    """
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    if args.register:
        if not args.role:
            await usage("Missing 'role' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.name:
            await usage("Missing 'name' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.email:
            await usage("Missing 'email' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.phone:
            await usage("Missing 'phone' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        else:
            logger.info("Executing create for new user")

        output = await cliexec.user_register(args.role, args.name, args.email, args.phone)
        output = json.dumps(output)
        return output

    elif args.retrieve:
        output = None
        if args.uuid:
            output = await cliexec.user_retrieve_uuid(args.uuid)
        elif args.role and args.email:
            output = await cliexec.user_retrieve_role_email(args.role, args.email)
        elif args.email:
            output = await cliexec.user_retrieve_email(args.email)
        else:
            output = await cliexec.user_retrieve_all()
        output = json.dumps(output)
        return output

    # COMPLETE THIS!
    elif args.update:
        if not args.uuid:
            await usage("Missing 'uuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.name:
            await usage("Missing 'name' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.email:
            await usage("Missing 'email' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.phone:
            await usage("Missing 'phone' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)

        # Convert tags from comma delimted string to List[str]
        output = await cliexec.user_update(args.uuid, args.email, args.name, args.phone)
        output = json.dumps(output)
        return output

    else:
        await usage("Unrecognized command")
        sys.exit(STATUS_COMMAND_INVALID)


async def products(args: any):
    """
    Function to handle the 'products' command.
    """
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    if args.assign:
        if not args.directory:
            await usage("Missing 'directory' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        output = await cliexec.product_assign(args.directory)
        output = json.dumps(output)
        return output

    elif args.generate:
        if args.namespace:
            output = await cliexec.product_generate(
                args.directory, args.filename, args.namespace,
                args.name, args.tags, args.description,
                args.url, args.vendor, args.model)
        else:
            output = await cliexec.product_artifact_generate(
                args.directory, args.filename, args.name,
                args.tags, args.data, args.description,
                args.url, args.vendor, args.model, args.type, host=args.service_host, port=args.service_port)

        return output

    elif args.retrieve:
        if args.namespace and args.name:
            output = await cliexec.product_retrieve_name(args.namespace, args.name)
        elif args.namespace:
            output = await cliexec.product_retrieve_namespace(args.namespace)
        elif args.email:
            output = await cliexec.product_retrieve_email(args.email)
        elif args.uuid:
            output = await cliexec.product_retrieve_uuid(args.uuid)
        elif args.uuids:
            output = await cliexec.product_retrieve_uuids(args.uuids)
        else:
            output = await cliexec.product_retrieve_all()
        output = json.dumps(output)
        return output

    elif args.discover:
        if not args.uuid:
            await usage("Missing 'uuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)

        output = await cliexec.product_discover_uuid(args.uuid)
        output = json.dumps(output)
        return output

    elif args.search:
        if not args.query:
            await usage("Missing 'query' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        output = await cliexec.product_search(args.query)
        output = json.dumps(output)
        return output

    # COMPLETE THIS
    elif args.update:
        if not args.namespace:
            await usage("Missing 'namespace' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.name:
            await usage("Missing 'name' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.publisher:
            await usage("Missing 'publisher' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.description:
            await usage("Missing 'description' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.tags:
            await usage("Missing 'tags' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)

        # Convert tags from comma delimted string to List[str]
        tags = [tag.strip() for tag in args.tags.split(",")]
        output = await cliexec.product_update(
                args.namespace, args.name, args.publisher,
                args.description, tags)
        output = json.dumps(output)
        return output

    else:
        print(f"")
        await usage("Unrecognized command")
        sys.exit(STATUS_COMMAND_INVALID)


async def artifacts(args: argparse.Namespace):
    """
    Function to handle the 'artifacts' command.
    """
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    if args.discover:
        output = None
        if args.productuuid and args.uuid:
            output = await cliexec.artifact_discover_uuid(args.productuuid, args.uuid)
        elif args.productuuid:
            output = await cliexec.artifact_discover_all(args.productuuid)
        output = json.dumps(output)
        return output

    else:
        await usage("Unrecognized command")
        sys.exit(STATUS_COMMAND_INVALID)


async def carts(args: argparse.Namespace):
    """
    Function to handle the 'carts' command.
    """
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    if args.add:
        if not args.productuuid :
            await usage("Missing 'productuuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.artifactuuid:
            await usage("Missing 'artifactuuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)

        output = None
        if args.uuid:
            output = await cliexec.cart_add_uuid(args.uuid, args.productuuid, args.artifactuuid)
        elif args.email:
            output = await cliexec.cart_add_email(args.email, args.productuuid, args.artifactuuid)
        output = json.dumps(output)
        return output

    elif args.remove:
        if not args.productuuid :
            await usage("Missing either 'productuuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.artifactuuid:
            await usage("Missing either 'artifactuuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)

        output = None
        if args.uuid:
            output = await cliexec.cart_remove_uuid(args.uuid, args.productuuid, args.artifactuuid)
        elif args.email:
            output = await cliexec.cart_remove_email(args.email, args.productuuid, args.artifactuuid)
        output = json.dumps(output)
        return output

    elif args.retrieve:
        output = None
        if args.uuid:
            output = await cliexec.cart_retrieve_uuid(args.uuid)
        elif args.email:
            output = await cliexec.cart_retrieve_email(args.email)
        else:
            output = await cliexec.cart_retrieve_all()
        output = json.dumps(output)
        return output

    else:
        await usage("Unrecognized command")
        sys.exit(STATUS_COMMAND_INVALID)


async def orders(args: argparse.Namespace):
    """
    Function to handle the 'orders' command.
    """
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    if args.purchase:
        if not args.cartuuid:
            await usage("Missing 'cartuuid' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        else:
            logger.info("Executing create for new order")

        output = await cliexec.order_purchase(args.cartuuid)
        output = json.dumps(output)
        return output

    elif args.retrieve:
        output = None
        if args.uuid:
            output = await cliexec.order_retrieve_uuid(args.uuid)
        elif args.email:
            output = await cliexec.order_retrieve_email(args.email)
        output = json.dumps(output)
        return output

    else:
        await usage("Unrecognized command")
        sys.exit(STATUS_COMMAND_INVALID)


async def auth(args: argparse.Namespace):
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    output = None
    if args.statistics:
        output = await cliexec.auth_statistics()
    elif args.status:
        if not args.email:
            await usage("Missing 'email' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        output = await cliexec.auth_status(args.email)
    elif args.login:
        if not args.email:
            await usage("Missing 'email' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.role:
            await usage("Missing 'role' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.password:
            await usage("Missing 'password' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        output = await cliexec.auth_login_user(args.role, args.email, args.password)
    elif args.logout:
        if not args.email:
            await usage("Missing 'email' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        if not args.role:
            await usage("Missing 'role' parameter")
            sys.exit(STATUS_ARGUMENT_MISSING)
        output = await cliexec.auth_logout_user(args.role, args.email)
    output = json.dumps(output)
    return output


async def monitor(args: argparse.Namespace):
    logger.info(f"{args}")

    if not is_valid_hostname(args.host):
        await usage("Invalid 'host' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)
    if not is_valid_port(args.port):
        await usage("Invalid 'port' parameter")
        sys.exit(STATUS_ARGUMENT_INVALID)

    cliexec = CliExec({
        "host": args.host,
        "port": args.port
    })

    output = None
    if args.health:
        output = await cliexec.monitor_health()
    elif args.metrics:
        output = await cliexec.monitor_metrics()
    output = json.dumps(output)
    return output


async def usage(msg: str):
    msg = f"Error: {msg}\n"
    print(msg)
    parser = state.gstate(STATE_PARSER)
    parser.print_help()


async def execute(xargs=None):
    """
    Main function that sets up the argparse CLI interface.
    """
    logger.info("executing")    # Initialize argparse and set general CLI description
    parser = argparse.ArgumentParser(description="Data Mesh Database CLI")
    state.gstate(STATE_PARSER, parser)

    # Parser for top-level commands
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument("--host", required=True, help="Registry host")
    parser.add_argument("--port", required=True, help="Registry port")

    # Create subparsers to handle multiple commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    utility_parser = subparsers.add_parser("utility", help="Utility service")
    utility_parser.add_argument("--dump", action='store_true', help="Dump registrar")
    utility_parser.add_argument("--generate", action='store_true', help="Dump registrar")
    utility_parser.add_argument("--config", required=False, help="Dump registrar")
    utility_parser.add_argument("--product", action='store_true', help="Dump registrar")
    utility_parser.add_argument("--artifact", action='store_true', help="Dump registrar")
    utility_parser.add_argument("--url", required=False, help="Dump registrar")
    utility_parser.add_argument("--output_file", required=False, help="Dump registrar")
    utility_parser.add_argument("--output_dir", required=False, help="Dump registrar")
    utility_parser.add_argument("--namespace", required=False, help="Dump registrar")
    utility_parser.add_argument("--tags", required=False, help="Dump registrar")

    users_parser = subparsers.add_parser("users", help="User information")
    group = users_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--register", action='store_true', help="Register a user")
    group.add_argument("--update", action='store_true', help="Update a user")
    group.add_argument("--retrieve", action='store_true', help="Retrieve a user")
    users_parser.add_argument("--role", help="Role of the user")
    users_parser.add_argument("--name", help="Name of the user")
    users_parser.add_argument("--email", help="Email for the user")
    users_parser.add_argument("--phone", help="Phone for the user")
    users_parser.add_argument("--uuid", help="UUID for the user")

    products_parser = subparsers.add_parser("products", help="Register a data product")
    group = products_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--assign", action='store_true', help="Assign UUIDs for products and artifacts")
    group.add_argument("--generate", action='store_true', help="Generate product and artifact configuration")
    group.add_argument("--register", action='store_true', help="Register a product")
    group.add_argument("--update", action='store_true', help="Update a product")
    group.add_argument("--retrieve", action='store_true', help="Retrieve a product")
    group.add_argument("--discover", action='store_true', help="Discover a product (go directly to the data product)")
    group.add_argument("--search", action='store_true', help="Search for a product")
    products_parser.add_argument("--directory", help="Directory for product configuration data")
    products_parser.add_argument("--filename", help="Filename containing product YAML configuration file")
    products_parser.add_argument("--address", help="Product IP address or DNS name")
    products_parser.add_argument("--namespace", help="Namespace for product")
    products_parser.add_argument("--name", help="Name for product")
    products_parser.add_argument("--tags", help="Product tags")

    products_parser.add_argument("--description", help="Product description")
    products_parser.add_argument("--url", help="Product site reference URL (for generating descriptions)")
    products_parser.add_argument("--data", help="Product site reference data")
    products_parser.add_argument("--uuid", help="UUID for product")
    products_parser.add_argument("--uuids", help="List of UUIDs for products")
    products_parser.add_argument("--email", help="Publisher email for product")
    products_parser.add_argument("--query", help="Query text")
    products_parser.add_argument("--vendor", help="Model vendor (currently, only OpenAI is supported)")
    products_parser.add_argument("--model", help="Model to use for generating description (must align to vendor)")
    # Used for the artifact generation
    products_parser.add_argument("--type", help="type of artifact being generated (service)")
    products_parser.add_argument("--service_host", help="Model to use for generating description (must align to vendor)")
    products_parser.add_argument("--service_port", help="Model to use for generating description (must align to vendor)")



    artifacts_parser = subparsers.add_parser("artifacts", help="Artifact information")
    group = artifacts_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--discover", action='store_true', help="Discover a product artifact (go directly to the data product)")
    artifacts_parser.add_argument("--uuid", help="UUID of artifact")
    artifacts_parser.add_argument("--productnamespace", help="Namespace of product")
    artifacts_parser.add_argument("--productname", help="Name of product")
    artifacts_parser.add_argument("--productuuid", help="UUID of product")
    artifacts_parser.add_argument("--name", help="Name of artifact")

    # Note that carts are created when a subscriber (role) is created
    # and hence can not be registered also
    carts_parser = subparsers.add_parser("carts", help="Cart information")
    group = carts_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", action='store_true', help="Add item to a cart")
    group.add_argument("--remove", action='store_true', help="Remove item to a cart")
    group.add_argument("--retrieve", action='store_true', help="Retrieve a cart")
    carts_parser.add_argument("--uuid", help="UUID of cart")
    carts_parser.add_argument("--email", help="Email (subscriber) of cart")
    carts_parser.add_argument("--item", help="Cart item")
    carts_parser.add_argument("--productuuid", help="Product UUID")
    carts_parser.add_argument("--artifactuuid", help="Artifact UUID")

    orders_parser = subparsers.add_parser("orders", help="Order information")
    group = orders_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action='store_true', help="Update an order")
    group.add_argument("--retrieve", action='store_true', help="Retrieve an order")
    group.add_argument("--purchase", action='store_true', help="Purchase the cart (and create an order)")
    orders_parser.add_argument("--cartuuid", help="Cart UUID")
    orders_parser.add_argument("--uuid", help="UUID of order")
    orders_parser.add_argument("--email", help="Email (subscriber) of order")

    # Parser for 'auth' command
    auth_parser = subparsers.add_parser("auth", help="Authenticate/authorize (login/logout) a user")
    group = auth_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--login", action='store_true', help="Login a user")
    group.add_argument("--logout", action='store_true', help="Logout a user")
    group.add_argument("--statistics", action='store_true', help="Show authentication statistics (all users)")
    group.add_argument("--status", action='store_true', help="Show authentication status for single user")
    auth_parser.add_argument("--role", help="Role of user")
    auth_parser.add_argument("--email", help="Email of user")
    auth_parser.add_argument("--password", help="Password of user")

    # Parser for 'monitor' command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor ecosystem platform components")
    group = monitor_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--health", action='store_true', help="Get health information")
    group.add_argument("--metrics", action='store_true', help="Get metrics information")
    monitor_parser.add_argument("--component", help="Name of the component")

    # Parse the arguments
    # args = parser.parse_args()
    args: argparse.Namespace = parser.parse_args(xargs if xargs is not None else sys.argv[1:])
    argsd = vars(args)

    # Set up logging - when "verbose" is set then
    # INFO level logs will be shown (all modules
    # issue INFO messages); If not set, then
    # WARNING level is setup and no logs (other
    # than WARNING/ERROR) will be shown
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    # Execute corresponding function based on provided command

    output = None
    if args.command == "utility":
        output = await utility(args)
    elif args.command == "users":
        output = await users(args)
    elif args.command == "auth":
        output = await auth(args)
    elif args.command == "products":
        output = await products(args)
    elif args.command == "artifacts":
        output = await artifacts(args)
    elif args.command == "carts":
        output = await carts(args)
    elif args.command == "orders":
        output = await orders(args)
    elif args.command == "monitor":
        output = await monitor(args)

    return output


def is_valid_hostname(host):
    import re
    if len(host) > 253:
        return False
    if host[-1] == ".":
        host = host[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in host.split("."))


def is_valid_port(port):
    try:
        port = int(port)
        return 0 <= port <= 65535
    except ValueError:
        return False


def main(args=None):
    import asyncio
    output = asyncio.run(execute(args))
    print(output)
    return output


if __name__ == "__main__":
    main(sys.argv[1:])

