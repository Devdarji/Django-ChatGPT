import openai
import ast

from django.conf import settings as dj_settings
from quiz import constants as quiz_constants

OPENAI_TOKEN = dj_settings.OPENAI_TOKEN
openai.api_key = OPENAI_TOKEN

openai.Model.list()


PROMPT = quiz_constants.PROMPT.format(lang="Python", level="Easy", topic="Python List")


response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=PROMPT,
    temperature=0,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)


# Parse the Response
response = response["choices"][0]["text"]

start_index = response.index("[")
end_index = response.rindex("]")

response = ast.literal_eval(response[start_index : end_index + 1])

quiz_instances = []

# Save the Instance in Database
for r in response:
    print("1", r.get("question"))
    print("2", r.get("option_a"))
    print("3", r.get("option_b"))
    print("4", r.get("option_c"))
    print("5", r.get("option_d"))
    print("6", r.get("code", ""))
    print("7", r.get("correct_answer", r.get("answer", "")))
