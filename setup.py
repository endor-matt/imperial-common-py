from setuptools import setup, find_packages

setup(
    name="imperial-common",
    version="1.0.0",
    description="Shared utilities for Death Star Operations Platform",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.20.0",
        "pyyaml>=5.0",
        "lxml>=4.9.0",
        "pycryptodome>=3.9.0",
    ],
)
