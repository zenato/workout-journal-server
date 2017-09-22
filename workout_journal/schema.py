import graphene
import journal.schema
import journal.mutation


class Query(journal.schema.Query, graphene.ObjectType):
    pass


class Mutation(journal.mutation.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
