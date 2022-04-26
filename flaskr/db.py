import sqlite3
import csv
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext

columns = ['adult', 'belongs_to_collection', 'budget', 'genres', 'homepage', 'id', 'imdb_id', 'original_language', 'original_title', 
        'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries', 'release_date', 'revenue',
        'runtime', 'spoken_languages', 'status', 'tagline', 'title', 'video', 'vote_average', 'vote_count']

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db(csv_path = None):
    db = get_db()
    cur = db.cursor()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    if csv_path is None:
        csv_path = os.path.join(current_app.root_path, "db/movies.csv")
    
    with open(csv_path, mode='r', encoding="utf-8") as f:
        dr = csv.DictReader(f)
        to_db = [
            (i['adult'], i['belongs_to_collection'], i['budget'], i['genres'], 
            i['homepage'], i['id'], i['imdb_id'], i['original_language'], i['original_title'], 
            i['overview'], i['popularity'], i['poster_path'], i['production_companies'], 
            i['production_countries'], i['release_date'], i['revenue'],
            i['runtime'], i['spoken_languages'], i['status'], i['tagline'], i['title'], 
            i['video'], i['vote_average'], i['vote_count']) for i in dr ]
        cur.executemany('''INSERT INTO movies (
            adult, belongs_to_collection, budget, genres, homepage, id, imdb_id, original_language, original_title, 
            overview, popularity, poster_path, production_companies, production_countries, release_date, revenue,
            runtime, spoken_languages, status, tagline, title, video, vote_average, vote_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?)''', to_db)
        db.commit()
        
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_movies():
    db = get_db()
    results = db.execute('''SELECT * FROM movies''').fetchall()
    formatted_results = []
    for record in results:
        new_record = {}
        for idx, column in enumerate(columns):
            new_record[column] = record[idx]
        formatted_results.append(new_record)

    return formatted_results

def get_movie_by_id(id):
    db = get_db()
    results = db.execute(f"SELECT * FROM movies WHERE id ='{id}'")
    formatted_results = []
    for record in results:
        new_record = {}
        for idx, column in enumerate(columns):
            new_record[column] = record[idx]
        formatted_results.append(new_record)
    return formatted_results
