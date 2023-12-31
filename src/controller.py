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

                # Update high probability tags
                update_tags(pii_tags, keys, finding.info_type.name)

    except AttributeError:
        print("No DLP findings in payload")

    # Remove all fields which are explicitly tagged as PII
    return strip_pii_by_keys(
        json.loads(payload), 
        [pii.field for pii in pii_tags if pii.has_pii]
    )


def update_tags(finding_name: str, tags: list[Tag], keys: list[str]) -> None:
    """Adds new tags based on DLP findings
    
    Args:
        finding_name: the name of the DLP finding
        tags: the list of tags to append to
        keys: the list of keys which correspond to the DLP finding info type
    """

    if finding_name not in [tag.info_type for tag in tags]:
        for key in keys:
            tags.append(
                Tag(key, True, finding_name, 1)
            )


def strip_pii_by_keys(data: dict, keys: str) -> dict:
    """Recursively redacts values from a dictioary based on a list of keys.

    Args:
        data: the original data containing the PII
    
    Returns:
        a list of PII tag names whose values should be redacted
    """

    for key, value in data.items():
        if isinstance(value, dict):
            data.update({key: strip_pii_by_keys(value, keys)})
        elif isinstance(value, list):
            for item in value:
                data.update({key: strip_pii_by_keys(item, keys)})
        elif key in keys:
            data.update({key: "<REDACTED>"})
    return data


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
