// Je charge mes dépendances qui me seront utiles durant le projet
const dotenv = require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

// J'instancie mon application avec Express
const app = express();
const port = 3000;

// J'ajoute des fonctionnalités
app.use(express.json());
app.use(express.urlencoded({extended: false}));

// Création d'un middleware inutile mais c'est toujours bien
// de se refresh la mémoire.
app.use((req, res, next) => {
    console.log('Requête reçue');
    next();
});

// Définir une route / sur localhost:3000
app.get('/', (req, res) => {
   res.send('Hey');
});

// Utilisation d'un fichier route avec un Router
app.use('/api/categories', require('./routes/api/category.route'));

// Je "branche" (fais écouter) mon app sur le port 3000
app.listen(port, () => {
    console.log("app démarrée");
});