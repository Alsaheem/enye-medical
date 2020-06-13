import graphene
from graphql import GraphQLError
from .models import Data
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType
from .helpers import  generate_username
############# User Type
class UserType(DjangoObjectType):
  class Meta:
    model = User
    # only_fields = ('id','email','password','username')

############# Data Type
class DataType(DjangoObjectType):
    class Meta:
        model = Data

############# Queries
class Query(graphene.ObjectType):
  searches = graphene.List(DataType)
  my_data = graphene.List(DataType,email=graphene.String(required=True))
  users = graphene.List(UserType)

  def resolve_my_data(self, info, email):
    user = User.objects.get(email= email)
    return Data.objects.filter(user = user)

  def resolve_searches(self, info):
    return Data.objects.all()

  def resolve_users(self, info):
    return User.objects.all()

#################Data Create Field#########################

class CreateData(graphene.Mutation):
  data = graphene.Field(DataType)

  class Arguments:
    title = graphene.String(required=True)
    radius = graphene.String(required=True)
    email = graphene.String(required=True)

  def mutate(self,info,title,radius,email):
    user = User.objects.get(email=email)
    if user.is_anonymous:
        raise GraphQLError('Login to add data')
    data = Data(title=title,radius=radius,user=user)
    data.save()
    return CreateData(data=data)

#################User Create Field#########################
class CreateUser(graphene.Mutation):
  user = graphene.Field(UserType)
  class Arguments:
    email = graphene.String(required=True)

  def mutate(self,info,email):
    username = generate_username(email)
    password = generate_username(email)
    user = User(username=username,password=password,email=email)
    user.set_password(password)
    user.save()
    return CreateUser(user=user)


class Mutation(graphene.ObjectType):
  create_user = CreateUser.Field()
  create_data = CreateData.Field()
