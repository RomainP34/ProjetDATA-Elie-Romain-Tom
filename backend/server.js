// Importation des modules nécessaires
const dotenv = require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

// Initialisation de l'application Express
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Middleware pour logger les routes accédées
app.use((req, res, next) => {
    console.log('Route reçue');
    next();
});

// Définition d'une route de base
app.get('/', (req, res) => {
    res.send('Hey');
});


app.get('/categories', async (req, res) => {
    // Je récupère ma clé api
    const apiKey = process.env.TMDB_API_KEY

    // Je confirme l'url avec la clé à l'interieur
    const url = `https://api.themoviedb.org/3/genre/movie/list?api_key=${apiKey}&languague=fr`;

    const response = await fetch(url)
    const genres = await response.json();

    // Ce que j'affiche aux utilisateurs
    res.json(genres)
});


app.listen(port, () => {
    console.log("App démarrée sur le port " + port);
});
