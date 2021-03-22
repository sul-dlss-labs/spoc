FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache -r requirements.txt

RUN python -m spacy download en_core_web_sm

EXPOSE 8501

CMD streamlit run src/apps/spoc_verifier.py
