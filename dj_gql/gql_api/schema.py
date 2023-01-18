import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

class UserType(DjangoObjectType):
    class Meta:
        model=User
        fields=('id','first_name','last_name','username','email')


class PostType(DjangoObjectType):
    class Meta:
        model=Post
        fields=('id','author','title','details') 

class CreateUser(graphene.Mutation):
    class Arguments:
        first_name=graphene.String(required=True)
        last_name=graphene.String(required=True)
        username=graphene.String(required=True)
        email=graphene.String(required=True)
        password=graphene.String(required=True)

    user=graphene.Field(UserType)

    @classmethod
    def mutate(cls,root,info,first_name,last_name,username,email,password):
        try:
            user=User(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.save()
            return CreateUser(user=user)
        except:
            return None

class UpdateUser(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
        first_name=graphene.String(required=True)
        last_name=graphene.String(required=True)
        username=graphene.String(required=True)
        email=graphene.String(required=True)

    user=graphene.Field(UserType)

    @classmethod
    def mutate(cls,root,info,id,first_name,last_name,username,email):
        try:
            user=User.objects.get(id=id)
            user.username=username
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.save()
            return UpdateUser(user=user)
        except User.DoesNotExist:
            return None



class DeleteUser(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
    user=graphene.Field(UserType)

    @classmethod
    def mutate(cls,root,info,id):
        try:
            user=User.objects.get(id=id)
            user.delete()
            return DeleteUser(success=True, message='User deleted successfully')
        except User.DoesNotExist:
            return None

class CreatePost(LoginRequiredMixin,graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)
        details=graphene.String(required=True)

    post=graphene.Field(PostType)

    @classmethod
    def mutate(cls,root,info,title,details):
        try:
            user=info.context.user
            print(user)
            if user.is_anonymous:
                raise Exception("You must be logged in to create a post")
            post=Post(title=title,details=details,author=user)
            post.save()
            return CreatePost(post=post)
        except:
            return None

class UpatePost(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
        title=graphene.String(required=True)
        details=graphene.String(required=True)

    post=graphene.Field(PostType)

    @classmethod
    def mutate(cls,root,info,id,title,details):
        try:
            post=Post.objects.get(id=id)
            post.title=title
            post.details=details
            post.save()
            return UpatePost(post=post)
        except Post.DoesNotExist:
            return None

class DeletePost(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    post=graphene.Field(PostType)

    @classmethod
    def mutate(cls,root,info,id):
        try:
            post=Post.objects.get(id=id)
            post.delete()
            return DeletePost(success=True, message='Post deleted successfully')
        except Post.DoesNotExist:
            return None

# For Queries 
class Query(graphene.ObjectType):
    all_users=graphene.List(UserType)
    all_posts=graphene.List(PostType)
    user_by_name=graphene.Field(UserType,name=graphene.String(required=True))

    def resolve_all_users(root,info):
        return User.objects.all()

    def resolve_all_posts(root,info):
        return Post.objects.all()

    def resolve_user_by_name(root,info,name):
        try:
            user=User.objects.get(username=name)
            return user
        except User.DoesNotExist:
            return None

# for mutations
class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()
    update_user=UpdateUser.Field()
    delete_user=DeleteUser.Field()
    create_post=CreatePost.Field()
    update_post=UpatePost.Field()
    delete_post=DeletePost.Field()

schema=graphene.Schema(query=Query,mutation=Mutation)