from pymongo import MongoClient
from mimesis import Text
import pandas as pd
from progress.bar import Bar

client = MongoClient()
text_faker = Text(locale='en')


def connect_db(db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    return collection


def store_books():
    books_collection = connect_db('goodreads', 'books')
    df_books = pd.read_csv('./goodbooks-10k/books.csv', index_col=0)
    books_list = []
    bar = Bar('Processing books', max=len(df_books))
    for idx, book in df_books.iterrows():
        data = {
            'bookId': book['book_id'],
            'workId': book['work_id'],
            'originalTitle': book['original_title'],
            'title': book['title'],
            'isbn': book['isbn'],
            'isbn13': book['isbn13'],
            'authors': book['authors'].split(','),
            'publicationYear': book['original_publication_year'],
            'languageCode': book['language_code'],
            'avgRating': book['average_rating'],
            'ratingsCount': book['ratings_count'],
            'workRatingsCount': book['work_ratings_count'],
            'workTextReviewsCount': book['work_ratings_count'],
            'ratings1': book['ratings_1'],
            'ratings2': book['ratings_2'],
            'ratings3': book['ratings_3'],
            'ratings4': book['ratings_4'],
            'ratings5': book['ratings_5'],
            'coverURL': book['image_url'],
            'smallCoverURL': book['small_image_url'],
            'Description': text_faker.text(),
        }
        books_list.append(data)
        bar.next()
    bar.finish()
    result = books_collection.insert_many(books_list)
    print(f'{len(result.inserted_ids)} inserted books')


def main():
    store_books()


if __name__ == '__main__':
    main()