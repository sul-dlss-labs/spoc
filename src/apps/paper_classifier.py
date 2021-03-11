import pathlib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from jinja2 import Template

st.set_page_config(page_title="Paper Classifier")

with open("src/apps/components/action_button.html") as fo:
    action_template = Template(fo.read())

papers = pd.read_json("data/papers.json")
full_text = pathlib.Path("data/full_text")
paper = papers.sample()


main_col, action_col = st.beta_columns([2, 0.5])

with main_col:
    f"""
    # Paper Classifier - Observation or not?

    ### { paper['Title'].iloc[0] }
    ### { paper['Year'].iloc[0] }
    ### { paper['Institution'].iloc[0] }

    ## Paper Abstract

    ## Load more document text
    """

    if st.button("Open pdf"):
        paper_text = full_text / paper["filename"].iloc[0]
        st.text(paper_text.read_text())

with action_col:
    next = st.button("NEXT >")
    components.html(
        action_template.render(status=paper["status"].iloc[0]),
        height=75,
        width=65
    )
