# Stanford Species Occurrences


## Development
We recommend using a Python virtual environment to install SPOC's package dependencies. SPOC is 
currently developed with [Python 3.9](https://www.python.org/downloads/) and above. 

### Setup
1. Create a new virtual environment `python -m venv spoc-env`
1. Activate (on POSIX systems) `source spoc-env/bin/activate`
1. Clone the current SPOC Git repository `git clone https://github.com/sul-dlss-labs/spoc.git`
1. Enter directory and install dependencies, `cd spoc && pip install -r requirements.txt`  

### Testing
The SPOC project uses Python types with [mypy][MYPY], linting with [Flake8][FLK8], and [Black][BLK]
for Python code formatting. Unit tests use the standard Python `unittest` and can be run 
with `python setup.py test` in the root directory. 

[Cypress][CYPRESS] is used for end-to-end integration testing.

## Deployment and CI/CD
The publicly available [Streamlit][STRMLIT] application is hosted on AWS. 

## Streamlit SPOC Verifier Application

[BLK]: https://black.readthedocs.io/en/stable/
[CYPRESS]: https://www.cypress.io/
[FLK8]: https://flake8.pycqa.org/en/latest/
[MYPY]: https://mypy.readthedocs.io/en/stable/
[STRMLIT]: https://www.streamlit.io/
