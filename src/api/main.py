import os
import pathlib
import re
import sys

from typing import Any, Optional

import pandas as pd  # type: ignore
import lxml.etree as etree  # type: ignore
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..lib.pipeline import nlp  # type: ignore
from ..lib.etl import TEI, enrich_entities, save_occurrence  # type: ignore

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)


from config.base import settings  # type: ignore # noqa: E402

xml_path = pathlib.Path(settings.papers_tei)

data = pathlib.Path(os.path.abspath(os.path.join("data")))

# This should be cached
all_records = pd.read_json(data / "species-records.json")
locations = pd.read_json(data / "locations.json")

places_re = re.compile(r"\[*\[(\d+)")


class Record(BaseModel):
    paper_id: str
    species_id: str
    species: Optional[str] = None
    time: Optional[str] = None
    place: Optional[str] = None
    div_enum: Optional[int] = None


app = FastAPI()

origins = ["https://taxa.stanford.edu", "http://taxa.stanford.edu"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/coordinates")
async def get_location_coordinates(places: str):
    places = places_re.findall(places)  # type: ignore
    if len(places) < 1:
        return {}
    place_idents = [int(r) for r in places]
    result = locations[locations["FEATURE_ID"].isin(place_idents)]
    output = {
        "lat_mean": result["LATITUDE"].mean(),
        "long_mean": result["LONGITUDE"].mean(),
        "markers": [],
    }
    for row in result.iterrows():
        output["markers"].append(
            {
                "latitude": row[1]["LATITUDE"],
                "longitude": row[1]["LONGITUDE"],
                "label": f"{row[1]['FEATURE_NAME']}, {row[1]['STATE']}",
            }
        )
    return output


@app.get("/api/div/")
async def get_div_html(paper_id: str, div_num: int, species_id: str):
    """
    Returns entity-tagged HTML for an XML div element

    :param paper_id: Name of the TEI-XML file
    :param div_enum: Index of DIV in the TEI-XML body
    :param species_id: Taxon ID for the species
    """
    if paper_id.endswith(".xml"):
        paper_path = xml_path / paper_id
    else:
        paper_path = xml_path / f"{paper_id}.tei.xml"
    if not paper_path.exists():
        msg = f"Cannot find {paper_id} XML"
        raise HTTPException(status_code=404, detail=msg)
    tei_xml = etree.XML(paper_path.read_bytes())
    div = tei_xml.find(f"tei:text/tei:body/tei:div[{div_num}]", namespaces=TEI)
    if div is None:
        raise HTTPException(
            status_code=404, detail=f"{paper_id} with div {div_num} not found"
        )
    text = ""
    for row in div.itertext():
        text += f" {row}"
    doc = nlp(text)
    enriched_html = enrich_entities(doc, paper_id, div_num, species_id)
    return {"html": enriched_html}


@app.get("/api/papers/{paper_id}")
async def get_paper_records(paper_id: str):
    """
    Returns all of the records associated with a paper

    :param paper_id: Name of the TEI-XML file
    """
    paper_filename = f"{paper_id}.tei.xml"
    records = all_records[
        all_records["Paper ID"].isin(
            [
                paper_filename,
            ]
        )
    ]
    if len(records) < 1:
        raise HTTPException(status_code=404, detail=f"{paper_id} not found")
    return {"id": paper_id, "records": records.to_dict(orient="records")}


@app.get("/api/records/")
async def get_record(paper_id: str, species_id: str):
    """
    Returns all species records for a paper and a species

    :param paper_id: Name of the TEI-XML file
    :param species_id: Identifier for the species
    """
    record = all_records[
        all_records["Paper ID"].isin([paper_id])
        & all_records["Species ID"].isin([species_id])
    ]
    if len(record) < 1:
        msg = f"Record for {paper_id} and species ID {species_id} not found"
        raise HTTPException(status_code=404, detail=msg)
    return record


@app.put("/api/records/")
async def update_record(record: Record):
    return record


@app.delete("/api/records/")
async def delete_record(record: Record):
    return {"message": f"{record.paper_id} {record.species_id} deleted"}


class Occurrence(BaseModel):
    species_id: str
    paper_id: str
    entity_id: Any
    label: str
    rejected: bool = False
    div_number: Optional[int] = None


@app.post("/api/verify")
async def verify_occurrence(occurrence: Occurrence, request: Request):
    result = save_occurrence(
        occurrence.paper_id,
        occurrence.species_id,
        request.client.host,
        occurrence.label,
        occurrence.div_number,
        occurrence.entity_id,
        occurrence.rejected,
    )
    return {"occurrence_id": result}


@app.get("/api/")
async def root():
    return {"message": "SPOC Endpoint"}
