from typing import Any
from Song.models import TrackLyric
from django.core.management import BaseCommand
import ast

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any): 
        all_song = TrackLyric.objects.all()
        for song in all_song:
            val = song.genre
            print(f"Original value: {val}")
            try:
                # Try to evaluate the string as a Python list
                parsed_data = ast.literal_eval(val)
                if isinstance(parsed_data, list) and all(isinstance(item, str) for item in parsed_data):
                    # If the parsed data is a list of strings, join them with commas
                    my_string = ', '.join(parsed_data)
                else:
                    # If not a valid list, assume it's a simple comma-separated string
                    my_string = val
            except (SyntaxError, ValueError):
                # If evaluation fails, assume it's a simple comma-separated string
                my_string = val
            
            # Save the modified string
            song.genre = my_string
            song.save()
            print(f"Saved song {song.pk} with genre {my_string}")
