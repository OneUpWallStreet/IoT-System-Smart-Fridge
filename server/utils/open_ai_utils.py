
from openai import OpenAI




api_key = 'openai_api_key_here'

def get_recipe(fridge_items):

    client = OpenAI(api_key=api_key)


    #friddge_items = ['apple','egg','butter','ground beef','peppers']
    item_str = ', '.join(fridge_items)


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that takes a list of food items in the fridge and provides recipes for those items. Please send the result in Markdown format.
                            You can use items from the fridge as well as common items used for cooking. Respond with detailed instructions for a recipe using the following items:"""
            },
            {
                "role": "user",
                "content": item_str
            }
        ]
    )
    #print(response.choices[0].message.content)
    
    return response.choices[0].message.content


def get_shopping_list(fridge_items):
    client = OpenAI(api_key=api_key)

    item_str = ', '.join(fridge_items)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that suggests a grocery store shopping list based on similar items to what the users already has or that would complement
                                the items the user has. Return a neat list format. Return at least 10 items and include fruit, vegetables, meat, dairy, and snacks. The user has the following items:"""
            },
            {
                "role": "user",
                "content": item_str
            }
        ]
    )
    return response.choices[0].message.content




