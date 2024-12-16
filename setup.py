from setuptools import setup, find_packages

setup(
    name="company_data_agency",
    version="0.1.0",
    description="A multi-agent system for retrieving and presenting company information",
    author="Your Name",
    packages=find_packages(include=["company_data_agency", "company_data_agency.*"]),
    install_requires=[
        "duckduckgo-search>=4.1.1",
        "mysql-connector-python>=8.0.33",
        "python-dotenv>=1.0.0",
        "tabulate>=0.9.0",
        "pydantic>=2.0.0",
        "groq>=0.4.2",
        "aiohttp>=3.8.0"
    ],
    python_requires=">=3.8",
) 