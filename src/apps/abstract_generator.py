import pathlib
import pandas as pd  # type: ignore
import streamlit as st  # type: ignore
import streamlit.components.v1 as components  # type: ignore
from jinja2 import Template

with open("src/apps/components/action_button.html") as fo:
    action_template = Template(fo.read())

st.set_page_config(page_title="Abstract Generator")

rejected, skipped, verified = 0, 0, 0


papers = pd.read_json("data/papers.json")
full_text = pathlib.Path("data/full_text")
paper = papers.sample()


main_col, action_col = st.beta_columns([2, 0.5])

with main_col:
    f"""
    # Abstract Generator
    ## You have verified { verified } rejected { rejected } skipped { skipped }

    ### { paper['Title'].iloc[0] }
    by { paper['Author'].iloc[0] }
    ### { paper['Year'].iloc[0] }
    ### { paper['Institution'].iloc[0] }

    ### Generated Abstract

    """
    if st.button("Open pdf"):
        st.stop()
#         paper_text = full_text/paper['filename'].iloc[0]
#         st.text(paper_text.read_text())

with action_col:
    st.button("Next >")
    components.html(
        action_template.render(status=paper["status"].iloc[0]), height=75, width=65
    )
