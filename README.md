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
