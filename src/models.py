# Copyright 2024 Broda Group Software Inc.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#
# Created:  2024-04-15 by eric.broda@brodagroupsoftware.com
# NOTE: It is important to ensure this file is identical to that
# in the bgssrv-dmregistry server models.py or you will
# get 422 Unprocessed Entity errors

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Optional
from enum import Enum


ROLE_GUEST = "guest"
ROLE_PUBLISHER = "publisher"
ROLE_SUBSCRIBER = "subscriber"
ROLE_ADMINISTRATOR = "administrator"

class Product(BaseModel):
    uuid: Optional[str] = None
    namespace: str
    name: str
    publisher: str
    description: str
    tags: List[str]
    address: Optional[str] = None
    createtimestamp: Optional[str] = None
    updatetimestamp: Optional[str] = None

class Contact(BaseModel):
    name: str
    email: str
    phone: str

class User(BaseModel):
    uuid: Optional[str] = None
    contact: Contact  # Assuming Contact is a defined Pydantic model
    # address: Address  # Assuming Address is a defined Pydantic model
    createtimestamp: Optional[str] = None
    updatetimestamp: Optional[str] = None
    role: str  # Add the 'role' attribute here

class Event(BaseModel):
    type: str
    email: str
    logintimestamp: Optional[str] = None

# Registration for product
class Registration(BaseModel):
    product: Product
    artifact_names: List[str]

# Registration UUIDs for product
# containing uuids for product, and each artifact
class UUIDs(BaseModel):
    product_uuid: str
    artifact_uuids: List[Dict[str, str]]
