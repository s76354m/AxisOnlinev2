from setuptools import setup, find_packages

setup(
    name="axisonline",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "numpy",
    ],
) 