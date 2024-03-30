# AI Bug Report Generator

This project provides a user-friendly interface to generate bug reports using a large language model (LLM). Users can describe the steps to reproduce an issue and the expected results, and the LLM will craft a detailed bug report incorporating these details.

## Requirements

This project requires the following Python libraries:
- python-dotenv
- streamlit
- langchain-google-genai
- pinecone-client
- scikit-learn

## Project Structure

The project consists of three main Python scripts:

* **chatbot.py:** This script handles the Streamlit user interface and interacts with other scripts to process user input and generate bug reports.
* **generate_bug_report.py:** This script defines the core logic for processing user input, querying Pinecone for similar issues, and using the LLM to create the bug report.
* **vectorizer.py:** This script handles vectorizing user input for searching similar issues within Pinecone.

## Functionality Overview

1. **User Input:** Users describe the steps to reproduce a bug and the expected results through a Streamlit interface.
2. **Vectorization and Search:** The user input is vectorized and used to query Pinecone for similar bug reports (if available).
3. **LLM Prompt Generation:** Based on user input and potentially retrieved similar issues, a prompt is crafted to guide the LLM in generating the bug report.
4. **Bug Report Generation:** The LLM utilizes the provided prompt to generate a comprehensive bug report describing the issue and potential solutions.
5. **Additional Information:** The generated report includes a template for users to add details about their test environment and any relevant screenshots or recordings.

## Running the Project

1. Install the required libraries using `pip install -r requirements.txt`.
2. Set up your Google and Pinecone accounts and obtain the necessary API keys.
3. Create a `.env` file in the project directory and store your API keys as the example in `.env.example`.
4. Ensure you have a Pinecone index created and populated with relevant bug report data (title, description, steps to reproduce, expected results) with appropriate metadata fields.
5. Run the Streamlit app using `streamlit run src/chatbot.py`.
6. To run with production mode options, use below command:
  ```
  streamlit run src/chatbot.py --client.toolbarMode=minimal
  ```

## Additional Notes

* This is a basic example, and the Pinecone integration can be further customized to match your specific data schema and indexing needs.
* Consider error handling and user feedback mechanisms for a more robust user experience.