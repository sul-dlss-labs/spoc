<<<<<<< HEAD
import os
import sys
=======
import folium  # type: ignore
>>>>>>> Support for simple Folium Map with Location entities set as markers
import pandas as pd  # type: ignore
import requests
import streamlit as st  # type: ignore
from st_aggrid import AgGrid, DataReturnMode, GridOptionsBuilder  # type: ignore
from st_aggrid import GridUpdateMode  # type: ignore
from streamlit_folium import folium_static  # type: ignore

import streamlit.components.v1 as components  # type: ignore
from jinja2 import Template

ROOT_PATH = os.path.abspath(".")
sys.path.append(ROOT_PATH)
from config.base import settings  # type: ignore # noqa: E402

st.set_page_config(page_title="SPOC Verifier", layout="wide")

with open("src/apps/components/action_button.html") as fo:
    action_template = Template(fo.read())

with open("src/apps/components/entities_area.html") as fo:
    entities_template = Template(fo.read())

main_col, geo_col, action_col = st.beta_columns([2, 1, 0.5])

species = pd.read_json("data/species-records.json")

grid_options = GridOptionsBuilder.from_dataframe(species)

# Grid options
grid_options.configure_selection("single", use_checkbox=True)
grid_options.configure_pagination(paginationAutoPageSize=True)


with main_col:
    """
    # SPOC Verifier
    """
    records_grid = AgGrid(
        species,
        gridOptions=grid_options.build(),
        data_return_mode=DataReturnMode.FILTERED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
    )
    selected = records_grid["selected_rows"]

with geo_col:
    if len(selected) > 0:
        f"""
        ## {selected[0]['Species']}

        """
        div_url = f"{settings.api_url}/api/div/?paper_id={selected_df['Paper ID'][0]}&div_num={selected_df['div_enum'][0]}"
        result = requests.get(div_url)
        entities_html = entities_template.render(content=result.json().get("html"))
        components.html(entities_html, height=500, scrolling=True)


with action_col:
    action_html = action_template.render(status="select")
    components.html(action_html, height=75, width=65)

if len(selected) > 0:
    """
    ## Places
    """
    geo_request = requests.get(f"/api/coordinates/?places={selected[0]['Place']}")
    geo_result = geo_request.json()
    m = folium.Map(
        location=[geo_result["lat_mean"], geo_result["long_mean"]], zoom_start=7
    )
    for place in geo_result["markers"]:
        folium.Marker(
            [place["latitude"], place["longitude"]],
            popup=place["label"],
            tooltip=place["label"],
        ).add_to(m)
    folium_static(m)
