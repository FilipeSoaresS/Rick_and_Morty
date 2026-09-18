import json
import re
from pathlib import Path

import psycopg2


# CONFIGURAÇÃO DO BANCO

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "rickandmorty",
    "user": "postgres",
    "password": "123456",
}


# ARQUIVOS JSON

BASE_DIR = Path(__file__).resolve().parent

CHARACTERS_FILE = BASE_DIR / "allCharsUpdated.json"
EPISODES_FILE = BASE_DIR / "allEpisodesUpdated.json"
LOCATIONS_FILE = BASE_DIR / "allLocations.json"


# FUNÇÕES AUXILIARES

def load_json(file_path):
    """Carrega um arquivo JSON."""

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_id(url):
    """
    Extrai o ID do final de uma URL.

    Exemplo:
    https://rickandmortyapi.com/api/character/38
    retorna:
    38
    """

    if not url:
        return None

    match = re.search(r"/(\d+)$", url)

    if match:
        return int(match.group(1))

    return None


# BANCO DE DADOS

def connect_database():

    print("Conectando ao PostgreSQL...")

    connection = psycopg2.connect(**DB_CONFIG)

    print("Conectado!")

    return connection


# CRIAÇÃO DAS TABELAS

def create_tables(cursor):

    # LOCATIONS

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100),
            dimension VARCHAR(255),
            url TEXT,
            created TIMESTAMP
        );
    """)

    # CHARACTERS

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            status VARCHAR(50),
            species VARCHAR(100),
            type VARCHAR(100),
            gender VARCHAR(50),

            origin_id INTEGER REFERENCES locations(id),
            location_id INTEGER REFERENCES locations(id),

            image TEXT,
            url TEXT,
            created TIMESTAMP
        );
    """)

    # EPISODES

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            air_date VARCHAR(100),
            episode VARCHAR(20),
            url TEXT,
            created TIMESTAMP
        );
    """)

    # CHARACTER <-> EPISODE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS character_episodes (
            character_id INTEGER NOT NULL,
            episode_id INTEGER NOT NULL,

            PRIMARY KEY (character_id, episode_id),

            FOREIGN KEY (character_id)
                REFERENCES characters(id)
                ON DELETE CASCADE,

            FOREIGN KEY (episode_id)
                REFERENCES episodes(id)
                ON DELETE CASCADE
        );
    """)

    print("Tabelas verificadas/criadas.")


# INSERIR LOCATIONS

def insert_locations(cursor, locations):

    sql = """
        INSERT INTO locations (
            id,
            name,
            type,
            dimension,
            url,
            created
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """

    for location in locations:

        cursor.execute(
            sql,
            (
                location["id"],
                location["name"],
                location.get("type"),
                location.get("dimension"),
                location.get("url"),
                location.get("created"),
            )
        )

        print(f"Localização: {location['name']}")


# INSERIR CHARACTERS

def insert_characters(cursor, characters):

    sql = """
        INSERT INTO characters (
            id,
            name,
            status,
            species,
            type,
            gender,
            origin_id,
            location_id,
            image,
            url,
            created
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """

    for character in characters:

        origin_id = extract_id(
            character.get("origin", {}).get("url")
        )

        location_id = extract_id(
            character.get("location", {}).get("url")
        )

        cursor.execute(
            sql,
            (
                character["id"],
                character["name"],
                character.get("status"),
                character.get("species"),
                character.get("type"),
                character.get("gender"),
                origin_id,
                location_id,
                character.get("image"),
                character.get("url"),
                character.get("created"),
            )
        )

        print(f"Personagem: {character['name']}")


# INSERIR EPISODES

def insert_episodes(cursor, episodes):

    sql = """
        INSERT INTO episodes (
            id,
            name,
            air_date,
            episode,
            url,
            created
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (id) DO NOTHING;
    """

    for episode in episodes:

        cursor.execute(
            sql,
            (
                episode["id"],
                episode["name"],
                episode.get("air_date"),
                episode.get("episode"),
                episode.get("url"),
                episode.get("created"),
            )
        )

        print(f"Episódio: {episode['name']}")


# RELAÇÃO CHARACTER <-> EPISODE

def insert_character_episodes(cursor, characters):

    sql = """
        INSERT INTO character_episodes (
            character_id,
            episode_id
        )
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
    """

    for character in characters:

        character_id = character["id"]

        for episode_url in character.get("episode", []):

            episode_id = extract_id(episode_url)

            if episode_id is None:
                continue

            cursor.execute(
                sql,
                (
                    character_id,
                    episode_id,
                )
            )

        print(
            f"Relacionamentos de episódios: "
            f"{character['name']}"
        )


# MAIN

def main():

    print("\n========================================")
    print(" RICK AND MORTY DATABASE IMPORTER")
    print("========================================\n")

    # CARREGAR JSON

    print("Carregando JSON...")

    characters = load_json(CHARACTERS_FILE)
    episodes = load_json(EPISODES_FILE)
    locations = load_json(LOCATIONS_FILE)

<<<<<<< HEAD
    characters.sort(key=lambda item: item["id"])
    episodes.sort(key=lambda item: item["id"])
    locations.sort(key=lambda item: item["id"])

=======
>>>>>>> e8e66a95eb7a37017dd598144619b69be73e5f72
    print(f"Personagens: {len(characters)}")
    print(f"Episódios:   {len(episodes)}")
    print(f"Localizações: {len(locations)}")

    # CONECTAR

    connection = connect_database()

    try:

        cursor = connection.cursor()

        # TABELAS

        create_tables(cursor)

        # LOCATIONS

        print("\n--- INSERINDO LOCALIZAÇÕES ---")

        insert_locations(
            cursor,
            locations
        )

        # CHARACTERS

        print("\n--- INSERINDO PERSONAGENS ---")

        insert_characters(
            cursor,
            characters
        )

        # EPISODES

        print("\n--- INSERINDO EPISÓDIOS ---")

        insert_episodes(
            cursor,
            episodes
        )

        # RELACIONAMENTOS

        print("\n--- CRIANDO RELAÇÕES PERSONAGEM/EPISÓDIO ---")

        insert_character_episodes(
            cursor,
            characters
        )

        # COMMIT

        connection.commit()

        print(" IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")

    except Exception as error:

        connection.rollback()

        print("\nERRO:")
        print(error)

    finally:

        cursor.close()
        connection.close()

        print("\nConexão encerrada.")


# EXECUÇÃO

if __name__ == "__main__":
    main()