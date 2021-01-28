import datetime
import pandas as pd
import streamlit as st

papers = pd.DataFrame([{ 'Paper ID': 'A',
                         'Instance ID': 'A02',
                         'Species - Genus': None,
                         'Time': None,
                         'Place': None },
                       { 'Paper ID': 'A',
                         'Instance ID': 'A03',
                         'Species - Genus': 'Tonicella lineata',
                         'Time': '1982',
                         'Place': 'Grimes Point' },
                        { 'Paper ID': 'B',
                          'Instance ID': 'B01',
                          'Species - Genus': None,
                           'Time': None,
                           'Place': None}])

f'''
# SPOC Verifier
'''

st.dataframe(papers)
