import pandas as pd  # type: ignore
import requests
import streamlit as st  # type: ignore
from st_aggrid import AgGrid, DataReturnMode, GridOptionsBuilder  # type: ignore
from st_aggrid import GridUpdateMode  # type: ignore
import streamlit.components.v1 as components  # type: ignore
from jinja2 import Template

st.set_page_config(page_title="SPOC Verifier", layout="wide")

with open("src/apps/components/action_button.html") as fo:
    action_template = Template(fo.read())

main_col, geo_col, action_col = st.beta_columns([1, 1, 0.5])

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
selected_df = pd.DataFrame(selected)

with geo_col:
    if not selected_df.empty:
        f"""
        ## {selected_df['Species'][0]}

        """
        div_url = f"/api/div/?paper_id={selected_df['Paper ID'][0]}&div_num={selected_df['div_enum'][0]}"
        result = requests.get(div_url)
        st.write(result.json().get('html'), unsafe_allow_html=True)
        """
        ## Places
        """
        for place in selected_df["Place"]:
            place = eval(place)
            if len(place) > 0:
                f"[{place[0][1]}]({place[0][0]})"

with action_col:
    action_html = action_template.render(status="select")
    components.html(action_html, height=75, width=65)
