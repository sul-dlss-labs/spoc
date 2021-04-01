# TAXA March 2021

import streamlit as st  # type: ignore
from PIL import Image  # type: ignore

from session import get_state  # type: ignore


image = Image.open("src/apps/image/TAXA.png")

colophon = st.beta_container()

state = get_state()

with colophon:
    st.image(
        image,
        caption="Help discover species occurrences hiding in library collections.",
    )

    st.write("# Help discover species hiding in library collections.")

    st.write(
        """The Stanford Libraries AI group is training computers to recognize
           species occurrence data in digitized student papers. By verifying the
           genus-species, the time, and location, you can help check the
           computers' work and improve the model."""
    )
    start_btn = st.button("GET STARTED")
    if start_btn is not None:
        state.seen_splash = True
