import networkx as nx
import json
import random
import os
import openai
import config
openai.organization = "org-d9J851UTnhskutiYjlc1UV2U"
openai.api_key = config.OPEN_AI_KEY

# use latest davinci model
MODEL = "text-davinci-003"

def generate_drink_from_ingredient(ingredient_name, graph, num_ingredients=3):
    # Get the 10 most likely ingredients to be used with the given ingredient
    ingredients = sorted(graph[ingredient_name].items(), key=lambda x: x[1]['weight'], reverse=True)[:10]

    # Get the 10 least likely ingredients to be used with the given ingredient
    # This is used to make sure that the drink is not too similar to the given ingredient
    least_likely_ingredients = sorted(graph[ingredient_name].items(), key=lambda x: x[1]['weight'])[:10]

    ingredients = []

    for i in range(num_ingredients):
        # Randomly select an ingredient from the 10 least likely ingredients
        ingredient = random.choice(least_likely_ingredients)[0]

        while ingredient in [i[0] for i in ingredients]:
            # If the randomly selected ingredient is in the 10 most likely ingredients, keep randomly selecting ingredients
            ingredient = random.choice(least_likely_ingredients)[0]

        # Add the randomly selected ingredient to the list of ingredients
        ingredients.append((ingredient, graph[ingredient_name][ingredient]))

    return ingredients

if __name__ == "__main__":
    # load gexf file
    graph = nx.read_gexf('data/ingredient_graph.gexf')

    user_input = input('Enter an ingredient: ')
    drink = generate_drink_from_ingredient(user_input, graph)

    # Using the drink ingredients, use GPT4 to generate a drink recipe
    # with specified ingredients, generating amounts, instruction, type of glass, and name
    response = openai.Completion.create(
        engine=MODEL,
        prompt=f"Ingredients: {user_input}, {', '.join([i[0] for i in drink])}\n\nReturn a JSON formatted object with amounts for each ingredient, how to prepare it, the type of glass used to hold the drink, and a clever, unique name for the drink. The JSON keys are \"name\", \"glass\", \"instructions\", and \"ingredients\", with ingredients being a dictionary with ingredient names as keys and amounts as values.\n",
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )

    generated_text = response.choices[0].text.strip()

    try:
        # Try to parse the generated text as JSON
        drink = json.loads(generated_text)
        print(drink)
    except:
        # If the generated text is not JSON, print the generated text
        exit(generated_text)

    # Now, with the generated drink, we can use DALL-E to generate an image of the drink
    # Prompt is:
    # "A drink with {ingredient1}, {ingredient2}, and {ingredient3} in a {glass} with instructions: {instructions}"
    # The image is saved to the images folder
    response = openai.Image.create(
        prompt=f"A drink with {user_input}, {', '.join([i[0] for i in drink])} in a {drink['glass']} with instructions: {drink['instructions']}"
    )

    url = response.data[0].url

    drink.url = url
    