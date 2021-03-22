import os
import sys

import lxml.etree as etree
import pytest

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)

import src.lib.etl as etl


@pytest.fixture
def example_tei():
    with open(f"{ROOT_PATH}/test/lib/example.tei.xml", "rb") as fo:
        return etree.XML(fo.read())


@pytest.fixture
def empty_tei():
    return etree.XML(
        """<?xml version="1.0" encoding="UTF-8"?>
<TEI xml:space="preserve" xmlns="http://www.tei-c.org/ns/1.0"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.tei-c.org/ns/1.0 /opt/grobid/grobid-home/schemas/xsd/Grobid.xsd"
 xmlns:xlink="http://www.w3.org/1999/xlink"></TEI>""".encode()
    )


def test_get_date(example_tei):
    assert etl.get_date(example_tei) == "2010-08-22"


def test_missing_date(empty_tei):
    assert etl.get_date(empty_tei) == ""


def test_get_text(example_tei):
    paper_text = etl.get_all_text(example_tei)
    assert len(paper_text) == 24577
    assert "fluctuations in suspended and seabed sediments" in paper_text


def test_no_text(empty_tei):
    assert etl.get_all_text(empty_tei) == ""
