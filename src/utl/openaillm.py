from openai import OpenAI
import os


class OpenAIClient:
    def __init__(self, model: str = "gpt-3.5-turbo",):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        self.model = model

    def send_prompt(self, prompt: str, context: str = '', max_tokens: int = 1200):
        """
        Send a prompt and optional context to the OpenAI API and return the response.

        :param prompt: The main prompt to send to the API.
        :param context: Additional context or system message to send with the prompt.
        :param model: The model to use for generating the response.
        :param max_tokens: The maximum number of tokens to generate in the response.
        :return: The response from the OpenAI API.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)