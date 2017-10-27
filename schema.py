import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Todo as TodoModel


class Todo(SQLAlchemyObjectType):

    class Meta:
        model = TodoModel



class Query(graphene.ObjectType):
    node = relay.Node.Field()
    todos = graphene.List(Todo)


    def resolve_todos(self, info):
        query = Todo.get_query(info)
        return query.all()



schema = graphene.Schema(query=Query, types=[Todo])
