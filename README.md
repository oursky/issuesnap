# IssueSnap

This project provides a user-friendly interface to generate bug reports using a large language model (LLM). Users can describe the steps to reproduce an issue and the expected results, and the LLM will craft a detailed bug report incorporating these details.

## Requirements

This project requires the following Python3 libraries:
- streamlit
- pinecone-client
- langchain-google-genai
- python-dotenv
- pandas

## Project Structure

* **IssueSnap.py:** Main script to start and run the web tool
* **generate_bug_report.py:** Functional script to define the core logic for processing user input, querying Pinecone for similar issues, and using the LLM to create the bug report.
* **closest_sample_finder.py:** Functional script to vectorize user input for searching similar issues within Pinecone.
* **upsert_csv_to_pinecone.py:** Standalone script that vectorizes source csv data for upserting to Pinecone database.

## Functionality Overview

1. **User Input:** Users describe the steps to reproduce a bug and the expected results through a Streamlit interface.
2. **Vectorization and Search:** The user input is vectorized and used to query Pinecone for similar bug reports (if available).
3. **LLM Prompt Generation:** Based on user input and potentially retrieved similar issues, a prompt is crafted to guide the LLM in generating the bug report.
4. **Bug Report Generation:** The LLM utilizes the provided prompt to generate a comprehensive bug report describing the issue and potential solutions.

## Running the Project

### Set Up Environment

1. Navigate to the project directory:
   ```
   cd your-work-directory/issuesnap
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv env
   source env/bin/activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Google and Pinecone accounts and obtain the necessary API keys.
5. Create a `.env` file in the project directory and store your API keys as the example in `.env.example`.
6. Ensure you have a Pinecone index created and populated with relevant bug report data (title, description, steps to reproduce, expected results) with appropriate metadata fields.

### Start the Web Tool on Local

1. Launch without hiding debug options:
   ```
   streamlit run src/IssueSnap.py
   ```

2. Launch with production mode options:
   ```
   streamlit run src/IssueSnap.py --client.toolbarMode=minimal
   ```

### Deployment

For deployment details, please see the [README](https://github.com/oursky/issuesnap/blob/main/deployment_templates/README.md) in folder `deployment_templates`.