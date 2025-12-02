# recommend.py - Mood + Genre + Language based Movie Recommender (no external libs)
# Run with:  python3 recommend.py

from typing import List, Dict

MOVIES: List[Dict] = [
    {"title": "The Matrix", "genre": "sci-fi|action", "language": "english", "mood": "intense", "rating": 8.7, "year": 1999, "description": "A hacker discovers reality is a simulation."},
    {"title": "Inception", "genre": "sci-fi|thriller", "language": "english", "mood": "intense", "rating": 8.8, "year": 2010, "description": "A thief enters dreams to steal secrets."},
    {"title": "Interstellar", "genre": "sci-fi|drama", "language": "english", "mood": "thoughtful", "rating": 8.6, "year": 2014, "description": "A team travels through a wormhole searching for a new home."},
    {"title": "The Dark Knight", "genre": "action|crime", "language": "english", "mood": "intense", "rating": 9.0, "year": 2008, "description": "Batman faces the Joker in Gotham."},
    {"title": "The Avengers", "genre": "action|adventure", "language": "english", "mood": "excited", "rating": 8.0, "year": 2012, "description": "Superheroes team up to save Earth."},
    {"title": "Guardians of the Galaxy", "genre": "action|comedy", "language": "english", "mood": "happy", "rating": 8.0, "year": 2014, "description": "A group of misfits protect the galaxy."},
    {"title": "Forrest Gump", "genre": "drama|romance", "language": "english", "mood": "emotional", "rating": 8.8, "year": 1994, "description": "A simple man lives an extraordinary life."},
    {"title": "The Shawshank Redemption", "genre": "drama", "language": "english", "mood": "thoughtful", "rating": 9.3, "year": 1994, "description": "Two prisoners build a deep friendship and plan escape."},
    {"title": "La La Land", "genre": "musical|romance", "language": "english", "mood": "romantic", "rating": 8.0, "year": 2016, "description": "Two artists chase dreams and love in Los Angeles."},
    {"title": "Whiplash", "genre": "drama", "language": "english", "mood": "intense", "rating": 8.5, "year": 2014, "description": "A drummer faces a brutal music teacher."},
    {"title": "3 Idiots", "genre": "comedy|drama", "language": "hindi", "mood": "happy", "rating": 8.4, "year": 2009, "description": "Three engineering students question the education system."},
    {"title": "Taare Zameen Par", "genre": "drama", "language": "hindi", "mood": "emotional", "rating": 8.3, "year": 2007, "description": "A teacher helps a dyslexic child discover his talent."},
    {"title": "Chhichhore", "genre": "comedy|drama", "language": "hindi", "mood": "happy", "rating": 8.0, "year": 2019, "description": "A father recalls college days to inspire his son."},
    {"title": "ZNMD", "genre": "comedy|adventure", "language": "hindi", "mood": "chill", "rating": 8.1, "year": 2011, "description": "Three friends go on a road trip in Spain."},
    {"title": "Andhadhun", "genre": "thriller|dark", "language": "hindi", "mood": "intense", "rating": 8.2, "year": 2018, "description": "A blind pianist gets stuck in a murder mystery."},
    {"title": "Your Name", "genre": "anime|romance", "language": "anime-jp", "mood": "romantic", "rating": 8.4, "year": 2016, "description": "Two strangers mysteriously swap bodies."},
    {"title": "Spirited Away", "genre": "anime|fantasy", "language": "anime-jp", "mood": "wholesome", "rating": 8.6, "year": 2001, "description": "A girl enters a magical spirit world."},
    {"title": "Attack on Titan: Chronicle", "genre": "anime|action", "language": "anime-jp", "mood": "intense", "rating": 8.7, "year": 2020, "description": "Humanity fights against giant titans."},
    {"title": "Demon Slayer: Mugen Train", "genre": "anime|action", "language": "anime-jp", "mood": "intense", "rating": 8.3, "year": 2020, "description": "Demon slayers guard passengers on a haunted train."},
    {"title": "Inside Out", "genre": "animation|family", "language": "english", "mood": "wholesome", "rating": 8.1, "year": 2015, "description": "Emotions inside a girl's mind deal with change."},
    {"title": "Coco", "genre": "animation|family", "language": "english", "mood": "wholesome", "rating": 8.4, "year": 2017, "description": "A boy travels to the Land of the Dead to find his ancestor."},
    {"title": "The Pursuit of Happyness", "genre": "drama", "language": "english", "mood": "emotional", "rating": 8.0, "year": 2006, "description": "A struggling father never gives up on his dream."},
    {"title": "DDLJ", "genre": "romance", "language": "hindi", "mood": "romantic", "rating": 8.0, "year": 1995, "description": "A love story across Europe and India."},
    {"title": "Barfi!", "genre": "romance|drama", "language": "hindi", "mood": "wholesome", "rating": 8.1, "year": 2012, "description": "A mute and deaf man finds love and friendship."},
    {"title": "Edge of Tomorrow", "genre": "sci-fi|action", "language": "english", "mood": "excited", "rating": 7.9, "year": 2014, "description": "A soldier relives the same battle day repeatedly."},
    {"title": "The Martian", "genre": "sci-fi|drama", "language": "english", "mood": "thoughtful", "rating": 8.0, "year": 2015, "description": "A stranded astronaut survives alone on Mars."},
    {"title": "Joker", "genre": "drama|thriller", "language": "english", "mood": "emotional", "rating": 8.4, "year": 2019, "description": "The story of a lonely man turning into the Joker."},
    {"title": "Dear Zindagi", "genre": "drama", "language": "hindi", "mood": "thoughtful", "rating": 7.5, "year": 2016, "description": "A young woman talks to a therapist to heal."},
]

