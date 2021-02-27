import datetime
import pandas as pd
import streamlit as st

import streamlit.components.v1 as components
from jinja2 import Template

st.set_page_config(page_title="SPOC Verifier", layout="wide")

with open("src/apps/components/action_button.html") as fo:
    action_template = Template(fo.read())

main_col, geo_col, action_col = st.beta_columns([2, 1, 0.5])

species = pd.DataFrame(
    [
        {
            "Paper ID": "A",
            "Instance ID": "A02",
            "Species - Genus": None,
            "Time": None,
            "Place": None,
        },
        {
            "Paper ID": "A",
            "Instance ID": "A03",
            "Species - Genus": "Tonicella lineata",
            "Time": "1982",
            "Place": "Grimes Point",
        },
        {
            "Paper ID": "B",
            "Instance ID": "B01",
            "Species - Genus": None,
            "Time": None,
            "Place": None,
        },
    ]
)

with main_col:
    f"""
    # SPOC Verifier
    """
    st.dataframe(species)

with geo_col:
    f"""
    # A-A03
    [PLACE]

    """

with action_col:

    components.html(action_template.render(status="select"), height=75, width=65)
