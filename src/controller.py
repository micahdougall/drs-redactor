import json

from dlp.tags import Tag
from dlp.service import inspect_string


def sanitise(
        project: str,
        inspect_config: str,
        payload: str,
        tags: dict
) -> dict:
    """Redacts sensitive data from a payload using DLP API along with explicit Data Catalog tags
    
    Args:
        project: GCP project ID
        inspect_config: DLP inspect config
        payload: the payload to sanitise
        tags: Data Catalog tags

    Returns:
        the sanitised payload
    """

    response = inspect_string(
        project,
        inspect_config,
        payload
    )

    pii_tags = Tag.from_list(tags)
    
    try:
        for finding in response.result.findings:
            print(f"Finding: {finding}")
            keys = get_keys_from_value(json.loads(payload), finding.quote)
            print(f"All matching keys for {finding.quote}: {keys}")

            # Redact fields where either:
            #   - Likeliness level from DLP is 'LIKELY' or above
            #   - Data Catalog tag has explicit PII classification
            #   - Data Catalog tag has likelihood threshold lower than DLP finding
            if finding.likelihood > 3 or any(
                map(
                    lambda tag: tag.field in keys and (
                        tag.has_pii or finding.likelihood > tag.likelihood_thresold
                    ), pii_tags
                )
            ):
                print(f"Redacting {finding.quote}")
                payload = payload.replace(finding.quote, "<REDACTED>")
    except AttributeError:
        print("No DLP findings in payload")

    return json.loads(payload)



def get_keys_from_value(data: any, value: str) -> list[str]:
    """Recursive method to find all the keys associated with a particular value in a dict

    Args:
        data: the original data containing the PII
            - should be a dict type at the first call
            - recursive calls could be a list or string
        value: the value to search for which is the 'quote' from a DlpResponse, ie
            - response.results.finding[i].quote

    Returns:
        a list of Keys which contain the PII value
    """

    print(f"Searching for {value} in {data}")
    _keys = []

    def _search_key(_data, _keys):
        if isinstance(_data, list):
            for item in _data:
                _search_key(item, _keys)
        elif isinstance(_data, dict):
            for (k, v) in _data.items():
                _keys.append(k) if v == value else _search_key(v, _keys)

    _search_key(data, _keys)
    return _keys
