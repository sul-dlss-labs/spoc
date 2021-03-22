import pandas as pd  # type: ignore
import streamlit as st  # type: ignore

import streamlit.components.v1 as components  # type: ignore
from jinja2 import Template

st.set_page_config(page_title="SPOC Verifier", layout="wide")

with open("src/apps/components/action_button.html") as fo:
    action_template = Template(fo.read())

main_col, geo_col, action_col = st.beta_columns([2, 1, 0.5])

species = pd.read_json("data/species-records.json")

with main_col:
    """
    # SPOC Verifier
    """
    st.dataframe(species)

with geo_col:
    """
    # A-A03
    [PLACE]

    """

with action_col:
    components.html(action_template.render(status="select"), height=75, width=65)
