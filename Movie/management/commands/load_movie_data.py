from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from Movie.models import MovieQuotes


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
        if MovieQuotes.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading movie data")


        #Code to load the data into database
        for row in DictReader(open('./movie_quotes.csv', "r",encoding='utf-8')):
            child=MovieQuotes(quote=row['quote'], movie=row['movie'], type=row['type'], year=row['year'])  
            child.save()