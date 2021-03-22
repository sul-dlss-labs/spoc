from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# This should be cached
all_records = pd.read_json("data/species-records.json")


class Record(BaseModel):
    paper_id: str
    species_id: str
    species: Optional[str] = None
    time: Optional[str] = None
    place: Optional[str] = None
    div_enum: Optional[int] = None


app = FastAPI()


@app.get("/papers/{paper_id}")
async def get_paper_records(paper_id: str):
    # Returns all of the records associated with a paper
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
    return {"id": paper_id, "records": records.to_dict(orient='records')}


@app.get("/records/")
async def get_record(paper_id: str, species_id: str):
    record = all_records[
        all_records["Paper ID"].isin([paper_id])
        & all_records["Species ID"].isin([species_id])
    ]
    if len(record) < 1:
        msg = f"Record for {paper_id} and species ID {species_id} not found"
        raise HTTPException(status_code=404, detail=msg)
    return record


@app.put("/records/")
async def update_record(record: Record):
    return record


@app.delete("/records/")
async def delete_record(record: Record):
    return {"message": f"{record.paper_id} {record.species_id} deleted"}


@app.get("/")
async def root():
    return {"message": "SPOC Endpoint"}
