#Load CSV into custom django model. Run only once.
import os
import django
import csv

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_database.settings')
django.setup()

# Now you can import your models
from anime.models import Anime

def load_data_from_csv(start_row=0):
    with open('myanimelist.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        r = 0
        for row in reader:
            if r < start_row:
                r=r+1
                continue
            print("Processing row:", r)
            r = r + 1
            uid = row['uid']
            # Check if a record with the same uid already exists
            existing_anime = Anime.objects.filter(uid=uid).first()
            if existing_anime:
                print(f"Record with uid={uid} already exists. Updating instead.")
                # Update existing record
                existing_anime.title = row['title']
                existing_anime.synopsis = row['synopsis']
                existing_anime.genre = row['genre']
                existing_anime.aired = row['aired']
                existing_anime.episodes = int(float(row['episodes'])) if row['episodes'] else 0
                existing_anime.members = int(row['members']) if row['members'] else 0
                existing_anime.popularity = float(row['popularity']) if row['popularity'] else 0.0
                existing_anime.ranked = float(row['ranked']) if row['ranked'] else 0.0
                existing_anime.score = float(row['score']) if row['score'] else 0.0
                existing_anime.img_url = row['img_url']
                existing_anime.link = row['link']
                existing_anime.save()
                print("Record updated successfully.")
            else:
                print("Creating record with uid:", uid)
                # Check if 'episodes' field is empty
                episodes = int(float(row['episodes'])) if row['episodes'] else 0
                # Check if 'members' field is empty
                members = int(row['members']) if row['members'] else 0
                # Check if 'popularity' field is empty
                popularity = float(row['popularity']) if row['popularity'] else 0.0
                # Check if 'ranked' field is empty
                ranked = float(row['ranked']) if row['ranked'] else 0.0
                Anime.objects.create(
                    uid=uid,
                    title=row['title'],
                    synopsis=row['synopsis'],
                    genre=row['genre'],
                    aired=row['aired'],
                    episodes=episodes,
                    members=members,
                    popularity=popularity,
                    ranked=ranked,
                    score=float(row['score']) if row['score'] else 0.0,
                    img_url=row['img_url'],
                    link=row['link']
                )
                print("Record created successfully.")

# Call the function to load data from the CSV file
load_data_from_csv(0)
