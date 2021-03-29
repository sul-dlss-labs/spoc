"""ETL for SPOC Papers"""
import os
import pathlib
import sqlite3
import sys

import spacy  # type: ignore
from spacy import displacy  # type: ignore
import pandas as pd  # type: ignore
import lxml.etree as etree  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from typing import Any, Dict, List

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)

from config.base import settings  # type: ignore # noqa: E402

root_path = pathlib.Path(ROOT_PATH)
xml_path = pathlib.Path(settings.papers_tei)

TEI = {"tei": "http://www.tei-c.org/ns/1.0"}


def get_date(xml_doc: etree.Element) -> str:
    """Extracts Publication Date if it exists"""
    pub_date_element = xml_doc.find(
        "tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date",
        namespaces=TEI,  # noqa: E501
    )
    if pub_date_element is not None:
        pub_date = pub_date_element.attrib.get("when", "")
    else:
        pub_date = ""
    return pub_date


def get_entities(doc: spacy.tokens.Doc) -> tuple:
    """Iterate through document's entities and add to lists"""
    species, places, habitats = [], [], []

    def __add_ent__(entity):
        record_info = [
            (token._.canonical, token._.entity_desc) for token in entity
        ]  # noqa: E501
        if entity.label_.startswith("SPECIES"):
            species.extend(record_info)
        elif entity.label_.startswith("LOCATION"):
            places.extend(record_info)
        elif entity.label_.startswith("HABITAT"):
            habitats.extend([rec[0] for rec in record_info])

    for ent in doc.ents:
        __add_ent__(ent)

    # TODO: Check doc._.overlap and add to lists

    # Removes duplicates from species, locations, and habitats
    species = list(set(species))
    locations = list(set(places))
    habitats = list(set(habitats))
    return species, locations, habitats


def enrich_entities(
    doc: spacy.Language, paper_id: str, div_number: int, species_id: str
) -> str:
    """
    Enriches entities from the spaCy's displacy with clickable
    actions

    :param doc: spaCy Doc
    :param paper_id: Paper ID
    :param div_number: Index of div
    :param species_id: Taxon ID of Species
    """

    def __generate_button__(mark_element, title, reject):
        entity = mark_element.contents[0].strip()
        span = mark_element.find("span")
        button = ner_soup.new_tag("button")
        button.string = title
        button["onclick"] = f"verify(event, {reject})"
        button["style"] = "width: 16px"
        button["data-paper_id"] = paper_id
        button["data-entity_id"] = ent_lookup[entity]
        button["data-label"] = span.string
        button["data-div_number"] = div_number
        button["data-species_id"] = species_id
        button["data-api_url"] = settings.api_url
        return button

    options = {
        "colors": {"LOCATION": "#92c1e1", "SPECIES": "#f8a359", "HABITAT": "#c0b58b"}
    }
    ner_html = displacy.render(doc, style="ent", options=options)
    # Revese look-up value of enties
    ent_lookup = {}
    for ent in doc.ents:
        for token in ent:
            if ent.text in ent_lookup:
                continue
            ent_lookup[ent.text] = token._.canonical
    ner_soup = BeautifulSoup(ner_html, "html.parser")
    # Finds all Entities, creates verified and rejected buttons
    marks = ner_soup.find_all("mark")
    for mark in marks:
        verified_btn = __generate_button__(mark, "+", 0)
        mark.append(verified_btn)
        rejected_btn = __generate_button__(mark, "-", 1)
        mark.append(rejected_btn)
    return ner_soup.prettify()


def process_div(
    div: etree.Element,
    nlp: spacy.lang,
    paper_name: str,
    publication_date: str,
    div_number: int,
) -> List[Dict[Any, Any]]:
    """Process XML div using spaCy NLP pipeline"""
    text = ""
    for row in div.itertext():
        text += f" {row}"
    doc = nlp(text)
    gbif = "https://www.gbif.org/species/search?q={0}&qField=SCIENTIFIC"
    species, locations, habitats = get_entities(doc)
    records = []
    for row in species:
        records.append(
            {
                "Paper ID": paper_name,
                "Instance ID": row[0],
                "Species": row[1],
                "GBIF": gbif.format(row[1]),
                "Time": publication_date,
                "Place": locations,
                "Habitats": habitats,
                "div_enum": div_number,
            }
        )
    return records


def process_xml(raw_xml: str, filename: str, nlp: spacy.lang) -> list:
    """Processes raw TEI XML and returns a list of records. Currently
    called by the data-prep.ipynb Jupyter notebook"""
    # Create an XML document from xml path
    tei_xml = etree.XML(raw_xml)
    publication_date = get_date(tei_xml)
    divs = tei_xml.findall("tei:text/tei:body/tei:div", namespaces=TEI)
    records = []
    for i, div in enumerate(divs):
        records.extend(
            process_div(div, nlp, filename, publication_date, i + 1)
        )  # noqa: E501
    return pd.DataFrame(records)


def save_occurrence(
    paper_id: str,
    species_id: str,
    ip_addr: str,
    label: str,
    div_number: str = None,
    identifier: str = None,
    rejected: int = 0,
) -> int:
    """Function takes data and creates a species occurrence result"""

    def __get_or_add__(table_name: str, var_name: str, value: Any) -> int:
        cur.execute(f"SELECT id FROM {table_name} WHERE {var_name}=?", (value,))
        result = cur.fetchone()
        if result is None:
            cur.execute(f"INSERT INTO {table_name} ({var_name}) VALUES (?)", (value,))
            cur.execute(f"SELECT max(id) FROM {table_name}")
            result = cur.fetchone()
        return result[0]

    con = sqlite3.connect(xml_path / "species-results.sqlite")
    cur = con.cursor()
    # Retrieves paper, ip address, and species ID
    paper_db_id = __get_or_add__("Papers", "filename", paper_id)
    ip_addr_id = __get_or_add__("IPAddresses", "address", ip_addr)
    species_db_id = __get_or_add__("Species", "taxon_id", species_id)
    # First checks if occurrence already exists, assumes paper_id, species_id,
    # and div_number make up an unique key
    cur.execute(
        """SELECT id FROM Occurrences
                   WHERE paper_id=? AND species_id=? AND div_number=?""",
        (paper_db_id, species_db_id, div_number),
    )
    occurrence_result = cur.fetchone()
    if occurrence_result is None:
        cur.execute(
            "INSERT INTO Occurrences (paper_id, species_id, div_number) VALUES (?,?,?)",
            (paper_db_id, species_db_id, div_number),
        )
        occurrence_id = cur.lastrowid
    else:
        occurrence_id = occurrence_result[0]
    cur.execute(
        """INSERT INTO OccurrenceEntity (occurrence_id, ip_addr_id, rejected)
                   VALUES (?,?,?)""",
        (occurrence_id, ip_addr_id, rejected),
    )
    occurrence_entity_id = cur.lastrowid
    # Updates Occurrence Entity table for non-Species entities
    if identifier is not None:
        if label.startswith("LOCATION"):
            entity_db_id = __get_or_add__("Locations", "external_id", identifier)
            entity_field = "location_id"
        if label.startswith("HABITAT") and identifier is not None:
            entity_db_id = __get_or_add__("Habitats", "name", identifier)
            entity_field = "habitat_id"
        if label.startswith("SPECIES"):
            entity_db_id = __get_or_add__("Species", "taxon_id", identifier)
            entity_field = "species_id"
        cur.execute(
            f"UPDATE OccurrenceEntity SET {entity_field}=? WHERE id=?",
            (entity_db_id, occurrence_entity_id),
        )
    con.commit()
    con.close()
    return True
