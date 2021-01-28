import streamlit as st

rejected, skipped, verified = 0,0,0

paper = { 'title': 'Sample', 'date': 'Date', 'abstract': 'A Sample abstract'}
institution = 'Stanford'

f'''
# You have verified { verified } rejected { rejected } skipped { skipped }

## { paper.get('title') }
## { paper.get('date') }
## { institution }

### Generated Abstract
{ paper.get('abstract') }
'''

next = st.sidebar.markdown("## NEXT >")
