import os
from gradio_client import Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def gen_papergpt_response(input):
    client = Client("https://mslab-papergpt.hf.space/")
    result = client.predict(input, api_key, fn_index=0)

    return result
