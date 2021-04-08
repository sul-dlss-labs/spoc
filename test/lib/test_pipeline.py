import os
import sys

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)

import src.lib.pipeline as pipeline  # noqa: E402


def test_nlp():
    doc = pipeline.nlp("A sea ammonia in Pacific Grove")
    ammonia_id = "urn:lsid:marinespecies.org:taxname:112078"
    assert len(doc.ents) == 3
    assert doc.ents[0].label_.startswith("HABITAT")
    assert doc.ents[1].label_.startswith("SPECIES")
    assert doc.ents[1][0]._.canonical == ammonia_id
    assert doc.ents[2].label_.startswith("LOCATION")
    assert doc.ents[2][0]._.canonical == 1652821


def test_no_ner():
    doc = pipeline.nlp("A fox jumped over the lazy dog")
    assert len(doc.ents) == 0


def test_genus_abbreviation():
    lice_id = "urn:lsid:marinespecies.org:taxname:519279"
    doc = pipeline.nlp("Within the fish's gill, P. bulbovaginatus")
    assert len(doc.ents) == 1
    assert doc.ents[0][0]._.canonical == lice_id