MOOD_OPTIONS = ["happy", "sad", "chill", "intense", "romantic", "thoughtful", "wholesome", "emotional", "excited"]
GENRE_OPTIONS = ["sci-fi", "action", "drama", "comedy", "romance", "anime", "thriller", "family", "any"]
LANG_OPTIONS = ["english", "hindi", "anime-jp", "any"]


def ask_choice(prompt: str, options: list) -> str:
    print(prompt)
    print("Options:", ", ".join(options))
    while True:
        choice = input("> ").strip().lower()
        if choice in options:
            return choice
        print("Please type one of:", ", ".join(options))


def filter_movies(mood: str, genre: str, language: str) -> List[Dict]:
    result = []
    for m in MOVIES:
        if m["mood"] != mood:
            continue
        if genre != "any" and genre not in m["genre"]:
            continue
        if language != "any" and m["language"] != language:
            continue
        result.append(m)
    return result


def recommend(mood: str, genre: str, language: str, top_k: int = 3) -> List[Dict]:
    print("\n[1] Trying exact match: mood + genre + language...")
    movies = filter_movies(mood, genre, language)

    if not movies:
        print("   No exact match. Relaxing language filter...")
        movies = filter_movies(mood, genre, "any")

    if not movies:
        print("   Still empty. Relaxing genre filter...")
        movies = filter_movies(mood, "any", language)

    if not movies:
        print("   Still empty. Only using mood...")
        movies = filter_movies(mood, "any", "any")

    movies.sort(key=lambda x: x["rating"], reverse=True)
    return movies[:top_k]


def main():
    print("=" * 60)
    print("MOVIE RECOMMENDATION SYSTEM (Mood + Genre + Language)")
    print("=" * 60)
    print(f"Total movies in catalogue: {len(MOVIES)}\n")

    mood = ask_choice("1) How are you feeling right now? (mood)", MOOD_OPTIONS)
    genre = ask_choice("2) What genre do you feel like watching? ('any' = no preference)", GENRE_OPTIONS)
    language = ask_choice("3) Preferred language? ('any' = no preference)", LANG_OPTIONS)

    print(f"\n🎯 Searching for movies with mood='{mood}', genre='{genre}', language='{language}'...\n")
    recs = recommend(mood, genre, language, top_k=3)

    if not recs:
        print("Sorry, no movies found. Try different options next time.")
        return

    print("Here are your recommendations:\n")
    for m in recs:
        print(f"- {m['title']} ({m['year']})  ⭐ {m['rating']}")
        print(f"  Genre: {m['genre']} | Language: {m['language']} | Mood: {m['mood']}")
        print(f"  {m['description']}\n")


if __name__ == "__main__":
    main()

