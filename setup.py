from setuptools import setup, find_packages

setup(
    name="SwarmV2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'plotly',
        'sqlalchemy',
        'pyodbc',
        'pydantic',
        'python-dotenv'
    ]
) 