import streamlit.components.v1 as components  # type: ignore
from jinja2 import Template

with open("src/apps/components/action_button.html") as fo:
    button_template = Template(fo.read())

components.html(button_template.render(state=None), height=64)
