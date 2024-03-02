import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.hashers import make_password
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_admin', 'institution')

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        institution = graphene.String()
        is_admin = graphene.Boolean() 

    def mutate(self, info, username, first_name, last_name, email, password, institution=None,is_admin=False):
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),  
            institution=institution,
            is_admin=is_admin
        )
        user.save()

        return CreateUser(user=user)
    
class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()

        return DeleteUser(success=True)
    
class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()
        institution = graphene.String()
        is_admin = graphene.Boolean()

    def mutate(self, info, id, username=None, first_name=None, last_name=None, email=None, password=None, institution=None, is_admin=None):
        user = User.objects.get(pk=id)

        if username is not None:
            user.username = username
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        if password is not None:
            user.password = make_password(password)
        if institution is not None:
            user.institution = institution
        if is_admin is not None:
            user.is_admin = is_admin

        user.save()

        return UpdateUser(user=user)

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID())

    def resolve_user_by_id(self, info, id):
        return User.objects.get(pk=id)

    def resolve_all_users(self, info):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
