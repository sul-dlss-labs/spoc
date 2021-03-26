import os
import pathlib
import sys


from typing import Optional

import pandas as pd  # type: ignore
import lxml.etree as etree  # type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ..lib.pipeline import nlp  # type: ignore
from ..lib.etl import TEI, enrich_entities  # type: ignore

sys.path.append(os.path.abspath(os.path.join("..", "config")))
from config.base import settings  # type: ignore # noqa: E402

xml_path = pathlib.Path(settings.papers_tei)

data = pathlib.Path(os.path.abspath(os.path.join("data")))

# This should be cached
all_records = pd.read_json(data / "species-records.json")
locations = pd.read_json(data / "locations.json")


class Record(BaseModel):
    paper_id: str
    species_id: str
    species: Optional[str] = None
    time: Optional[str] = None
    place: Optional[str] = None
    div_enum: Optional[int] = None


app = FastAPI()


@app.get("/api/coordinates")
async def get_location_coordinates(places: str):
    places = eval(places)
    if len(places) < 1:
        return {}
    place_idents = [r[0] for r in places]
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
async def get_div_html(paper_id: str, div_num: int):
    """
    Returns entity-tagged HTML for an XML div element

    :param paper_id: Name of the TEI-XML file
    :param div_enum: Index of DIV in the TEI-XML body
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
    enriched_html = enrich_entities(doc, paper_id)
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


@app.get("/api/")
async def root():
    return {"message": "SPOC Endpoint"}
