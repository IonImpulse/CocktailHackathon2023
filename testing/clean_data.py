import csv
import json

def openCSVFileAsJSON(filename):
    # Open CSV file, read it, and return it as a JSON object with the first row as the keys
    # return as a list of dictionaries
    with open(filename, 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        keys = next(reader)
        data = [dict(zip(keys, map(str, row))) for row in reader]
        return data


if __name__ == "__main__":
    drinks = []

    all_drinks = openCSVFileAsJSON('data/raw/all_drinks.csv')
    hotaling_cocktails = openCSVFileAsJSON('data/raw/hotaling_cocktails.csv')


    # All drinks has strDrink, strIngredient{1-15}, strMeasure{1-15}
    # Convert to a list of dictionaries with keys: name, ingredients, 
    # with ingredients being a list of dictionaries with keys: name, amount
    for drink in all_drinks:
        ingredients = []
        for i in range(1, 16):
            ingredient = drink['strIngredient' + str(i)]
            amount = drink['strMeasure' + str(i)]
            if ingredient:
                ingredients.append({'name': ingredient.strip(), 'amount': amount.strip()})
        drinks.append({'name': drink['strDrink'], 'ingredients': ingredients})

    
    # Hotaling cocktails has "Cocktail Name", "Ingredients", and "Garnish"
    # We have to look for the ingredients in the ingredients list, with the amounts split 
    # by ‘oz’, ‘dash’, ‘bsp’, ‘drops’, 'tsp', 'dash', 'cups', 'cup', 'sprigs', 'bottles'. The ingredients list is separated by a comma.
    # The garnish is also split by a comma, but no amount is given, so we just put "1" for each.

    amounts = ['oz', 'dash', 'bsp', 'drops', 'tsp', 'dash', 'cups', 'cup', 'sprigs', 'bottles']

    for drink in hotaling_cocktails:
        ingredients = []
        for ingredient in drink['Ingredients'].split(','):
            ingredient = ingredient.strip()
            if ingredient:
                amount = '1'
                for a in amounts:
                    if a in ingredient:
                        # Amount is "number amount_type", eg "1.4 oz"
                        amount = f"{ingredient.split(a)[0].strip()} {a}"
                        ingredient = ingredient.split(a)[1].strip()
                        break

                # Look to see if the first char of the first word in the ingredient is a number, and if so, remove it
                try :
                    if ingredient.split(' ')[0][0].isdigit():
                        ingredient = ' '.join(ingredient.split(' ')[1:])
                except:
                    print(ingredient)
                    pass

                ingredients.append({'name': ingredient.strip(), 'amount': amount.strip()})
        drinks.append({'name': drink['Cocktail Name'], 'ingredients': ingredients})

    # Write the drinks to a JSON file, in write/create mode
    with open('data/drinks.json', 'w+') as f:
        json.dump(drinks, f, indent=4)
