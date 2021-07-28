# Methods Planner
## NER

Description|Input|Action|Output|Notes
-----|-----|-----|-----|-----|-----
Assemble student paper metadata|various csv files|align and collate|csv file |Metadata is used in the Streamlit app (title, year, location, etc.)
Convert PDFs to text segment divs via Grobid*|papers, pdf|transformation|tei-xml|The div size and formation is set to defaults. This can be modified.
*not strictly neccessary unless we want to use GROBID to remove references
Gather Species names from GNRD|papers, pdf|identifying, extracting terms|dataframe|Verified species names, taxonomic classification, verification source title (eg. "Catalog of Life")
Gather species identifiers and other info|lists of terms, dataframe|query, extract info|dataframe|**may not be necessary for SPOC goals, but nice to build out knowledge graph
Gather location names from multiple sources|list of terms, csv files|prune and collate|csv files|Amanda produced separate files for CA, OR, WA approx 15 cols each
Extract only 4 columns of location data|csv files|combine and filter|json|Feature_name, Feature_ID, Primary Lat and Primary Lon. See notebook
Gather a list of habitats|COPIOUS set, txt files|collate|jsonl|See Phase 1 Work doc, used the training corpus provided in COPIOUS, *.ann files
Get a list of habitat terms|jsonl|extract|json|See notebook
Create spaCy Pipline|json files|construct model|spaCy model|This model will need to be trained
Apply pipeline to the divs|tei-xml|run entity recognition|json|The entities are understood by direct match only
Make data available via Streamlit|json|visualize|html|taxa.stanford.edu !
Enable accept/reject/add entities for training data|html|human decision|sql lite|Interface defines decision points and directs the human work
Employ training data|sql lite|training|spaCy model
