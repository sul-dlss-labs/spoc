"""Species Entity Recogition Pipeline"""

import pandas as pd
import spacy

from spacy.language import Language
from spacy_lookup import Entity

species = pd.read_json('../data/species.json')
locations = pd.read_json('../data/locations.json')
habitats = pd.read_json('../data/habitats.json')

species_dict = dict(zip(species.taxonID, species.scientificName))
location_dict = dict(zip(locations.FEATURE_ID, locations.FEATURE_NAME))
for row in [species_dict, location_dict]:
    for key, val in row.items():
        row[key] = [val,]

@Language.factory(name='species_entity')
def create_species_entity(nlp: Language, name: str):
    return Entity(name=name, keywords_dict=species_dict, label='SPECIES')

@Language.factory(name='location_entity')
def create_location_entity(nlp: Language, name: str):
    return Entity(name=name, keywords_dict=location_dict, label='LOCATION')

@Language.factory(name='habitat_entity')
def create_habitat_entity(nlp: Language, name: str):
    return Entity(name=name, keywords_list=list(habitats.Habitat), label='HABITAT')

nlp = spacy.load('en_core_web_md')
nlp.add_pipe('species_entity')
nlp.add_pipe('location_entity')
nlp.add_pipe('habitat_entity')
nlp.remove_pipe("ner")
