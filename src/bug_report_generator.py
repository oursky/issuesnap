import logging
import os
from dotenv import load_dotenv
from langchain_google_genai import (
	ChatGoogleGenerativeAI,
	HarmBlockThreshold,
	HarmCategory,
)
from closest_sample_finder import find_closest_samples

# Configure logging (optional, adjust log level and output as needed)
logging.basicConfig(level=logging.INFO,
					format='%(asctime)s - %(levelname)s - %(message)s')


def check_api_key():
	load_dotenv()
	google_api_key = os.getenv("GOOGLE_API_KEY")
	if not google_api_key:
		raise KeyError("GOOGLE_API_KEY")


def init_llm():
	try:
		load_dotenv()
		google_api_key = os.getenv("GOOGLE_API_KEY")
		# Initialize LLM model
		llm = ChatGoogleGenerativeAI(
			model="gemini-2.0-flash",
			safety_settings={
				HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
				HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
				HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
				HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
			},
		)
		return llm
	except Exception as e:
		logging.error(f"bug_report_generator.py: Error initializing LLM: {e}")
		raise


def split_response(content):
	try:
		content_split = content.split("Issue Title:")[1].split("Issue Body:")
		title = content_split[0].strip("*").strip("`").strip()
		body = content_split[1].strip("*").strip("`").strip()
		return title, body
	except Exception as e:
		logging.error(f"bug_report_generator.py: Error parsing response: {e}")


def process_user_input(user_steps, expected_results, test_env):

	llm = init_llm()
	samples = []

	try:
		samples = find_closest_samples(user_steps, expected_results)
	except Exception as e:
		logging.error(
			f"bug_report_generator.py: Error finding closest samples: {e}")

	try:
		# Send custom prompt
		prompt = """You are a software QA tester. The user reported encountering a bug.
Steps to reproduce:
{user_steps}
Expected Results:
{expected_results}

Taking reference of the examples below, can you generate a bug report describting the issue, steps to reproduce and expected results?
Use simple and short sentences. Use similar format and punctuations.

Below are some examples of bug report:
""".format(user_steps=user_steps, expected_results=expected_results)

		for sample in samples:
			prompt += f"{sample}"

		# Generate custom bug report using LLM
		response = llm.invoke(prompt)
		title, body = split_response(response.content)

		report = f"\nIssue Title\n```\n"
		report += title
		report += f"\n```\n"
		report += f"\nIssue Body\n```\n"
		report += body
		report += f"\n\n## Environment:\n"
		report += test_env
		report += f"\n```\n"
		report += f"📎 Attachments\n\n"
		report += f"Don’t forget to include any **screenshots** 📲 or **screen recordings** 🎥 when submitting your issue!"
		return report
	except Exception as e:
		logging.error(
			f"bug_report_generator.py: Error generating bug report: {e}")
		raise
