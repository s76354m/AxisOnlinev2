from setuptools import setup, find_packages

setup(
    name="axis-program-management",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        "pandas",
        "sqlalchemy",
        "pyodbc",
    ],
) 