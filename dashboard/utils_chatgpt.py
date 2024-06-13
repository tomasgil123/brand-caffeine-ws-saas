from openai import OpenAI

from dashboard.utils import (read_md_file, get_text_between_comments)

class OpenaiInsights():
    def __init__(self):
        self.client = OpenAI()

    # ask_question method returns a string
    def generate_insights(self, data):

        prompts = read_md_file("./dashboard/prompts.md")

        selected_prompt = get_text_between_comments(prompts, data['prompt_name'], "<!")

        selected_prompt = selected_prompt.replace("{brand}", data['brand_name'])

        try:
            delimiter = "####"
            
            messages =  [  
                {'role':'system', 
                'content': selected_prompt},    
                {'role':'user', 
                'content': f"{delimiter}{data['string_data']}{delimiter}"},  
            ]
            response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
                temperature=0, 
                max_tokens=1000, 
            )
            
            return response.choices[0].message.content.strip()
        except Exception as err:
            print(err)