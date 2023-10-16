// Fonction de prédiction
function getPrediction() {
    var userInput = document.getElementById("user-input").value;
    fetchCSV(userInput);
}

// Fonction pour lire le fichier CSV (Requete serveur flask)
function fetchCSV(userInput) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://127.0.0.1:5000/load_data?horse_name=' + userInput, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var horseData = data.horse_data;
            var winPrediction = data.win_prediction;           
            const newPrompt = 'Ecrit une phrase qui donne le pronostic claire du cheval ' + userInput + '\n\nPronostic : ' + winPrediction;
            fetchPrediction(newPrompt, horseData);
            console.log(winPrediction)
        }
    };
    xhr.send();
}

// Fonction d'envoi de la prédiction vers l'API OpenAI
function fetchPrediction(prompt, horseData) {
    let retryCount = 0;
    var apiKey = "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";
    var endpoint = "https://api.openai.com/v1/completions";
    var prompt = prompt + horseData;
    console.log(prompt);

    var headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey,
    };

    var data = {
        model: 'davinci',
        prompt: prompt,
        max_tokens: 100,
    };

    //envoie de la requete
    fetch(endpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                if (response.status === 429 && retryCount < 3) {
                    retryCount++;
                    const delay = 1000 * Math.pow(2, retryCount); // Backoff exponentiel
                    return new Promise(resolve => setTimeout(() => resolve(fetchPrediction(data, resultElement)), delay));
                }
                throw new Error('Erreur HTTP ' + response.status);
            }
            return response.json();
        })
        .then(result => {
            if (result && result.choices && result.choices[0] && result.choices[0].text) {
                var prediction = result.choices[0].text;
                var predictionResult = document.getElementById('prediction-result');
                predictionResult.innerHTML = prediction;
                //Resultat dans la  Console
                console.log("Prédiction :", prediction);
                
            } else {
                console.error("Erreur lors de la récupération de la prédiction.");
            }
        })
        .catch(error => {
            if (error.message.includes('Erreur HTTP 429')) {
                console.error("Trop de requêtes. Veuillez réessayer plus tard.");
            } else {
                console.error('Erreur :', error);
                console.error("Erreur lors de la récupération de la prédiction.");
            }
        });
}
