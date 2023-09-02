import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = "org-YYUFrsvmL5WjuUJhZJXqcM3l"  # personal
openai.api_key = os.getenv("OPENAI_API_KEY")

model = os.getenv("OPENAI_CHAT_MODEL")


def ChatCompletion(messages):
    try:
        completion = openai.ChatCompletion.create(model=model, messages=messages)
        return completion.choices[0].message
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e}")
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"OpenAI API request failed to connect: {e}")
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request was invalid: {e}")
    except openai.error.AuthenticationError as e:
        print(f"OpenAI API request was not authorized: {e}")
    except openai.error.PermissionError as e:
        print(f"OpenAI API request was not permitted: {e}")
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")


def ImageCreation(prompt):
    try:
        response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
        return response.data[0].url
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e}")
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"OpenAI API request failed to connect: {e}")
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request was invalid: {e}")
    except openai.error.AuthenticationError as e:
        print(f"OpenAI API request was not authorized: {e}")
    except openai.error.PermissionError as e:
        print(f"OpenAI API request was not permitted: {e}")
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")


def ImageEdit(image, mask, prompt):
    try:
        response = openai.Image.create_edit(
            image=image, mask=mask, prompt=prompt, n=1, size="1024x1024"
        )
        return response.data[0].url
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e}")
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"OpenAI API request failed to connect: {e}")
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request was invalid: {e}")
    except openai.error.AuthenticationError as e:
        print(f"OpenAI API request was not authorized: {e}")
    except openai.error.PermissionError as e:
        print(f"OpenAI API request was not permitted: {e}")
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")


def ImageVariation(image):
    try:
        response = openai.Image.create_variation(image=image, n=1, size="1024x1024")
        return response.data[0].url
    except openai.error.Timeout as e:
        print(f"OpenAI API request timed out: {e}")
    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"OpenAI API request failed to connect: {e}")
    except openai.error.InvalidRequestError as e:
        print(f"OpenAI API request was invalid: {e}")
    except openai.error.AuthenticationError as e:
        print(f"OpenAI API request was not authorized: {e}")
    except openai.error.PermissionError as e:
        print(f"OpenAI API request was not permitted: {e}")
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
