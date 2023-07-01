import google.cloud.dlp

CLIENT = google.cloud.dlp_v2.DlpServiceClient()


class DlpResponse:
    """A class to represent a DLP response"""

    def __init__(self, data):
        self.__dict__.update(data)


def is_pii_risk(finding: DlpResponse, max_likelihood_level: int) -> bool:
    """Maps a DLP finding to a boolean value based on the max likelihood level

    Args:
        finding: the DLP finding
        max_likelihood_level: the maximum likelihood level to consider

    Returns:
        True if the finding is above the max likelihood level, False otherwise
    """

    return {
        "LIKELIHOOD_UNSPECIFIED	": 0,
        "VERY_UNLIKELY": 1,
        "UNLIKELY": 2,
        "POSSIBLE": 3,
        "LIKELY": 4,
        "VERY_LIKELY": 5
    }.get(finding.likelihood) > max_likelihood_level


def inspect_string(project: str, inspect_config: str, data: str) -> dict:
    """Inspects a string of data for PII using the DLP API
    
    Args:
        project: the GCP project to use
        inspect_config: the job configuration as a json string
        data: the data to search within

    Returns:
        a dict of DLP findings
    """

    dlp_client = google.cloud.dlp_v2.DlpServiceClient()
    return dlp_client.inspect_content(
        request={
            "parent": f"projects/{project}",
            "inspect_config": inspect_config,
            "item": {"value": data}
        }
    )


def inspect_deidentify(
    project: str,
    deidentify_config: str,
    inspect_config: str,
    data: str
) -> dict:
    """
    Inspects a string of data for PII and masks sensitive data

    Args:
        project: the GCP project to use
        deidentify_config: configuration for the data redaction
        inspect_config: the job configuration as a json string
        data: the data to search within

    Returns:
        a file with PII data redacted

    """
    print(data)
    print(type(data))
    dlp_client = google.cloud.dlp_v2.DlpServiceClient()
    response = dlp_client.deidentify_content(
        request={
            "parent": f"projects/{project}",
            "deidentify_config": deidentify_config,
            "inspect_config": inspect_config,
            "item": {"value": data}
        }
    )
    return response.item.value