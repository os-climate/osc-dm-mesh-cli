import logging
import yaml
import os
import json

from utl.webscraper import WebScraper
from utl.openaillm import OpenAIClient
from utl.tag_generator import _create_tags
from bgsexception import BgsException

logger = logging.getLogger(__name__)

def _create_description(vendor, model, url: str):

    scraper = WebScraper(url, depth=0)
    (actual_results, links) = scraper.scrape_single_page(url)
    actual_results = actual_results[:1000]

    # Ignore vendor for now, and just use OpenAI
    temperature = 0
    timeout = 100
    max_retries = 3
    llm = OpenAIClient(model=model)

    query = (
        "Provide a summary for a high level business product "
        "which details what data can be found. output should be a plain text description without headers, bold "
        "or other markdown formatting elements"
    )
    description = llm.send_prompt(query, actual_results)

    return description

def create_product_file(
        output_dir: str, file_name: str, namespace: str, name: str,
        tags: str | None, description: str | None, url: str, vendor: str, model: str):

    with open('./templates/product.yaml', 'r') as file:
        contents = yaml.safe_load(file)

    if not description:
        description = _create_description(vendor, model, url)

    hierarchy_file = "./config/hierarchy.yaml"
    with open(hierarchy_file, 'r') as file:
        hierarchy_contents = yaml.safe_load(file)

    available_tags = []
    # TODO do this with list comprehension
    for val in [*hierarchy_contents.values()]:
        for element in val:
            available_tags.extend(element.keys())

    if tags is None:
        tags = _create_tags(description, available_tags, vendor=vendor, model=model)
        tags = tags.strip().split(",")
    else:

        tags = tags.strip().split(",")
        with open(hierarchy_file, 'r') as file:
            hierarchy = yaml.safe_load(file)

        tags_hierarchy = []
        for val in [*hierarchy.values()]:
            for element in val:
                tags_hierarchy.extend(element.keys())
        for val in tags:
            if val not in tags_hierarchy:
                raise Exception(f"invalid tag: {val}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    contents["product"]["description"] = description
    contents["product"]["tags"] = tags
    contents["product"]["name"] = name
    contents["product"]["namespace"] = namespace

    fqpath = os.path.join(output_dir, file_name)
    with open(fqpath, 'w') as file:
        yaml.dump(contents, file)

    output = {"product": fqpath}
    output = json.dumps(output)
    return output

def create_artifact_file(
        output_dir: str, file_name: str, name: str, tags: str,
        data_url: str, description: str, url: str, vendor: str, model: str,
        artifact_type: str, host=None, port=None):

    hierarchy_file = "./config/hierarchy.yaml"
    with open(hierarchy_file, 'r') as file:
        hierarchy_contents = yaml.safe_load(file)

    available_tags = []
    # TODO do this with list comprehension
    for val in [*hierarchy_contents.values()]:
        for element in val:
            available_tags.extend(element.keys())

    if tags is None:
        tags = _create_tags(description, available_tags, vendor=vendor, model=model)
        tags = tags.strip().split(",")
    else:

        tags = tags.strip().split(",")
        with open(hierarchy_file, 'r') as file:
            hierarchy = yaml.safe_load(file)

        tags_hierarchy = []
        for val in [*hierarchy.values()]:
            for element in val:
                tags_hierarchy.extend(element.keys())

        for val in tags:
            if val not in tags_hierarchy:
                raise Exception(f"invalid tag: {val}")

    if not description:
        description = _create_description(vendor, model, url)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    artifacts_dir = os.path.join(output_dir, "artifacts")
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)

    with open('./templates/artifact.yaml', 'r') as file:
        contents = yaml.safe_load(file)

    contents["artifact"]["description"] = description
    contents["artifact"]["tags"] = tags
    contents["artifact"]["name"] = name
    contents["artifact"]["links"][0]["url"] = data_url


    if artifact_type == "service":
        contents["service"] = {}
        contents["service"]["host"] = host
        contents["service"]["port"] = port
    fqpath = os.path.join(artifacts_dir, file_name)
    with open(fqpath, 'w') as file:
        yaml.dump(contents, file)

    output = {"artifact": fqpath}
    output = json.dumps(output)
    return output
