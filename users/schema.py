from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Profile
from .constants import M, W


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        sex = graphene.String()
        age = graphene.Int()

    def mutate(self, info, **kwargs):
        user = get_user_model()(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
        )
        user.set_password(kwargs.get('password'))
        user.save()
        age = kwargs.get('age', None)
        sex = kwargs.get('sex', None)
        if age and sex:
            profile = Profile.objects.get(user=user)
            if age:
                profile.age = age
            if sex:
                if sex != M and sex != W:
                    raise GraphQLError('Sex must be M or W')
                profile.sex = sex
            profile.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
