import graphene
from graphene.types.resolver import dict_resolver
from pymongo import MongoClient

client = MongoClient()
reviews_collection = client.goodreads.reviews


class Review(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    _id = graphene.ID()
    bookId = graphene.ID()
    rate = graphene.Float()
    text = graphene.String()
    likes = graphene.Int()


class Book(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    bookId = graphene.ID()
    workId = graphene.Int()
    title = graphene.String()
    originalTitle = graphene.String()
    isbn = graphene.String()
    isbn13 = graphene.Int()
    authors = graphene.List(graphene.String)
    publicationYear = graphene.Int()
    languageCode = graphene.String()
    avgRating = graphene.Float()
    ratingsCount = graphene.Int()
    workRatingsCount = graphene.Int()
    workTextReviewsCount = graphene.Int()
    ratings1 = graphene.Int()
    ratings2 = graphene.Int()
    ratings3 = graphene.Int()
    ratings4 = graphene.Int()
    ratings5 = graphene.Int()
    coverURL = graphene.String()
    smallCoverURL = graphene.String()
    description = graphene.String()
    reviews = graphene.List(Review)

    @classmethod
    def resolve_reviews(self, root, info, **kwargs):
        results = reviews_collection.find({'bookId': root['bookId']})
        return results