FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y git

RUN pip install --no-cache -r requirements.txt

RUN python -m spacy download en_core_web_sm

EXPOSE 8501

CMD streamlit run --server.address 0.0.0.0 src/apps/spoc_verifier.py
