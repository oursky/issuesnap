import os
from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from vectorizer import find_closest_samples

# Configuration (Load environment variables)
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)


def process_user_input(user_steps, expected_results):

    samples = find_closest_samples(user_steps, expected_results)

    # Send custom prompt if similar issue is found
    if len(samples) > 0:

        prompt = """You are a software QA tester. By given steps to reproduce and expected behaviours of a bug issue, you return write a good issue title and description for the issue to report. Use simple and short sentences. Use similar format and punctuations. Wrap your result in code snippet.

  Given steps to reproduce:
  {user_steps}

  Given expected behaviours:
  {expected_results}

  Below are some examples of bug report:
  """.format(user_steps=user_steps, expected_results=expected_results)

        for sample in samples:
            prompt += f"{sample}"

        # Generate bug report using LLM
        response = llm.invoke(prompt)
        response.content += f"\nDon’t forget to include your test environment details, as well as any screenshots or screen recordings, when submitting your issue.🚀\n"
        response.content += """
  Below is a template for test environment information:
  ```
  ## Environment:
  - Environment: UAT
  - Platform: 
  - Build version: 
  - Browser: 
  - Device (OS version): 
  - Test account: 
  ```
  """
        response.content += f"\nHappy Testing!🌟"

        print(prompt)

        return response.content
    else:
        # Send a general prompt if no similar issue is found
        prompt = f"The user reported encountering a bug. Steps to reproduce:\n{user_steps}\nExpected Results:\n{expected_results}\n"
        prompt += "Can you generate a detailed bug report describing the issue and potential solutions?"

        response = llm.invoke(prompt)

        print(prompt)

        return response.content
