# Copyright 2024 Broda Group Software Inc.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
# Created:  2024-04-15 by eric.broda@brodagroupsoftware.com
import logging
import os
import sys
import uuid
from datetime import datetime
import yaml
from typing import List
import getpass

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

import utilities
import models
import constants
from bgsexception import BgsException

ENDPOINT_PREFIX = "/api"
REGISTRAR_API=ENDPOINT_PREFIX + "/registrar"
SEARCH_API=ENDPOINT_PREFIX + "/search"
DATAPRODUCT_API=ENDPOINT_PREFIX + "/dataproducts"
MONITOR_API=ENDPOINT_PREFIX + "/monitor"

# Set up logging
# LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)

# Abstract class
class CliExec():

    host = None
    port = None

    def __init__(self, config: dict):
        """Create CLI"""
        logger.info(f"Using config:{config}")
        self.host = config["host"]
        self.port = config["port"]


    ####
    # UTILITY
    #####


    async def dump(self):
        """Dump registry"""
        logger.info("Dump registry")
        service = REGISTRAR_API + "/dump"
        method = "GET"
        response = await utilities.httprequest(self.host, self.port, service, method)
        return response


    #####
    # USERS
    #####


    async def user_register(self, role: str, name: str, email: str, phone: str):
        """Register user"""

        logger.info(f"Registering user name:{name} email:{email} phone:{phone}")

        # Create contact
        contact = models.Contact(
            name=name,
            email=email,
            phone=phone
        )

        # Create a Publisher instance using the Contact instance
        user = models.User(
            contact=contact,
            role=role
        )
        logger.info(f"Using user:{user}")
        user_dict = user.model_dump()

        service = REGISTRAR_API + "/users"
        method = "POST"
        headers = self._create_headers()
        response = await utilities.httprequest(self.host, self.port, service, method, headers=headers, obj=user_dict)
        logger.info(f"Registering user name:{name} email:{email} phone:{phone}, response:{response}")

        return response


    async def user_retrieve_all(self):
        """Retrieve all users"""
        logger.info("Show users")
        service = REGISTRAR_API + "/users"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    async def user_retrieve_uuid(self, uuid: str):
        """Retrieve user by UUID"""
        logger.info(f"View user uuid:{uuid}")
        service = REGISTRAR_API + f"/users/uuid/{uuid}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    async def user_retrieve_email(self, email: str):
        """Retrieve user by UUID"""
        logger.info(f"View users by email:{email}")
        service = REGISTRAR_API + f"/users/email/{email}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    async def user_retrieve_role_email(self, role: str, email: str):
        """Retrieve user by role/email"""
        logger.info(f"Show user role:{role} email:{email}")
        service = REGISTRAR_API + f"/users/role/{role}/email/{email}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    #####
    # PRODUCTS
    #####


    async def product_generate(self, directory: str):
        """Register data product directory"""

        logger.info(f"Registering directory (directory):{directory}")

        # Check if directory exists
        if not os.path.exists(directory):
            msg = f"Directory does not exist:{directory}"
            logger.error(msg)
            raise BgsException(msg)

        # Check if UUIDs already exist
        filename = "uuids.yaml"
        fqfilename = os.path.join(directory, filename)
        if os.path.exists(fqfilename):
            msg = f"UUIDs have already been generated:{fqfilename}"
            logger.error(msg)
            raise BgsException(msg)

        # Load the product to verify it is valid
        product: models.Product = await self._load_product(directory)
        if not product:
            msg = f"Could not load product, directory:{directory}"
            logger.error(msg)
            raise BgsException(msg)

        # Load the artifacts to verify they are valid
        artifact_names: List[str] = await self._load_artifacts(directory)
        if not artifact_names:
            msg = f"Could not load artifacts, directory:{directory}"
            logger.error(msg)
            raise BgsException(msg)

        # Generate the product UUID
        product_uuid = f"{uuid.uuid4()}"

        # Generate the artifact UUIDs
        artifacts = []
        for artifact_name in artifact_names:
            artifact_uuid = f"{uuid.uuid4()}"
            artifact = { artifact_name: artifact_uuid }
            logger.info(f"Registering artifact:{artifact}")
            artifacts.append(artifact)
        sorted_artifacts = sorted(artifacts, key=lambda x: sorted(x.keys()))
        artifact_yaml = yaml.dump(sorted_artifacts)

        import getpass
        generation_user = getpass.getuser()
        generation_date = datetime.now().strftime("%d-%b-%Y %H:%M:%S %Z")
        details = (
            "##### \n"
            "# \n"
            "# UUIDs Definition \n"
            "# \n"
            "# This file contains the UUIDs for your product and artifacts (by name) \n"
            "# \n"
            "# ----- \n"
            "# \n"
            f"# Generated on: {generation_date} \n"
            f"# Generated by: {generation_user} \n"
            "# \n"
            "##### \n"
        )
        details = details + f"product_uuid: {product_uuid}  \n"
        details += f"artifact_uuids: \n{artifact_yaml}  \n"

        # Write the ordered YAML string to a file (this is a
        # record for product owner for all UUIDs related
        # to this product)
        with open(fqfilename, 'w') as file:
            file.write(details)

        logger.info(f"Registering directory:{directory}, filename:{fqfilename} details:{details}")

        response = {
            "uuids": fqfilename,
            "product_uuid": product_uuid,
            "artifact_uuids": sorted_artifacts
        }

        return response


    async def deprecated_product_register(self, directory: str, address: str):
        """Register data product directory"""

        logger.info(f"Registering directory (directory):{directory}")

        # Acquire the product UUIDs
        filename = "uuids.yaml"
        fqfilename = os.path.join(directory, filename)
        uuids_dict = None
        with open(fqfilename, 'r') as file:
            uuids_dict = yaml.safe_load(file)

        # Write the address to a YAML file (this a
        # record for product owner for what they submitted)
        filename = "registration.yaml"
        fqfilename = os.path.join(directory, filename)

        import getpass
        registration_user = getpass.getuser()
        registration_date = datetime.now().strftime("%d-%b-%Y %H:%M:%S %Z")
        details = (
            "##### \n"
            "# \n"
            "# Data Product Address Registration \n"
            "# \n"
            "# This file contains the address for your product \n"
            "# \n"
            "# ----- \n"
            "# \n"
            f"# Registered on: {registration_date} \n"
            f"# Registered by: {registration_user} \n"
            "# \n"
            "##### \n"
        )
        details = details + f"address: {address}  \n"
        logger.info(f"details:{details}")
        with open(fqfilename, 'w') as file:
            file.write(details)

        product: models.Product = await self._load_product(directory)
        product.uuid = uuids_dict["product_uuid"]
        product.address = address

        logger.info(f"Registering product:{product}")
        product_dict = product.model_dump()

        service = REGISTRAR_API + "/products"
        method = "POST"
        headers = self._create_headers()
        xproduct = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers, obj=product_dict)
        response = {
            "product": xproduct,
            "fqfilename": fqfilename
        }

        logger.info(f"Registering directory (directory):{directory}, response:{response}")
        return response


    async def product_retrieve_all(self):
        """Retrieve all products"""
        logger.info("Retrieve all products")
        service = REGISTRAR_API + "/products"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve all products, response:{response}")

        return response


    async def product_retrieve_namespace(self, namespace: str):
        """Retrieve all products for a namespace"""

        logger.info(f"Retrieve product namespace:{namespace}")

        service = REGISTRAR_API + f"/products/namespace/{namespace}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve product namespace:{namespace}, response:{response}")

        return response


    async def product_retrieve_name(self, namespace: str, name: str):
        """Retrieve product by namespace and name"""

        logger.info(f"Retrieve product namespace:{namespace} name:{name}")

        service = REGISTRAR_API + f"/products/namespace/{namespace}/name/{name}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve product namespace:{namespace} name:{name}, response:{response}")

        return response


    async def product_retrieve_email(self, email: str):
        """Retrieve product by publisher email"""

        logger.info(f"Retrieve product publisher email:{email}")

        service = REGISTRAR_API + f"/products/email/{email}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve product publisher email:{email}, response:{response}")

        return response


    async def product_retrieve_uuid(self, uuid: str):
        """Retrieve product for single uuid"""

        logger.info(f"Retrieve product uuid:{uuid}")

        service = REGISTRAR_API + f"/products/uuid/{uuid}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve product uuid:{uuid}, response:{response}")

        return response


    async def product_retrieve_uuids(self, uuids: str):
        """
        Retrieve product for list of uuids.
        Note that the input uuids parameter is a
        list of UUIDs delimited by a space.
        """

        logger.info(f"Retrieve product uuids:{uuids}")

        xuuids = uuids.split()
        logger.info(f"Using 1xuuids:{xuuids}")

        payload = {"uuids": xuuids}

        service = REGISTRAR_API + f"/products/uuids/"
        method = "POST"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers, obj=payload)
        logger.info(f"Retrieve product uuids:{uuids}, response:{response}")

        return response


    async def product_discover_uuid(self, uuid: str):
        """Discover product by uuid"""
        logger.info(f"Discover product uuid:{uuid}")
        service = DATAPRODUCT_API + f"/uuid/{uuid}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Discover product uuid:{uuid}, response:{response}")
        return response


    async def product_search(self, query: str):
        """Query product"""
        logger.info(f"Search products query:{query}")

        # A quick note on why I am using a POST instead of a GET
        # for a search request... Traditionally, GET requests are used to
        # retrieve data from a server. They append the query parameters
        # to the URL, which is straightforward for simple queries.
        # However, URLs have a length limit, which can vary by
        # browser and server but generally hovers around 2,000
        # characters. This limitation makes GET less suitable
        # for very large text strings. Moreover, since GET parameters
        # are included in the URL, they are logged in server
        # logs and browser history, posing potential security
        # or privacy issues for sensitive data.
        #
        # POST requests, on the other hand, send data to the server
        # in the body of the request. This allows them to carry much
        # larger amounts of data without the limitations imposed on URL
        # length. POST requests are also inherently more secure in terms
        # of concealing data from URL logs and browser history.
        service = SEARCH_API + "/query"
        method = "POST"

        request = {
            "query": query
        }
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers, obj=request)
        logger.info(f"Search products query:{query}, response:{response}")
        return response


    #####
    # PRODUCT ARTIFACTS
    #####


    async def artifact_discover_all(self, product_uuid: str):
        """Discover all artifacts for a product"""

        logger.info(f"Discover all artifacts for a product uuid:{product_uuid}")

        service = DATAPRODUCT_API + f"/uuid/{product_uuid}/artifacts"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Discover all artifacts for a product uuid:{product_uuid}, response:{response}")

        return response


    async def artifact_discover_uuid(self, product_uuid: str, uuid: str):
        """Discover product artifact by uuid"""

        logger.info(f"Discover product uuid:{product_uuid} artifact uuid:{uuid}")

        service = DATAPRODUCT_API + f"/uuid/{product_uuid}/artifacts/{uuid}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Discover product product_uuid:{product_uuid} artifact uuid:{uuid}, response:{response}")

        return response


    #####
    # CARTS
    #####


    async def cart_retrieve_all(self):
        """Retrieve all carts"""
        logger.info("Retrieve all carts")
        service = REGISTRAR_API + "/carts"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve all carts, response:{response}")
        return response


    async def cart_retrieve_uuid(self, uuid: str):
        """Retrieve cart by uuid"""
        logger.info(f"Retrieve cart uuid:{uuid}")
        service = REGISTRAR_API + f"/carts/uuid/{uuid}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve cart uuid:{uuid}, response:{response}")
        return response


    async def cart_retrieve_email(self, email: str):
        """Retrieve cart by subscriber email"""
        logger.info(f"Retrieve cart publisher email:{email}")
        service = REGISTRAR_API + f"/carts/email/{email}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve cart publisher email:{email}, response:{response}")
        return response


    async def cart_add_uuid(self, uuid: str, productuuid: str, artifactuuid: str):
        """Add to cart by uuid"""
        logger.info(f"Add cart uuid:{uuid} productuuid:{productuuid} artifactuuid:{artifactuuid}")

        service = REGISTRAR_API + f"/carts/uuid/{uuid}/{productuuid}/{artifactuuid}"
        method = "POST"

        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Add cart uuid:{uuid} productuuid:{productuuid} artifactuuid:{artifactuuid}, response:{response}")
        return response


    async def cart_remove_uuid(self, uuid: str, productuuid: str, artifactuuid: str):
        """Remove item from cart by uuid"""
        logger.info(f"Remove cart uuid:{uuid} productuuid:{productuuid} artifactuuid:{artifactuuid}")

        service = REGISTRAR_API + f"/carts/uuid/{uuid}/{productuuid}/{artifactuuid}"
        method = "DELETE"

        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Remove cart uuid:{uuid} productuuid:{productuuid} artifactuuid:{artifactuuid}, response:{response}")
        return response


    async def cart_add_email(self, email: str, productuuid: str, artifactuuid: str):
        """Add to cart by email"""
        logger.info(f"Retrieve cart email:{email}")

        service = REGISTRAR_API + f"/carts/email/{email}/{productuuid}/{artifactuuid}"
        method = "POST"

        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve cart email:{email}, response:{response}")
        return response


    async def cart_remove_email(self, email: str, productuuid: str, artifactuuid: str):
        """Remove item from cart by email"""
        logger.info(f"Retrieve cart email:{email}")

        service = REGISTRAR_API + f"/carts/email/{email}/{productuuid}/{artifactuuid}"
        method = "DELETE"

        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve cart email:{email}, response:{response}")
        return response


    async def order_purchase(self, cartuuid: str):
        """Purchase cart and create order"""

        logger.info(f"Purchase cart cartuuid:{cartuuid}")

        request_dict = {
            "cartuuid": cartuuid
        }
        logger.info(f"Using request_dict:{request_dict}")

        service = REGISTRAR_API + "/orders"
        method = "POST"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers, obj=request_dict)
        logger.info(f"Purchase cart cartuuid:{cartuuid}, response:{response}")

        return response


    async def order_retrieve_uuid(self, uuid: str):
        """Retrieve order by uuid"""
        logger.info(f"Retrieve order uuid:{uuid}")
        service = REGISTRAR_API + f"/orders/uuid/{uuid}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve order uuid:{uuid}, response:{response}")
        return response


    async def order_retrieve_email(self, email: str):
        """Retrieve order by subscriber email"""
        logger.info(f"Retrieve order email:{email}")
        service = REGISTRAR_API + f"/orders/email/{email}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        logger.info(f"Retrieve order email:{email}, response:{response}")
        return response


    #####
    # AUTH (login/logout)
    #####


    async def auth_login_user(self, role: str, email: str, password: str):
        """Login user (via email)"""
        logger.info(f"Event (login) user role:{role} email:{email} password:{password}")

        payload = {
            "role": role,
            "email": email,
            "password": password
        }
        service = REGISTRAR_API + "/auth/login"
        method = "POST"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers, obj=payload)
        return response


    async def auth_logout_user(self, role: str, email: str):
        """Logout user (via email)"""
        logger.info(f"Event (logout) user role:{role} email:{email}")

        payload = {
            "role": role,
            "email": email
        }
        service = REGISTRAR_API + "/auth/logout"
        method = "POST"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers, obj=payload)
        return response


    async def auth_statistics(self):
        """Login statistics (all users)"""
        logger.info("Show login statistics")
        service = REGISTRAR_API + "/auth/statistics"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    async def auth_status(self, email: str):
        """Login status for an email"""
        logger.info(f"Show login status for email:{email}")
        service = REGISTRAR_API + f"/auth/status/{email}"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    #####
    # MONITOR
    #####


    async def monitor_health(self):
        """Monitor ecosystem platform health"""
        logger.info("Monitor ecosystem platform health")
        service = MONITOR_API + "/health"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    async def monitor_metrics(self):
        """Monitor ecosystem platform metrics"""
        logger.info("Monitor ecosystem platform metrics")
        service = MONITOR_API + "/metrics"
        method = "GET"
        headers = self._create_headers()
        response = await utilities.httprequest(
            self.host, self.port, service, method, headers=headers)
        return response


    #####
    # INTERNAL
    #####

    def _create_headers(self):
        headers = {
            constants.HEADER_USERNAME: getpass.getuser(),
            constants.HEADER_CORRELATION_ID: str(uuid.uuid4())
        }
        return headers


    async def _order_yaml(self, uuids):
        logger.info(f"uuids:{uuids}")
        # Order the YAML in an intuitive way

        from collections import OrderedDict
        data = OrderedDict([
            ("product_uuid", uuids["product_uuid"]),
            ('artifact_uuids', uuids["artifact_uuids"])
        ])
        logger.info(f"data:{data}")
        # Function to represent OrderedDict as a regular dict in YAML
        def represent_ordereddict(dumper, data):
            return dumper.represent_dict(data.items())
        yaml.add_representer(OrderedDict, represent_ordereddict)
        order_uuids = yaml.dump(data, default_flow_style=False)
        logger.info(f"order_uuids:{order_uuids}")
        return order_uuids


    async def _load_product(self, directory: str):
        file_path = os.path.join(directory, "product.yaml")
        logger.info(f"Loading product:{file_path}")

        product: models.Product = None
        with open(file_path, 'r') as f:
            try:
                data = yaml.safe_load(f)
                data = data["product"]
                product = models.Product(**data)

            except yaml.YAMLError as e:
                msg = f"Error reading YAML file {file_path}: {e}"
                logger.error(msg, exc_info=True)
                raise BgsException(msg, e)
        return product


    async def _load_artifacts(self, directory: str):
        artifact_names = []
        for root, dirs, files in os.walk(directory):
            if root.endswith("artifacts"):
                # logger.info(f"Loading artifacts:{files}")
                for file in files:
                    if file.endswith(".yaml") or file.endswith(".yml"):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            try:
                                logger.info(f"Loading artifact:{file_path}")
                                data = yaml.safe_load(f)
                                # logger.info(f"Loading data:{data}")
                                artifact_name = data["artifact"]["name"]
                                artifact_names.append(artifact_name)
                            except yaml.YAMLError as e:
                                msg = f"Error reading YAML file {file_path}: {e}"
                                logger.error(msg, exc_info=True)
                                raise BgsException(msg, e)
        return artifact_names

