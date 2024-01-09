import requests
import random

api_token = '302b54d6d9565e619c7ed019517318e1'
language = 'fr'

# Fonction pour vérifier si un genre est disponible
def is_genre_available(genres, selected_genre_id):
    try:
        selected_genre_id = int(selected_genre_id)
        for genre in genres:
            if genre['id'] == selected_genre_id:
                return True
        return False
    except ValueError:
        return False  # La conversion en entier a échoué, ce n'est pas un chiffre valide


# Fonction pour récupérer la liste des genres
def get_genre_list():
    try:
        response = requests.get(f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_token}&language={language}')
        response.raise_for_status()
        genres = sorted(response.json()['genres'], key=lambda x: x['id'])
        return genres
    except requests.exceptions.HTTPError as e:
        print(f"Une erreur HTTP s'est produite : {e}")
        return []

# Fonction pour récupérer les films en fonction du genre et de la note minimale
def get_movies_by_genre(selected_genre_id, min_vote, films_deja_vus):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/discover/movie", params={
            'api_key': api_token,
            'language': language,
            'with_genres': selected_genre_id,
            'vote_average.gte': min_vote
        })
        response.raise_for_status()
        movies = response.json()['results']
        # Filtrer les films déjà vus
        return [movie for movie in movies if movie not in films_deja_vus]
    except requests.exceptions.HTTPError as e:
        print(f"Une erreur HTTP s'est produite : {e}")
        return []

# Liste pour stocker les films déjà vus par l'utilisateur
films_deja_vus = []

print('Bienvenue sur votre outil de suggestion de films.')

continuer = 'oui'

while continuer == 'oui':
    genres = get_genre_list()

    if not genres:
        print("Impossible de récupérer la liste des genres. Vérifiez votre connexion Internet ou les paramètres.")
        break

    # Afficher la liste des genres
    for genre in genres:
        print(f'{genre["id"]} - {genre["name"]}')

    selected_genre_id = input('Commencez par choisir un genre de film par son id : ')
    # Vérifier si le genre choisi est disponible
    if not is_genre_available(genres, selected_genre_id):
        print("Genre non valide. Veuillez choisir un genre valide.")
        continue  # Revenir au début de la boucle pour demander un autre genre

    min_vote = input('A partir de quelle note sur 10 jugez-vous le film admissible pour un visionnage ? ')

    movies_per_genre = get_movies_by_genre(selected_genre_id, min_vote, films_deja_vus)

    if not movies_per_genre:
        print("Aucun film trouvé pour ce genre et cette note minimale.")
    else:
        movies_per_genre.sort(key=lambda x: (x['vote_average'], x['popularity']), reverse=True)

        print('Afficher la liste des films ou un film tiré au hasard ? (1 ou 2)')
        choice = input()
        if choice == '1':
            # Afficher uniquement les films qui ne sont pas déjà vus
            for movie in movies_per_genre:
                if movie not in films_deja_vus:
                    print(f"\n\n{movie['title']} - {movie['release_date']}\n{movie['overview']}\nMoyenne : {movie['vote_average']}")
                    # Demander si l'utilisateur a vu le film
                    vu = input('Avez-vous déjà vu ce film ? (oui/non) ').lower()
                    if vu == 'oui':
                        films_deja_vus.append(movie)  # Ajouter le film à la liste des films déjà vus
        else:
            while True:
                films_non_vus = [movie for movie in movies_per_genre if movie not in films_deja_vus]
                if not films_non_vus:
                    print("Vous avez vu tous les films disponibles dans cette catégorie.")
                    break
                random_movie = random.choice(films_non_vus)
                print(
                    f"\n\n{random_movie.get('title', 'Titre inconnu')} - {random_movie.get('release_date', 'Date de sortie inconnue')}\n{random_movie.get('overview', 'Aucune description disponible')}\nMoyenne : {random_movie.get('vote_average', 'Moyenne inconnue')}")
                # Demander si l'utilisateur a vu le film
                vu = input('Avez-vous déjà vu ce film ? (oui/non) ').lower()
                if vu != 'oui':
                    break  # Sortir de la boucle interne si l'utilisateur n'a pas vu le film
                else:
                    films_deja_vus.append(random_movie)  # Ajouter le film à la liste des films déjà vus

    continuer = input('\nFaire une autre recherche ? (oui/non) ')

# Consulter la liste des films déjà vus
if films_deja_vus:
    print("\nListe des films déjà vus :")
    for movie in films_deja_vus:
        print(f"{movie['title']} - {movie['release_date']}")

print('Merci d\'avoir utilisé notre service de suggestion de films.')