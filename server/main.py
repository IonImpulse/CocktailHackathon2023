import networkx as nx
import json
import random
import openai
import config

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, HTTPException, Request

openai.organization = "org-d9J851UTnhskutiYjlc1UV2U"
openai.api_key = config.OPEN_AI_KEY
MODEL = "text-davinci-003"
SSL_CERT_PRIVKEY = "/etc/letsencrypt/live/overflow.bar/privkey.pem"
SSL_CERT_PERMKEY = "/etc/letsencrypt/live/overflow.bar/fullchain.pem"

app = FastAPI()

graph = nx.read_gexf('ingredient_graph.gexf')

def generate_drink_from_ingredient(ingredient_name, graph, num_ingredients=3):
    ingredients = sorted(graph[ingredient_name].items(), key=lambda x: x[1]['weight'], reverse=True)[:10]
    least_likely_ingredients = sorted(graph[ingredient_name].items(), key=lambda x: x[1]['weight'])[:10]

    ingredients = []

    for i in range(num_ingredients):
        ingredient = random.choice(least_likely_ingredients)[0]

        while ingredient in [i[0] for i in ingredients]:
            ingredient = random.choice(least_likely_ingredients)[0]

        ingredients.append((ingredient, graph[ingredient_name][ingredient]))

    return ingredients

@app.get("/api/v1/generate_drink/{base_ingredient}/{num_ingredients}")
async def generate_drink(base_ingredient: str, num_ingredients: int):
    drink_ingredients = generate_drink_from_ingredient(base_ingredient, graph, num_ingredients)

    for i in range(5):
        response = openai.Completion.create(
            engine=MODEL,
            prompt=f"Ingredients: {base_ingredient}, {', '.join([i[0] for i in drink_ingredients])}\n\nReturn a JSON formatted object with amounts for each ingredient, how to prepare it, the type of glass used to hold the drink, and a clever, unique name for the drink. The JSON keys are \"name\", \"glass\", \"instructions\", and \"ingredients\", with ingredients being a dictionary with ingredient names as keys and amounts as values.\n",
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )

        generated_text = response.choices[0].text.strip()

        try:
            drink = json.loads(generated_text)
            print(drink)
            break
        except Exception as e:
            print(e)
            if i == 4:
                raise HTTPException(status_code=500, detail="Failed to generate drink")
            continue

    response = openai.Image.create(
        prompt=f"A drink with {base_ingredient}, {', '.join([i[0] for i in drink_ingredients])} in a {drink['glass']} with instructions: {drink['instructions']}"
    )

    url = response.data[0].url
    drink["url"] = url

    return drink

app.mount("/", StaticFiles(directory="../website", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    import sys

    # Print routes
    print(app.routes)

    # mount static files
    if "--prod" in sys.argv:
        # Production mode
        # Add redirect from http to https
        from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
        app.add_middleware(HTTPSRedirectMiddleware)

        # Add SSL
        from starlette.middleware import Middleware
        from starlette.middleware.trustedhost import TrustedHostMiddleware
        from starlette.middleware.gzip import GZipMiddleware
        from starlette.middleware.cors import CORSMiddleware

        middleware = [
            Middleware(TrustedHostMiddleware, allowed_hosts=["overflow.bar"]),
            Middleware(GZipMiddleware, minimum_size=1000),
            Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        ]

        for m in middleware:
            app.add_middleware(m)

        uvicorn.run("main:app", host="0.0.0.0", port=443, log_level="info", reload=False,
                    workers=16, ssl_keyfile=SSL_CERT_PRIVKEY, ssl_certfile=SSL_CERT_PERMKEY)
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=5000,
                    log_level="info", reload=True)