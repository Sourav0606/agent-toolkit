from legacy import parse_legacy_payload
import pytest


def test_legacy_parser_deprecated_format():
    # Pre-existing failure in baseline!
    res = parse_legacy_payload("format_v1_data")
    assert res == {"parsed": True}
