# Company Data Agency

A multi-agent system for retrieving and presenting company information from multiple sources.

## Project Structure

```
company_data_agency/
├── core/                      # Core agent and agency classes
│   ├── custom_agent.py       # Base agent class
│   └── custom_agency.py      # Agency orchestration
├── config/                   # Configuration files
│   ├── .env                  # Environment variables
│   └── agency_manifesto.md   # Agency instructions
├── utils/                    # Utility functions
│   ├── database.py          # Database operations
│   ├── web_search.py        # Web search operations
│   └── data_presentation.py # Data formatting
├── tests/                    # Test files
│   └── test_db.py           # Database connection test
├── agents/                   # Individual agents
│   ├── web_search_agent/    # Web search agent
│   ├── database_agent/      # Database agent
│   └── data_presenter_agent/# Data presenter agent
├── setup.py                 # Package setup
└── requirements.txt         # Dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `config/.env`:
   ```
   MYSQL_HOST=your_host
   MYSQL_USER=your_user
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=your_database
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

Run the agency:
```bash
python company_data_agency/agency.py
```

Enter a company name when prompted, and the agency will:
1. Search for company information on the web
2. Search in the database
3. Present combined results in a table format

## Development

- Core functionality is in the `core` directory
- Add new utility functions in the `utils` directory
- Configuration files are in the `config` directory
- Tests are in the `tests` directory

## Requirements

- Python 3.8+
- MySQL database
- Groq API key
- Required Python packages listed in requirements.txt 