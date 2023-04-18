API_ENDPOINT = "api/v1/generate_drink/"

var state = {
  base_ingredient: null,
  num_extra: 1,
}

/*
Return data from the API endpoint
Format:
{
  "name": "South of the Border Strike",
  "glass": "highball",
  "instructions": "Fill a highball glass with ice cubes. Squeeze in the juice of one lemon, add 1 tablespoon of olive brine, top with 4 ounces Sprite, and finish with a dash of Tabasco sauce. Stir to combine.",
  "ingredients": {
    "lemon": 1,
    "olive brine": 1,
    "sprite": 4,
    "tabasco sauce": "dash"
  },
  "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-d9J851UTnhskutiYjlc1UV2U/user-trxGvJ2OaftgNCgOITnvSvyZ/img-AcYvt8rV45FwNGQPw4rOhP0n.png?st=2023-04-17T07%3A34%3A29Z&se=2023-04-17T09%3A34%3A29Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-04-17T05%3A15%3A08Z&ske=2023-04-18T05%3A15%3A08Z&sks=b&skv=2021-08-06&sig=Z%2B/zOAw9KdIop48L26BnXrmhn2MOkd9%2By8XiSd8Y9II%3D"
}
*/
async function getDrink(base_ingredient, num_extra) {
  let response = await fetch(API_ENDPOINT + base_ingredient + "/" + num_extra);
  let data = await response.json();
  return data;
}

async function generateDrink() {
  const drink = await getDrink(state.base_ingredient, state.num_extra);

  document.getElementById("drink-image").src = drink.url;
  document.getElementById("drink-name").innerHTML = drink.name;
  let glass = drink.glass;

  if (!glass.includes("glass")) {
    glass += " glass";
  }

  document.getElementById("drink-glass").innerHTML = `Served in a ${glass}`;
  document.getElementById("drink-ingredients").innerHTML = Object.keys(
    drink.ingredients
  ).map((key) => {
    return `${key.toUpperCase()}`
  }).join(", ");

  document.getElementById("drink-instructions").innerHTML = drink.instructions;

  setStep(4);
  
}

function hideFader() {
  document.getElementById("fader").classList.add("slide-out");
  setTimeout(function () {
    document.getElementById("fader").style.display = "none";
  }, 900);
}

function generateButtons() {
  let step1 = document.getElementById("step1");
  let step2 = document.getElementById("step2");

  let step1_buttons = step1.getElementsByClassName("button-container")[0];
  let step2_buttons = step2.getElementsByClassName("button-container")[0];

  let randomized = BASE_INGREDIENTS.sort(() => Math.random() - 0.5);

  for (let i = 0; i < randomized.length; i++) {
    let button = document.createElement("button");
    button.classList.add("button");
    button.classList.add("base-ingredient");
    button.innerHTML = randomized[i].toUpperCase();
    button.addEventListener("click", function () {
      state.base_ingredient = randomized[i];
      setStep(2);
    });
    step1_buttons.appendChild(button);
  }

  const NUM_EXTRA_TEXT = [
    "BIT SIZED",
    "BASIC",
    "BYTE SIZED",
    "COMPLEX",
    "FULL STACK",
  ];

  for (let i = 1; i <= 5; i++) {
    let button = document.createElement("button");
    button.classList.add("button");
    button.classList.add("num-extra");
    button.innerHTML = NUM_EXTRA_TEXT[i - 1];
    button.addEventListener("click", function () {
      state.num_extra = i;
      setStep(3);
      generateDrink();
    });
    step2_buttons.appendChild(button);
  }
}

function setStep(step) {
  let steps = document.getElementsByClassName("step");
  for (let i = 0; i < steps.length; i++) {
    steps[i].classList.remove("slide-in");
    steps[i].classList.remove("slide-out");

    steps[i].classList.add("slide-out");

    setTimeout(function () {
      steps[i].classList.add("hidden");
    }, 900);

      
    if (i == step - 1) {
      setTimeout(function () {
        steps[i].classList.remove("slide-out");
        steps[i].classList.remove("hidden");
        steps[i].classList.add("slide-in");
      }, 900);
    }
  }
}

function repeatContent(el, till) {
  let html = el.innerHTML;
  let counter = 0; // prevents infinite loop

  while (el.offsetWidth < till && counter < 50) {
    el.innerHTML += html;
    counter += 1;
  }
}

function setupScroller() {
  let outer = document.querySelector("#outer");
  let content = outer.querySelector('#content');

  repeatContent(content, outer.offsetWidth);

  let el = outer.querySelector('#loop');
  el.innerHTML = el.innerHTML + el.innerHTML;
}

setInterval(function () {
  document.getElementById("loading-text").innerHTML = LOADING_MSGS[
    Math.floor(Math.random() * LOADING_MSGS.length)
  ];
}, 1000);

setupScroller();
generateButtons();