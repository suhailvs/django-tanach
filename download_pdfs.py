import urllib.request
# pip install pypdf
from pypdf import PdfReader
# create a djangoapp myapp and add a model with name Word
from djangotanach.models import Word
# you can get this from: https://github.com:suhailvs/torah/django_site/tanach/books.py
from djangotanach.books import TANACH_BOOKS, NT_BOOKS

HEBREW_UNICODE = "אבגדהוזחטיכלמנסעפצקרשת"

def bulk_create_words(chapter_data, book_index,chapter_index):
    """
    Bulk inserts Hebrew words into the database.
    Deletes previous entries before inserting new data.
    """
    # Word.objects.all().delete()

    bulk_list = []
    counter=0
    for line in chapter_data:
        if not line:
            continue

        for wn, w in enumerate(line):
            bulk_list.append(
                Word(
                    book=book_index+1,  # Genesis
                    chapter=chapter_index+1,
                    line=counter + 1,
                    position=wn + 1,
                    token=w[0].strip(),
                    # english_hebrew=w[1].strip(),
                    meaning=w[2].strip(),
                )
            )
        counter+=1
    Word.objects.bulk_create(bulk_list)


def parse_pdf(file_path="gen1.pdf"):
    """
    Parses a Hebrew-English interlinear PDF and extracts structured word data.
    """
    reader = PdfReader(file_path)
    chapter_data = []

    for page in reader.pages:
        text = page.extract_text()
        words = text.split("\n")
        word_found = []

        # Extract Hebrew words and their corresponding translations
        for i in range(len(words)):
            if any(letter in HEBREW_UNICODE for letter in words[i]):
                word_found.append([words[i], words[i + 1], words[i + 2]])

        # Group words by line
        lines, line_words = [], []
        oldpage_line_balance = []
        for i, w in enumerate(word_found):
            if i == 0:
                if ":" not in w[0]:
                    # ['hebrew', 'b·dgth ', 'in·fish-of ']
                    oldpage_line_balance.append(w) 
                    continue
            
            if ":" in w[0]:  # Identify new line
                if oldpage_line_balance:
                    if chapter_data:
                        chapter_data[-1].extend(oldpage_line_balance)
                    oldpage_line_balance = []
                lines.append(line_words)
                line_words = []

            elif oldpage_line_balance:
                oldpage_line_balance.append(w)
                continue
            line_words.append(w)

            if i == len(word_found) - 1:  # Last element
                lines.append(line_words)
        chapter_data.extend(lines)
    return chapter_data


def download_pdf(fname, bookindex,chapter_index):
    """
    Downloads Hebrew-English interlinear PDFs from scripture4all.org.
    """

    ot_names = ['gen','exo','lev','num','deu','jos','jdg','rut','1sa','2sa','1kg',
        '2kg','1ch','2ch','ezr','neh','est','job','psa','pro','qoh',
        'can','isa','jer','lam','eze','dan','hos','joe','amo','oba',
        'jon','mic','nah','hab','zep','hag','zec','mal']
    base_url = "https://www.scripture4all.org/OnlineInterlinear/OTpdf"
    dname = f"{ot_names[bookindex]}{chapter_index + 1}.pdf"
    print(f"Downloading: {dname}")
    urllib.request.urlretrieve(f"{base_url}/{dname}", fname)


def display_saved_data(book_index,chapter_count, chapter_index):
    """
    Displays saved Hebrew words and their English meanings from the database.
    """
   
    for line_num in range(chapter_count):
        words = Word.objects.filter(
            book=book_index + 1, chapter=chapter_index + 1, line=line_num + 1
        ).order_by("position")

        print(f"Book {book_index + 1}, Chapter {chapter_index + 1}, Line {line_num + 1}")
        print(" ".join(w.meaning.strip() for w in words))
        print(" ".join(w.token.strip() for w in words))
        print(" ".join(w.english_hebrew.strip() for w in words))
        print("\n")



def save_csv():
    import csv
    with open('en_wordsfull.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)        
        for cb in range(len(TANACH_BOOKS)):            
            book = TANACH_BOOKS[cb]
            print('writing book:',book)
            for cc in range(len(book['chapters'])):
                chapters = book['chapters'][cc]
                for cl in range(chapters):
                    words= Word.objects.filter(
                        book=cb+1,chapter=cc+1, line=cl+1)
                    csvwriter.writerow([w.meaning for w in words])
        print('completed. writing data')
        

def a():
    # Word.objects.all().delete()
    for book_index, book in enumerate(TANACH_BOOKS):
        # if book_index==13:
            
        fn = book["book"].replace(' ','')[:3].lower()
        
        for chapter_index, chapter_count in enumerate(book["chapters"]):
            if Word.objects.filter(book=book_index+1, chapter=chapter_index+1): continue

            fname = f"djangotanach/pdfs/tanach/{fn}{chapter_index + 1}.pdf"
            print(fname)
            # download_pdf(fname, book_index,chapter_index)
            chapter_data=parse_pdf(fname)
            bulk_create_words(chapter_data,book_index,chapter_index)
            # display_saved_data(book_index,chapter_count, chapter_index)
    save_csv()
    
def b():
    # download_pdf_newtestment
    base_url = "https://www.scripture4all.org/OnlineInterlinear/NTpdf"
    for book_index, book in enumerate(NT_BOOKS):
        fn = book["book"].replace(' ','')[:3].lower()
        for chapter_index in range(book["chapters"]):
            if fn == 'phi': fn='phm'
            fname = f"pdfs/nt/{fn}{chapter_index + 1}.pdf"
            dname = f"{fn}{chapter_index + 1}.pdf"
            print(f"Downloading: {dname}")
            urllib.request.urlretrieve(f"{base_url}/{dname}", fname)
# if __name__=='__main__':
a()