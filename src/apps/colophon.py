# TAXA March 2021

import streamlit as st
import base64
from PIL import Image


#st.set_page_config(layout="wide")


#image = Image.open('image/TAXA.png')

TAXA_LOGO = "image/TAXA.png"
colophon = st.beta_container()

#st.image(image, caption="Help discover species occurrences hiding in library collections.")

with colophon:


    st.markdown(
        f"""
        <div class="container">
            <img class="taxa-logo" src="data:image/png;base64,{base64.b64encode(open(TAXA_LOGO, "rb").read()).decode()}">
            </div>
            """,
            unsafe_allow_html=True
            )


    st.write('# Help discover species hiding in library collections.')

    st.write("The Stanford Libraries AI group is training computers to recognize species occurrence data in digitized student papers. By verifying the genus-species, the time, and location, you can help check the computers' work and improve the model.")
    st.button("GET STARTED")
    st.markdown("---")
    st.markdown("To learn more about this project see the [Project Book for TAXA](https://library-ai.stanford.edu) or go directly to the [code repository](https://library-ai.stanford.edu). To learn more about all AI projects at Stanford Libraries, visit [library-ai.stanford.edu](https://library-ai.stanford.edu)")

    




