[![SPOC application CI](https://github.com/sul-dlss-labs/spoc/actions/workflows/spoc-app.yml/badge.svg)](https://github.com/sul-dlss-labs/spoc/actions/workflows/spoc-app.yml)

# Stanford Species Occurrences
This project provides a Streamlit application that provides record-level verification of individual
student reports for training and validation purposes as well publishing the records for inclusion
in [Global Biodiversity Information Facility][GBIF].

## Development
We recommend using a Python virtual environment to install SPOC's package dependencies. SPOC is
currently developed with [Python 3.9](https://www.python.org/downloads/) and above.

### Setup
1. Create a new virtual environment `python3 -m venv spoc-env`
1. Activate (on POSIX systems) `source spoc-env/bin/activate`
1. Clone the current SPOC Git repository `git clone https://github.com/sul-dlss-labs/spoc.git`
1. Enter directory and install dependencies, `cd spoc && pip install -r requirements.txt`  

## Documentation
The SPOC project uses Jupyter [Book](https://jupyterbook.org/) and [notebooks](https://jupyter.org/)
for documenting the workflows, project, data, models, and technology. The book
is available through Github pages at https://sul-dlss-labs.github.io/spoc/.

To build the latest documentation for this project:

`jupyter-book build doc/`

Publish the documentation to Github pages

`ghp-import -n -p -f doc/_build/html`

### Setting up SSL using LetsEncrypt
On the AWS EC2 instance, follow the instructions for installing and configuring [certbot][CERTBOT].
For step 7, just get the certificate only using `sudo certbot --standalone -d taxa.stanford.edu certonly`
To renew the cert, stop the SPOC containers and run `sudo certbot renew --dry-run`, and again without the --dry-run flag to actually renew.
Make sure the key files are copied into the config folder before starting the containers:
```
sudo cp /etc/letsencrypt/live/taxa.stanford.edu/fullchain.pem ./config/
sudo cp /etc/letsencrypt/live/taxa.stanford.edu/privkey.pem ./config/
```

### Testing
The SPOC project uses Python types with [mypy][MYPY], linting with [Flake8][FLK8], and [Black][BLK]
for Python code formatting. Unit tests use the [pytest][PYTST] and can be run
with `pytest test/` from the root directory.

[Cypress][CYPRESS] is used for end-to-end integration testing.

## Deployment and CI/CD
The publicly available [Streamlit][STRMLIT] application is hosted on AWS.


[BLK]: https://black.readthedocs.io/en/stable/
[CYPRESS]: https://www.cypress.io/
[FLK8]: https://flake8.pycqa.org/en/latest/
[GBIF]: https://www.gbif.org/
[MYPY]: https://mypy.readthedocs.io/en/stable/
[PYTST]: https://docs.pytest.org/en/stable/
[STRMLIT]: https://www.streamlit.io/
[CERTBOT]:https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx
