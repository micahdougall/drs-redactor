import unittest
import os
from unittest.mock import MagicMock, patch
import argparse
import json

from .context import controller, Tag


class TestController(unittest.TestCase):

    @patch(
        "src.dlp.service.inspect_string",
        return_value={
            "name": "Bob",
            "first_name": "Donald",
            "last_name": "Duck",
            "email": "donald.duck@test.com"
        }
    )
    def test_sanitise(self, mock_inspect_string):
        # Given
        mock_project = MagicMock()
        mock_inspect_config = MagicMock()

        payload = {
            "name": "Bob",
            "first_name": "Donald",
            "last_name": "Duck",
            "email": "donald.duck@test.com"
        }
        tags = [
            Tag("name", True, "FIRST_NAME", 1),
            Tag("email", True, "EMAIL_ADDRESS", 1),
        ]
        # When
        sanitised_payload = controller.sanitise(
            mock_project, mock_inspect_config, payload, tags
        )
        # Then
        self.assertEqual(
            sanitised_payload,
            {
                "name": "<REDACTED>",
                "first_name": "Donald",
                "last_name": "Duck",
                "email": "<REDACTED>"
            }
        )

    def test_update_tags(self):
        # Given
        tags = [
            Tag("phone", True, "PHONE_NUMBER", 1),
            Tag("email", True, "EMAIL_ADDRESS", 1),
            Tag("postcode", True, "POST_CODE", 1),
        ]
        keys = ["name", "first_name"]
        finding_name = "FIRST_NAME"
        # When
        controller.update_tags(finding_name, tags, keys)
        # Then
        self.assertEqual(
            tags,
            [
                Tag("phone", True, "PHONE_NUMBER", 1),
                Tag("email", True, "EMAIL_ADDRESS", 1),
                Tag("postcode", True, "POST_CODE", 1),
                Tag("name", True, "FIRST_NAME", 1),
                Tag("first_name", True, "FIRST_NAME", 1),
            ]
        )


    def test_strip_pii_by_keys(self):
        # Given
        data = {"key1": "value1", "key2": "value2", "key3": "value3"}
        keys = ["key1", "key2"]
        # When
        stripped_data = controller.strip_pii_by_keys(data, keys)
        # Then
        self.assertEqual(
            stripped_data,
            {"key1": "<REDACTED>", "key2": "<REDACTED>", "key3": "value3"}
        )

    def test_get_keys_from_value(self):
        # Given
        data = {"key1": "BOB", "key2": "value", "key3": "BOB"}
        value = "BOB"
        # When
        keys = controller.get_keys_from_value(data, value)
        # Then
        self.assertEqual(keys, ["key1", "key3"])


if __name__ == "__main__":
    unittest.main()
