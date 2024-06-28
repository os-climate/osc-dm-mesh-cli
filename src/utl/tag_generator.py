from utl.openaillm import OpenAIClient
import yaml
import logging

logger = logging.getLogger(__name__)
def _create_tags(data, available_tags, vendor=None, model="gpt-4o",):
    if model is None:
        model = "gpt-4o"

    tags = ",".join(available_tags)


    # Ignore vendor for now, and just use OpenAI
    temperature = 0
    timeout = 100
    max_retries = 3
    llm = OpenAIClient(model=model)

    query = (
        "From the list of tags provided as context, "
        "return ONLY a comma separated list of 1 to 3 tags that apply to the following data, labeled DATA\n\n"
        "DATA:{}\n\n"
    )
    query = query.format(data)
    logger.info(f"query being sent: {query}")
    out_tags = llm.send_prompt(query, tags)
    logger.info(f"created tags: {out_tags}")
    return out_tags