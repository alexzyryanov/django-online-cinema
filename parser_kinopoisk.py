import requests
import json
import sqlite3


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}


def kinopoisk_parser():
    url = "https://api.ott.kinopoisk.ru/v12/selections/434?limit=100&offset=1&selectionWindowId=tvod_est&serviceId=25"

    request = requests.get(url=url, headers=header)
    responce = request.json()
    with open("movies.json", "w", encoding="utf-8") as file:
        json.dump(responce, file, ensure_ascii=False, indent=4)


def add_db_cinema():
    with open("movies.json", "rb") as file:
        data = json.load(file)

    connect_db = sqlite3.connect("online_cinema\db.sqlite3")
    cursor = connect_db.cursor()
    for i in data["data"]:
        cursor.execute(""" INSERT INTO content_content VALUES (?, ?, ?, ?, ?, ?, ?) """,
            (len(cursor.execute(""" SELECT id FROM content_content """).fetchall()) + 1,
            i["title"],
            i["posterUrl"],
            i["horizontalPoster"],
            0,
            i["id"],
            i["years"]))
        connect_db.commit()
    cursor.close()
    connect_db.close()


def add_db_genre():
    with open("movies.json", "rb") as file:
        data = json.load(file)

    all_genres = []
    for i in data["data"]:
        if len(i["genres"]) > 1:
            for genre in i["genres"]:
                all_genres.append(genre)

    connect_db = sqlite3.connect("online_cinema\db.sqlite3")
    cursor = connect_db.cursor()

    for i in set(all_genres):
        cursor.execute(""" INSERT INTO content_genre VALUES (?, ?) """,
            (len(cursor.execute(""" SELECT id FROM content_genre """).fetchall()) + 1, i))
        connect_db.commit()

    cursor.close()
    connect_db.close()


def correct_genre():
    with open("movies.json", "rb") as file:
        data = json.load(file)

    connect_db = sqlite3.connect("online_cinema\db.sqlite3")
    cursor = connect_db.cursor()

    for movie in data["data"]:
        curret_movie = movie["title"]
        if len(movie["genres"]) > 1:
            for genre in movie["genres"]:
                cursor.execute(""" INSERT INTO content_content_genres VALUES (?, ?, ?) """,
                    (len(cursor.execute(""" SELECT id FROM content_content_genres """).fetchall()) + 1,
                    cursor.execute(f""" SELECT id FROM content_content WHERE name_film = "{curret_movie}" """).fetchone()[0],
                    cursor.execute(f""" SELECT id FROM content_genre WHERE name_genre = "{genre}" """).fetchone()[0]))
                connect_db.commit()

        elif len(movie["genres"]) == 1:
            cursor.execute(""" INSERT INTO content_content_genres VALUES (?, ?, ?) """,
                (len(cursor.execute(""" SELECT id FROM content_content_genres """).fetchall()) + 1,
                cursor.execute(f""" SELECT id FROM content_content WHERE name_film = "{curret_movie}" """).fetchone()[0],
                cursor.execute(f""" SELECT id FROM content_genre WHERE name_genre = "{movie["genres"][0]}" """).fetchone()[0]))
            connect_db.commit()
                
    cursor.close()
    connect_db.close()


def kinopoisk_actor_parse():
    connect_db = sqlite3.connect("online_cinema\db.sqlite3")
    cursor = connect_db.cursor()

    urls = [i[0] for i in cursor.execute(""" SELECT id_film FROM content_content """)]
    for i in urls:
        id_film = i
        url = f"https://api.ott.kinopoisk.ru/v12/hd/content/{id_film}/metadata/external"
        request = requests.get(url=url, headers=header)
        responce = request.json()

        all_actors = [i[0] for i in cursor.execute(""" SELECT name_actor FROM content_actor """)]

        for actor in responce["credits"]["actors"]:
            if actor["person"]["name"] not in all_actors:
                print(actor["person"]["name"])
                cursor.execute(""" INSERT INTO content_actor VALUES (?, ?, ?, ?) """,
                    (len(cursor.execute(""" SELECT id FROM content_actor """).fetchall()) + 1,
                    actor["person"]["name"],
                    0,
                    actor["person"]["imageUrl"]))
                connect_db.commit()
                all_actors.append(actor)

            cursor.execute(""" INSERT INTO content_content_actors VALUES (?, ?, ?) """,
            (len(cursor.execute(""" SELECT id FROM content_content_actors """).fetchall()) + 1,
            cursor.execute(f""" SELECT id FROM content_content WHERE id_film = "{id_film}" """).fetchone()[0],
            cursor.execute(f""" SELECT id FROM content_actor WHERE name_actor = "{actor["person"]["name"]}" """).fetchone()[0]))
            connect_db.commit()

    cursor.close()
    connect_db.close()



def main():
    kinopoisk_parser()
    add_db_cinema()
    add_db_genre()
    correct_genre()
    kinopoisk_actor_parse()


if __name__ == "__main__":
    main()
