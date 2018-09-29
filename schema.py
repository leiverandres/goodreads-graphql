import graphene
from pymongo import MongoClient
from basic_types import Book, Review

client = MongoClient()
books_collection = client.goodreads.books
reviews_collection = client.goodreads.reviews


class CreateReview(graphene.Mutation):
    class Arguments:
        bookId = graphene.Int(name='bookId', required=True)
        username = graphene.String(required=True)
        rate = graphene.Float(required=True)
        text = graphene.String(required=True)

    state = graphene.String()
    review = graphene.Field(Review)

    def mutate(self, info, bookId, username, rate, text):
        result = books_collection.find_one({'bookId': bookId})
        if result == None:
            return CreateReview(state='Book id not found')
        new_review = {
            'bookId': bookId,
            'username': username,
            'rate': rate,
            'text': text,
            'likes': 0,
        }
        result = reviews_collection.insert_one(new_review)

        if not result is None:
            return CreateReview(state='success', review=new_review)
        else:
            return {'state': 'Something went wrong on serverside'}


class Query(graphene.ObjectType):
    books = graphene.List(Book, pageSize=graphene.Int(), page=graphene.Int())
    book = graphene.Field(Book, bookId=graphene.ID(required=True))
    reviews = graphene.List(Review)

    def resolve_books(self, info, **kwargs):
        pageSize = kwargs.get('pageSize', None)
        page = kwargs.get('page', None)
        books = books_collection.find()
        if pageSize != None and page != None:
            start = page * pageSize
            end = start + pageSize
            return books[start:end]
        return books

    def resolve_book(self, info, bookId):
        result = books_collection.find_one({'bookId': int(bookId)})
        if result == None:
            return {'message': 'Book not found'}
        else:
            return result

    def resolve_reviews(self, info):
        results = reviews_collection.find({})
        return results


class Mutations(graphene.ObjectType):
    create_review = CreateReview.Field()
    # like_review = LikeReview.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)