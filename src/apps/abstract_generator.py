import pathlib
import pandas as pd
import streamlit as st
from components import action_button

rejected, skipped, verified = 0,0,0

papers = pd.read_json("data/papers.json")
full_text = pathlib.Path("data/full_text")
paper = papers.sample()


f'''
# You have verified { verified } rejected { rejected } skipped { skipped }

### { paper['title'].iloc[0] }
### { paper['date'].iloc[0] }
### { paper['institution'].iloc[0] }

### Generated Abstract

'''

next = st.sidebar.markdown("## NEXT >")

if st.button('Open pdf'):
    st.text("Loads pdf")
