import os
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    wait_fixed,
)  # for exponential backoff

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

@retry(wait=wait_fixed(2))
def completion_with_backoff(**kwargs):
    print("Trying")
    return openai.ChatCompletion.create(**kwargs)

def do_get_best_noun(nouns, prompt) -> str:
    # create the prompt
    # gpt_prompt = "Give a one word response to fill in the blank in the following sentence with one of the following options: "
    gpt_prompt = "Give a one word response to fill in the blank using only one of these options: "
    # for i in nouns:
    #     gpt_prompt = gpt_prompt + " " + i + ","
    gpt_prompt += ", ".join(nouns)
    gpt_prompt += f". The {prompt} was located on the _."
    # openai gpt-4
    message = [{"role": "user", "content": gpt_prompt}]
    response = completion_with_backoff(
            model="gpt-4",
            messages=message,
            temperature=0.2,
            max_tokens=1000,
            frequency_penalty=0.0
    )

    # best noun
    return response['choices'][0]['message']['content']

# testing
if __name__ == "__main__":
    nouns = {"floor":1, "desk":2, "table":3, "computer":4, "chair":5}
    prompt = "cake"

    best_noun = do_get_best_noun(nouns, prompt)
    print(best_noun)
