"""ETL for SPOC Papers"""
import spacy  # type: ignore
import pandas as pd  # type: ignore
import lxml.etree as etree  # type: ignore

from typing import Any, Dict, List

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
