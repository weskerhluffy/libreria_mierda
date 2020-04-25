'''
Created on 29/05/2018

@author: ernesto
'''
# XXX: https://coderpad.io/4HNMFFYG

from re import split

"""
Given a flat file of book metadata, write a Library class that parses the book data and provides an API that lets you search for all books containing a word.

API:

Library
  - <constructor>(input) -> returns a Library object
  - search(word) -> returns all books that contain the word anywhere in the
                    title, author, or description fields. Only matches *whole* words.
                    E.g. Searching for "My" or "book" would match a book containing
                    "My book", but searching for "My b" or "boo" would *not* match.
"""
from re import match, sub
from collections import namedtuple

# Parse the string, so as to separate each metadata book
# For every book (all its metadata), get words from all attributes.
# For every word, store the (case insensitive) word as key of a dictionary, and the value will be the title of the book.
# For words not matching return empty list.

# Words               # Books
# Hitchhiker's        Hitchhiker's Guide to the Galaxy
# lower(Guide)        Hitchhiker's Guide to the Galaxy
# 
 
# Phd. Sr.

# Word boundary->space and semicolon
LIBRARY_DATA = """
TITLE: Hitchhiker's Guide to the Galaxy 
AUTHOR: Douglas Adams
DESCRIPTION: Seconds before the Earth is demolished to make way for a galactic freeway,
Arthur Dent is plucked off the planet by his friend Ford Prefect, a researcher for the
revised edition of The Hitchhiker's Guide to the Galaxy who, for the last fifteen years, has been posing as an out-of-work actor.

TITLE: Dune
AUTHOR: Frank Herbert
DESCRIPTION: The troubles begin when stewardship of Arrakis is transferred by the
Emperor from the Harkonnen Noble House to House Atreides. The Harkonnens don't want to
give up their privilege, though, and through sabotage and treachery they cast young
Duke Paul Atreides out into the planet's harsh environment to die. There he falls in
with the Fremen, a tribe of desert dwellers who become the basis of the army with which
he will reclaim what's rightfully his. Paul Atreides, though, is far more than just a
usurped duke. He might be the end product of a very long-term genetic experiment
designed to breed a super human; he might be a messiah. His struggle is at the center
of a nexus of powerful people and events, and the repercussions will be felt throughout
the Imperium.

TITLE: A Song Of Ice And Fire Series
AUTHOR: George R.R. Martin
DESCRIPTION: As the Seven Kingdoms face a generation-long winter, the noble Stark family confronts the poisonous plots of the rival Lannisters, the emergence of the
White Walkers, the arrival of barbarian hordes, and other threats.

"""

Book = namedtuple("Book", "title author description")


class Library:

    def __init__(self, data):
        self.data = data
        self._wb = {}  # Word to book mapping
        self.books = None
        # parse/split the book data, so as to have one entry per book.
        self._parse_books()
        # create dict word to book
        self._create_word_to_book()

    def _parse_books(self):
#        book_strs=self.data.split("\n\n")
        self.books=[]
        book_strs=split(r"\n\n",self.data)
#        print("libros {}".format(book_strs))
        for book_str in book_strs:
            if not book_str.strip():
                continue
            lines=book_str.split("\n")
#            print("lineas {}".format(lines))
            book={}
            for line in filter(lambda l:l.strip(),lines):
#                print("linea {}".format(line))
                if ":" in line:
                    attr_name, attr_value=line.split(":")
                    book[attr_name.strip()]=attr_value.strip()
                else:
                    book["DESCRIPTION"]+=line
            self.books.append(Book(book["TITLE"],book["AUTHOR"],book["DESCRIPTION"]))
            
    def _create_word_to_book(self):
        books = self.books
        for book in books:
            for attr in book:
                for word in attr.split(" "):
                    word = sub("[.,:]", "", word.lower().strip())
                    if word:
                        self._wb.setdefault(word, set()).add(book)
#        print(self._wb)
    
    def search(self, word):
        r = []
        lword = word.lower()
#        print("buscando {} en {}".format(lword, self._wb.keys()))
        if lword in self._wb:
            r = list(self._wb[lword])
#        print("r {}".format(r))
        return r


library = Library(LIBRARY_DATA)
first_results = library.search("Arrakis")
assert first_results[0].title == "Dune"
second_results = library.search("winter")
assert second_results[0].title == "A Song Of Ice And Fire Series"
third_results = library.search("demolished")
assert third_results[0].title == "Hitchhiker's Guide to the Galaxy"
fourth_results = library.search("the")
assert len(fourth_results) == 3
titles = [result.title for result in fourth_results]
assert "Dune" in titles
assert "A Song Of Ice And Fire Series" in titles
assert "Hitchhiker's Guide to the Galaxy" in titles
