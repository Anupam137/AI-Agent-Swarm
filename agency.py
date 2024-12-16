import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from company_data_agency.custom_agency import CustomAgency
from company_data_agency.web_search_agent.web_search_agent import WebSearchAgent
from company_data_agency.database_agent.database_agent import DatabaseAgent
from company_data_agency.data_presenter_agent.data_presenter_agent import DataPresenterAgent

def main():
    # Initialize agents
    web_search = WebSearchAgent()
    db_search = DatabaseAgent()
    presenter = DataPresenterAgent()

    # Create the agency with communication flows
    agency = CustomAgency(
        agents=[web_search, db_search, presenter],
        communication_flows=[
            [web_search, presenter],  # Web search can communicate with presenter
            [db_search, presenter],   # Database can communicate with presenter
        ],
        shared_instructions="company_data_agency/agency_manifesto.md"
    )

    print("\nCompany Data Agency Demo")
    print("------------------------")
    print("Enter a company name to search for its contact information.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            company_name = input("Enter company name: ").strip()
            if company_name.lower() == 'exit':
                break

            if not company_name:
                print("Please enter a company name.")
                continue

            # Process the company name through the agency
            result = agency.run_sync(company_name)
            print("\nResult:", result)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()