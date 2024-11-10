from setuptools import setup, find_packages

# for encoding
from codecs import open
from os import path

WORKING_DIR = path.abspath(path.dirname(__file__))

with open(path.join(WORKING_DIR, 'README.md'), encoding='utf-8') as f:
    readme_docs = f.read()

# This call to setup() does all the work
setup(
    name="simple_calculator",
    version="0.1.0",
    description="Example simple calculator",
    long_description=readme_docs,
    long_description_content_type="text/markdown",
    url="https://fun-with-python-example-simple-calculator.readthedocs.io/en/latest/",
    author="Hubert Piotrowski",
    author_email="example@email-foo.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["simple_calculator"],
    include_package_data=True,
    install_requires=["pytest"]
)