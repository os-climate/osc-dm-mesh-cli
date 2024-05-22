import logging
import yaml
import os
import json

from utl.webscraper import WebScraper
from utl.openaillm import OpenAIClient
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
        tags: str, description: str, url: str, vendor: str, model: str):

    if not description:
        description = _create_description(vendor, model, url)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open('./templates/product.yaml', 'r') as file:
        contents = yaml.safe_load(file)

    contents["product"]["description"] = description
    contents["product"]["tags"] = tags.strip().split(",")
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
        data_url: str, description: str, url: str, vendor: str, model: str):

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
    contents["artifact"]["tags"] = tags.strip().split(",")
    contents["artifact"]["name"] = name
    contents["artifact"]["links"][0]["url"] = data_url

    fqpath = os.path.join(artifacts_dir, file_name)
    with open(fqpath, 'w') as file:
        yaml.dump(contents, file)

    output = {"artifact": fqpath}
    output = json.dumps(output)
    return output

