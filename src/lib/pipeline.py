"""Species Entity Recogition Pipeline"""

import os
import pathlib
import pandas as pd  # type: ignore
import spacy  # type: ignore

from spacy.language import Language  # type: ignore
from spacy_lookup import Entity  # type: ignore

data = pathlib.Path(os.path.abspath(os.path.join("data")))

species = pd.read_json(data / "species.json")
locations = pd.read_json(data / "locations.json")
habitats = pd.read_json(data / "habitats.json")

species_dict = dict(zip(species.taxonID, species.scientificName))
for key, val in species_dict.items():
    values = [
        val,
    ]
    terms = val.split()
    if len(terms) == 2:
        values.append(f"{terms[0][0]}. {terms[1]}")
    species_dict[key] = values
location_dict = dict(zip(locations.FEATURE_ID, locations.FEATURE_NAME))
for key, val in location_dict.items():
    location_dict[key] = [
        val,
    ]


@Language.factory(name="species_entity")
def create_species_entity(nlp: Language, name: str):
    return Entity(name=name, keywords_dict=species_dict, label="SPECIES")


@Language.factory(name="location_entity")
def create_location_entity(nlp: Language, name: str):
    return Entity(name=name, keywords_dict=location_dict, label="LOCATION")


@Language.factory(name="habitat_entity")
def create_habitat_entity(nlp: Language, name: str):
    habitats_list = list(habitats.Habitat)
    return Entity(name=name, keywords_list=habitats_list, label="HABITAT")


nlp = spacy.load("en_core_web_md")
nlp.add_pipe("species_entity")
nlp.add_pipe("location_entity")
nlp.add_pipe("habitat_entity")
nlp.remove_pipe("ner")
