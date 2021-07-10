from flask import Flask, jsonify, render_template, request
import requests
import random

app = Flask(__name__)

def dados(cidade):
    
    apikey = "c868145961df12d120df69d7c5b2a564"

    request_weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={apikey}&units=metric&lang=pt_br")

    weather_status = request_weather.status_code
    if weather_status == 404:
        cidade_valida = 0
        return "Cidade inválida."
    else:
        cidade_valida = 1

    if cidade_valida != 0:
        weather_data = request_weather.json()
                
        weather_main = weather_data["weather"][0]["main"]

        temperatura = weather_data['main']['temp']
        
        if weather_main not in ["Rain", "Thunderstorm", "Drizzle"] :
            chovendo = 0
        else:
            chovendo = 1

    return {
            "temperatura": temperatura,
            "chovendo": chovendo
    }

def pokemon(type):
    request_pokemon = requests.get (f"https://pokeapi.co/api/v2/type/{type}")
    
    pokemon_data = request_pokemon.json()
    
    poke = pokemon_data["pokemon"]
    
    sorteio = random.choice(poke)

    pokemon_nome = sorteio["pokemon"]["name"]

    pokemon_url = sorteio["pokemon"]["url"]

    a = requests.get(pokemon_url)

    imagem = a.json()["sprites"]["front_default"]

    return {
        "name": pokemon_nome,
        "sprite": imagem
    }


def rules(cidade):
    data = dados(cidade)
    temperatura = data["temperatura"]
    chovendo = data["chovendo"]
    
    if chovendo == 1:
        data_poke = pokemon('electric')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Elétrico",
            "sprite": f"{data_poke['sprite']}"
        
        }

    elif temperatura < 5:
        data_poke = pokemon('ice')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Gelo",
            "sprite": f"{data_poke['sprite']}"
                                
        }

    elif temperatura >= 5 and temperatura < 10:
        data_poke = pokemon('water')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Água",
            "sprite": f"{data_poke['sprite']}"
                                
        }
        
    elif temperatura >= 12 and temperatura <= 15:
        data_poke = pokemon('grass')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Grama",
            "sprite": f"{data_poke['sprite']}"
                    
        }

    elif temperatura >= 15 and temperatura <= 21:
        data_poke = pokemon('ground')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Terra",
            "sprite": f"{data_poke['sprite']}"
                                
        }
        
    elif temperatura >= 23 and temperatura <= 27:
        data_poke = pokemon('bug')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Inseto",
            "sprite": f"{data_poke['sprite']}"
                    
        }
        
    elif temperatura >= 27 and temperatura <= 33:
        data_poke = pokemon('rock')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Pedra",
            "sprite": f"{data_poke['sprite']}"
                    
        }

    elif temperatura > 33 :
        data_poke = pokemon('fire')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Fogo",
            "sprite": f"{data_poke['sprite']}"
                    
        }

    else:
        data_poke = pokemon('normal')
        return {
            "nome":f"{data_poke['name'].title()}",
            "tipo":"Normal",
            "sprite": f"{data_poke['sprite']}"
        }


@app.route('/')
def cidade():
   return render_template('cidade.html')


@app.route("/result", methods=["POST"])
def result():
    cidade = request.form.get('cidade')
    try:
        data = dados(cidade)
        temperatura = data["temperatura"]
        chovendo = data["chovendo"]
        pokemon = rules(cidade)
    except:
        return dados(cidade)
    
    r = {
            "temperatura": temperatura,
            "chovendo": chovendo,
            "pokemon": pokemon
        
        }
    return render_template("result.html",result = r)


if __name__ == "__main__":
    app.run(debug=True)
    