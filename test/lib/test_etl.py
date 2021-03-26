import os
import sys
import lxml.etree as etree
import pytest

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)

import src.lib.etl as etl  # noqa: E402


@pytest.fixture
def example_tei():
    with open(f"{ROOT_PATH}/test/fixtures/example.tei.xml", "rb") as fo:
        return etree.XML(fo.read())


@pytest.fixture
def empty_tei():
    return etree.XML(
        """<?xml version="1.0" encoding="UTF-8"?>
<TEI xml:space="preserve" xmlns="http://www.tei-c.org/ns/1.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.tei-c.org/ns/1.0 /opt/grobid/grobid-home/schemas/xsd/Grobid.xsd"
 xmlns:xlink="http://www.w3.org/1999/xlink"></TEI>""".encode()  # noqa: E501
    )


def test_get_date(example_tei):
    assert etl.get_date(example_tei) == "2010-08-22"


def test_missing_date(empty_tei):
    assert etl.get_date(empty_tei) == ""
