import requests
import json
import pandas as pd
from typing import Optional, Union
import time


class Book:
    title: str
    subtitle: str
    authors: list
    contributors: list
    publish_date: str
    isbn_10: str
    isbn_13: str
    subjects: list

    def __init__(self, title, ol_id = '', subtitle='', contributors=[], authors=[], publish_date='', isbn_10='', isbn_13='', subjects=[]):
        self.ol_id = ol_id
        self.title = title
        self.subtitle = subtitle
        self.contributors = contributors
        self.authors = authors
        self.publish_date = publish_date
        self.isbn_10 = isbn_10
        self.isbn_13 = isbn_13
        self.subjects = subjects

    def __str__(self) -> str:
        this_str = f'==========\n{self.title =}\n{self.subtitle =}\n{self.authors =}\n{self.publish_date =}\n{self.ol_id =}\n{self.isbn_10 =}\n{self.isbn_13 =}\n{self.subjects =}\n{self.contributors =}\n==========\n'
        return this_str
    
    def get_json(self):
        this_str = {
            'ol_id': self.ol_id,
            'title': self.title,
            'subtitle': self.subtitle,
            'authors': self.authors,
            'publish_date': self.publish_date,
            'isbn_10': self.isbn_10,
            'isbn_13': self.isbn_13,
            'subjects': self.subjects,
            'contributions': self.contributors
        } 

        return json.dumps(this_str)



def get_author(ol_id) -> str:
    author_json = requests.get(f'https://openlibrary.org/authors/{ol_id}.json')
    author_dict = json.loads(author_json.text)
    return author_dict['personal_name']




def main() -> int:
    isbn10s = []

    get_more = True
    while get_more:
        get_isbn = input("\nEnter ISBN-10, ISBN-13, or X to stop entry.\n")
        if get_isbn.lower() == 'x':
            get_more = False
        else:
            isbn10s.append(get_isbn)
            time.sleep(1)

    list_of_dicts = []
    dict_of_dicts = {}
    list_of_books = []
    for isbn10 in isbn10s:
        if isbn10 in dict_of_dicts:
            continue
        else:
            book_json = requests.get(f'https://openlibrary.org/isbn/{isbn10}.json')

            book_dict = json.loads(book_json.text)
            list_of_dicts.append(book_dict)
            dict_of_dicts[isbn10] = book_dict

            author_names = []
            keys = []
            for key, value in book_dict.items():
                keys.append(key)
            if 'authors' in keys:
                list_of_author_links = book_dict['authors']
                author_ids = []
                for obj in list_of_author_links:
                    this_link = obj['key'].split('/')[2]
                    author_ids.append(this_link)
                for author_id in author_ids:
                    name = get_author(author_id)
                    name_dict = {'name': name, 'ol_id': author_id}
                    author_names.append(name_dict)
            
            this_book = Book(book_dict['title'], ol_id=book_dict['key'].split('/')[2], authors=author_names, publish_date=book_dict['publish_date'])
            if 'isbn_10' in keys:
                this_book.isbn_10 = book_dict['isbn_10'][0]
            if 'isbn_13' in keys:
                this_book.isbn_13 = book_dict['isbn_13'][0]
            if 'contributions' in keys:
                this_book.contributors = book_dict['contributions']
            if 'subtitle' in keys:
                this_book.subtitle = book_dict['subtitle']
            if 'subjects' in keys:
                this_book.subjects = book_dict['subjects']
            list_of_books.append(this_book)

    book_df = pd.DataFrame(list_of_dicts)

    # x = book_df.iloc[0]
    # print(x.title)

    for book in list_of_books:
        print(book)

    print(book.get_json())

    return 0

main()
