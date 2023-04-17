import json
import csv
import networkx as nx

if __name__ == "__main__":
    # Open data/drinks.json, read it, and return it as a JSON object
    with open('data/drinks.json', 'r', encoding="utf8") as f:
        drinks = json.load(f)

    # Json file is a list of dictionaries with keys: name, ingredients,
    # where ingredients is a list of dictionaries with keys: name, amount

    # Create a list of all ingredients, counting the number of times each ingredient is used
    ingredients = {}
    for drink in drinks:
        for ingredient in drink['ingredients']:
            name = ingredient['name'].lower()
            if name in ingredients:
                ingredients[name] += 1
            else:
                ingredients[name] = 1

    # Sort the ingredients by the number of times they are used
    ingredients = sorted(ingredients.items(), key=lambda x: x[1], reverse=True)

    # Create a graph of the ingredients
    # Edges are the likelihood of the two ingredients being used together
    # Additionally, we want to link ingredients that never appear together to each other
    # We do this by creating a node for each ingredient, and then creating an edge between each ingredient and the "None" node
    # This way, we can find the most likely ingredient to be used with an ingredient that has never been used before
    G = nx.Graph()

    # Add all ingredients as nodes
    for ingredient in ingredients:
        G.add_node(ingredient[0])

    # Add edges between ingredients
    for drink in drinks:
        for i in range(len(drink['ingredients'])):
            for j in range(i + 1, len(drink['ingredients'])):
                ingredient1 = drink['ingredients'][i]['name'].lower()
                ingredient2 = drink['ingredients'][j]['name'].lower()
                if G.has_edge(ingredient1, ingredient2):
                    G[ingredient1][ingredient2]['weight'] += 1
                else:
                    G.add_edge(ingredient1, ingredient2, weight=1)

    # Add edges between ingredients and the "None" node
    for ingredient in ingredients:
        if G.has_edge(ingredient[0], 'None'):
            G[ingredient[0]]['None']['weight'] += 1
        else:
            G.add_edge(ingredient[0], 'None', weight=1)

    # Print top 50 ingredients in JS array format
    print("var top_ingredients = [")
    for ingredient in ingredients[:50]:
        print("    \"" + ingredient[0] + "\",")
    print("];")


    # Save the graph as a json file
    with open('data/ingredient_graph.json', 'w') as f:
        json.dump(nx.readwrite.json_graph.node_link_data(G), f)

    # Save graph as gexf file
    nx.write_gexf(G, "data/ingredient_graph.gexf")