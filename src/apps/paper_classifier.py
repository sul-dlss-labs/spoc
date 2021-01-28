import datetime
import pathlib
import pandas as pd
import streamlit as st

papers = pd.read_json("data/papers.json")
full_text = pathlib.Path("data/full_text")
paper = papers.sample()

rejected, skipped, verified = 0,0,0

f'''
# Paper Classifier - Observation or not?

### { paper['title'].iloc[0] }
### { paper['date'].iloc[0] }
### { paper['institution'].iloc[0] }

## Paper Abstract

## Load more document text
'''

if st.button('Open pdf'):
    paper_text = full_text/paper['filename'].iloc[0]
    st.text(paper_text.read_text())

next = st.sidebar.markdown("## NEXT >")
