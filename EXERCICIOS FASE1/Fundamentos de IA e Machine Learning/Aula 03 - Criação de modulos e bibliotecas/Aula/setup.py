from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='investimentopy',
    version='1.0.1',
    packages=find_packages(),
    description='Uma biblioteca para análise de investimentos',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
