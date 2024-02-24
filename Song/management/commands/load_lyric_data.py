from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from Song.models import SongLyric,MusicLyric, BillBoardLyric, TrackLyric


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"
    
    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if TrackLyric.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading songs data")


        #Code to load the data into database
        for row in DictReader(open('./track_album_spotify_youtube_artist.csv', "r",encoding='utf-8')):
            song = TrackLyric(artist_name=row['artist'], track_name=row['title'], genre=row['genre'], 
                              lyrics=row['lyrics'], release_date=int(float(row['year'])), 
                              youtube_link=row['youtube_links'], spotify_link=row['url_spotify'], album=row['Album'])  
            song.save()