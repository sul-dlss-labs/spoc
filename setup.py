import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="SPOC Verifier",
    version="0.0.1",
    license="LICENSE.md",
    long_description=read("README.md"),
    setup_requires=["pytest-runner"],
    # test_suite="test",
    tests_require=["pytest"],
)
