from django.core.management.base import BaseCommand
import csv
import importlib.resources
"""
https://judaism.stackexchange.com/a/76293
Torah: 79,847 words (according to E.S.)
Neviim: 141,414 words (also, according to E. S.)
Kesuvim: 83,640 words (
"""
def calculate_line_number(book_no, chapter, line):
    index = 0
    with importlib.resources.open_text("djangotanach.csv","counts.csv") as csv_file:
        t_count = list(csv.reader(csv_file))
        # book = t_count[book_no+1]
        for i in range(len(t_count)):
            chapter_count = t_count[i]
            if i == book_no-1:
                if chapter < 1 or chapter > len(chapter_count):
                    return "Invalid chapter number"

                if line < 1 or line > int(chapter_count[chapter - 1]):
                    return "Invalid verse number"

                # Sum up all previous chapters' verses
                index += sum(int(c) for c in chapter_count[:chapter - 1])
                
                # Add the verse number (1-based index)
                index += line

                return index

            else:
                # Sum up all verses of previous books
                index += sum(int(c) for c in t_count[i])

    return "Book not found"

class Command(BaseCommand):
    help = "Quran commands"

    def handle(self, *args, **options):
        lineno = calculate_line_number(1,1,1)-1 # since index starts with zero
        with importlib.resources.open_text("djangotanach.csv","words.csv") as csv_file:
            words_list = list(csv.reader(csv_file))
            line = words_list[lineno]
            self.stdout.write(f'line:{line}')
        