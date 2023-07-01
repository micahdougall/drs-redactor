from __future__ import annotations
import json
from dataclasses import dataclass
from strenum import StrEnum
from dataclass_wizard import JSONWizard


# Google InfoType detector ref: https://cloud.google.com/dlp/docs/infotypes-reference
class InfoType(StrEnum):
    AGE = "AGE",
    CREDIT_CARD_NUMBER = "CREDIT_CARD_NUMBER",
    DATE_OF_BIRTH = "DATE_OF_BIRTH",
    EMAIL_ADDRESS = "EMAIL_ADDRESS",
    FIRST_NAME = "FIRST_NAME",
    GENDER = "GENDER",
    LAST_NAME = "LAST_NAME",
    LOCATION = "LOCATION",
    MEDICAL_RECORD_NUMBER = "MEDICAL_RECORD_NUMBER",
    PASSPORT = "PASSPORT",
    PERSON_NAME = "PERSON_NAME",
    PHONE_NUMBER = "PHONE_NUMBER",
    STREET_ADDRESS = "STREET_ADDRESS",
    VEHICLE_IDENTIFICATION_NUMBER = "VEHICLE_IDENTIFICATION_NUMBER"


@dataclass
class Tag(JSONWizard):
    class _(JSONWizard.Meta):
        debug_enabled = True
        raise_on_unknown_json_key = True

    field: str
    has_pii: bool
    info_type: InfoType = None
    likelihood_threshold: int = 4

    def __post_init__(self):
        assert 0 <= self.likelihood_threshold <= 5
