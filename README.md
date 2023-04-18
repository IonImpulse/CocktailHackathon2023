# OVERFLOW.BAR

# Pipeline:

## 1. Data Cleaning
Takes data from all_drinks.csv and hotaling_cocktails.csv and cleans it to be used in the next step.
All drinks already has ingredients seperated from amounts, but hotaling_cocktails does not.
We can use ‘oz’, ‘dash’, ‘bsp’, ‘drops’ as measurements to seperate the ingredients from the amounts.

Format is as follows:
```
{
    "name": "name of drink",
    "ingredients": [
        {
            "name": "name of ingredient",
            "amount": "amount of ingredient"
        },
        ...
    ],
    "instructions": "instructions for drink"
}
```

## 2. Data Analysis
We now can vectorize the ingredients and use a clustering algorithm to cluster the drinks into groups.
We can then use a classification algorithm to classify a new drink into one of the groups.
Additionally, we can cluster the ingredients into groups and determine which ingredients work well together.
From this, we can create novel drinks by combining ingredients from different groups that theoretically should work well together, but have not been tried before.

## 3. OpenAI Integration
Now that we have our ingredients for our novel drinks, we can use OpenAI to generate a name and instructions for the drink.
We call OpenAI's API, using davinci-003 as the model, and pass in the ingredients as the prompt.
We specify that the response should be JSON formatted, and keep retrying until it's valid JSON.
Usually it works the first time, but sometimes it returns some invalid JSON, so we have to retry.
After we get a valid response, we parse the JSON, and call DALL-E to generate an image for the drink.
Once we have everything we need, we can return the drink to the user.

## 4. Web App
Using FastAPI as our server and Nginx as our reverse proxy, we can serve a simple webapp, hosted at https://overflow.bar.