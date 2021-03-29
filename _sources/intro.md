Welcome to the Species Occurrences (SPOC) project
==============================================

This project is based on a collection at [Harold A. Miller Marine Biology Library at Hopkins Marine Station](https://library.stanford.edu/hopkins), part of [Stanford Libraries](https://library.stanford.edu). 

Species Occurrence records are foundational to understanding biodiversity in ecosystems and help researchers track adaptation and the effects of climate change. Knowledge bases that gather observations from around the world including species, location and time of the event provide a more complete picture of historical and geographic changes in biodiversity. Not surprisingly, observations from the past recorded on paper are often missing from these knowledge bases because they are hard to come by. Libraries up and down the Pacific coast hold collections of undergraduate student papers with observations of marine plants and animals “hidden” in the text. Reading and extracting those observations by hand is an effort libraries cannot afford to undertake. 

The goal of this project is to employ natural language processing, machine learning, and data visualization to amplify the work of librarians in identifying and verifying these observations. 

There are four key steps to the effort:
1. Extract scientifically relevant entities from the corpus
* Species occurrences (taxon/species + location (lat/lon) + date)
* Keywords: most distinctive words, most frequent words, perhaps other entity sets TBD
* Location(s) (named; “Hopkins Beach”, “Fisherman’s Cove”)
* Habitat type(s) (e.g., “subtidal”)
2. Link these entities to authorities and draw information into the app from those sources to provide context for validation.
3. Visualize the data spatially and temporally as part of validation. Where are observations located? What year? 
4. Serve the metadata to relevant aggregators, e.g., the Global Biodiversity Information Facility | GBIF. 

This is where we will document our efforts and share outcomes. 
