import argparse
import contextlib
import json
import os
import unittest
from unittest.mock import ANY, MagicMock, call, patch

from .context import service


class ServiceTest(unittest.TestCase):

    def test_is_pii_risk(self):
        # Given
        max_level = 3
        finding = DlpResponse(likelihood="POSSIBLE")
        # When
        is_risk = service.is_pii_risk(finding, max_level)
        # Then
        self.assertTrue(is_risk)

    @patch("src.dlp.service.google.cloud.dlp_v2.DlpServiceClient")
    def test_inspect_string(self, mock_dlp_client):
        # Given
        mock_project = MagicMock()
        mock_config = MagicMock()
        data = {"name": "Bob", "email": "me@them.com"}
        # When
        redacted = service.inspect_deidentify(
            mock_project, mock_config, data
        )
        # Then
        assert mock_dlp_client.assert_called_once_with(
            project=mock_project,
            inspect_config=mock_config,
            data=data
        )

    @patch("src.dlp.service.inspect_deidentify.dlp_client")
    def test_inspect_deidentify(self, mock_dlp_client):
        # Given
        mock_project = MagicMock()
        mock_bucket = MagicMock()
        mock_config = MagicMock()
        data = {"name": "Bob", "email": "me@them.com"}
        # When
        redacted = service.inspect_deidentify(
            mock_project, mock_bucket, mock_config, data
        )
        # Then
        assert mock_dlp_client.assert_called_once_with(
            project=mock_project,
            deidentify_config=mock_config,
            inspect_config=mock_config,
            data=data
        )


if __name__ == "__main__":
    unittest.main()
