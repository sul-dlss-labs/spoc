import os
import streamlit as st
import streamlit.components.v1 as components
from jinja2 import Template

with open("src/apps/components/action_button.html") as fo:
    button_template = Template(fo.read())

components.html(button_template.render(state=None), height=64)
