import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Link, Vote
from users.schema import UserType
from django.db.models import Q


class LinkType(DjangoObjectType):
    test = graphene.String(source='get_test')

    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    links = graphene.List(LinkType, search=graphene.String(),
                          first=graphene.Int(), skip=graphene.Int(),)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        qs = Link.objects.all()
        search = kwargs.get('search')
        if search:
            filter_search = (
                    Q(url__icontains=search) |
                    Q(description__icontains=search)
            )
            qs = qs.filter(filter_search)
        skip = kwargs.get('skip')
        if skip:
            qs = qs[skip:]
        first = kwargs.get('first')
        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


class CreateLink(graphene.Mutation):
    """
    Output of mutation
    """
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        """
        Input of mutation
        """
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        """
        Create data and return data
        :param info:
        :param url:
        :param description:
        :return:
        """
        user = info.context.user or None

        link = Link(url=url, description=description, posted_by=user,)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()