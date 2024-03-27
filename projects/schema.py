import graphene
from graphene_django import DjangoObjectType
from .models import Test, Dimension, Pregunta, Proyecto, ProyectoTest, ProyectoDimension, ProyectoPregunta
from users.models import User

class TestType(DjangoObjectType):
    class Meta:
        model = Test
        fields = ('id', 'nombre', 'descripcion', 'autor', 'bibliografia', 'fecha_creacion', 'fecha_actualizacion')

class DimensionType(DjangoObjectType):
    class Meta:
        model = Dimension
        fields = ('id', 'id_test', 'nombre', 'descripcion', 'fecha_creacion', 'fecha_actualizacion')

class PreguntaType(DjangoObjectType):
    class Meta:
        model = Pregunta
        fields = ('id', 'id_dimension', 'pregunta', 'tipo_pregunta', 'valor_minimo', 'valor_maximo')

class ProyectoType(DjangoObjectType):
    class Meta:
        model = Proyecto
        fields = ('id', 'nombre', 'descripcion', 'id_usuario', 'fecha_creacion', 'fecha_actualizacion')

class ProyectoTestType(DjangoObjectType):
    class Meta:
        model = ProyectoTest
        fields = ('id', 'id_proyecto', 'id_test')

class ProyectoDimensionType(DjangoObjectType):
    class Meta:
        model = ProyectoDimension
        fields = ('id', 'id_proyecto', 'id_dimension')

class ProyectoPreguntaType(DjangoObjectType):
    class Meta:
        model = ProyectoPregunta
        fields = ('id', 'id_proyecto', 'id_pregunta')

class CreateTest(graphene.Mutation):
    test = graphene.Field(TestType)

    class Arguments:
        nombre = graphene.String(required=True)
        descripcion = graphene.String()
        autor = graphene.String()
        bibliografia = graphene.String()

    def mutate(self, info, nombre, descripcion=None, autor=None, bibliografia=None):
        test = Test(
            nombre=nombre,
            descripcion=descripcion,
            autor=autor,
            bibliografia=bibliografia
        )
        test.save()

        return CreateTest(test=test)
    
class UpdateTest(graphene.Mutation):
    test = graphene.Field(TestType)

    class Arguments:
        id = graphene.String(required=True)
        nombre = graphene.String()
        descripcion = graphene.String()
        autor = graphene.String()
        bibliografia = graphene.String()

    def mutate(self, info, id, nombre=None, descripcion=None, autor=None, bibliografia=None):
        test = Test.objects.get(pk=id)

        if nombre is not None:
            test.nombre = nombre
        if descripcion is not None:
            test.descripcion = descripcion
        if autor is not None:
            test.autor = autor
        if bibliografia is not None:
            test.bibliografia = bibliografia

        test.save()

        return UpdateTest(test=test)

class DeleteTest(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    def mutate(self, info, id):
        test = Test.objects.get(pk=id)
        test.delete()

        return DeleteTest(success=True)

    
class CreateDimension(graphene.Mutation):
    dimension = graphene.Field(DimensionType)

    class Arguments:
        id_test = graphene.String(required=True)
        nombre = graphene.String(required=True)
        descripcion = graphene.String()

    def mutate(self, info, id_test, nombre, descripcion=None):
        dimension = Dimension(
            id_test=Test.objects.get(pk=id_test),
            nombre=nombre,
            descripcion=descripcion
        )
        dimension.save()

        return CreateDimension(dimension=dimension)
    
class UpdateDimension(graphene.Mutation):
    dimension = graphene.Field(DimensionType)

    class Arguments:
        id = graphene.String(required=True)
        id_test = graphene.String()
        nombre = graphene.String()
        descripcion = graphene.String()

    def mutate(self, info, id, id_test=None, nombre=None, descripcion=None):
        dimension = Dimension.objects.get(pk=id)

        if id_test is not None:
            dimension.id_test = Test.objects.get(pk=id_test)
        if nombre is not None:
            dimension.nombre = nombre
        if descripcion is not None:
            dimension.descripcion = descripcion

        dimension.save()

        return UpdateDimension(dimension=dimension)

class DeleteDimension(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    def mutate(self, info, id):
        dimension = Dimension.objects.get(pk=id)
        dimension.delete()

        return DeleteDimension(success=True)

class CreatePregunta(graphene.Mutation):
    pregunta = graphene.Field(PreguntaType)

    class Arguments:
        id_dimension = graphene.String(required=True)
        pregunta = graphene.String(required=True)
        tipo_pregunta = graphene.String(required=True)
        valor_minimo = graphene.Int(required=True)
        valor_maximo = graphene.Int(required=True)

    def mutate(self, info, id_dimension, pregunta, tipo_pregunta, valor_minimo, valor_maximo):
        pregunta = Pregunta(
            id_dimension=Dimension.objects.get(pk=id_dimension),
            pregunta=pregunta,
            tipo_pregunta=tipo_pregunta,
            valor_minimo=valor_minimo,
            valor_maximo=valor_maximo
        )
        pregunta.save()

        return CreatePregunta(pregunta=pregunta)
    
class UpdatePregunta(graphene.Mutation):
    pregunta = graphene.Field(PreguntaType)

    class Arguments:
        id = graphene.String(required=True)
        id_dimension = graphene.String()
        pregunta = graphene.String()
        tipo_pregunta = graphene.String()
        valor_minimo = graphene.Int()
        valor_maximo = graphene.Int()

    def mutate(self, info, id, id_dimension=None, pregunta=None, tipo_pregunta=None, valor_minimo=None, valor_maximo=None):
        pregunta_instance = Pregunta.objects.get(pk=id)

        if id_dimension is not None:
            pregunta_instance.id_dimension = Dimension.objects.get(pk=id_dimension)
        if pregunta is not None:
            pregunta_instance.pregunta = pregunta
        if tipo_pregunta is not None:
            pregunta_instance.tipo_pregunta = tipo_pregunta
        if valor_minimo is not None:
            pregunta_instance.valor_minimo = valor_minimo
        if valor_maximo is not None:
            pregunta_instance.valor_maximo = valor_maximo

        pregunta_instance.save()

        return UpdatePregunta(pregunta=pregunta_instance)

class DeletePregunta(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.String(required=True)

    def mutate(self, info, id):
        pregunta_instance = Pregunta.objects.get(pk=id)
        pregunta_instance.delete()

        return DeletePregunta(success=True)


class CreateProyecto(graphene.Mutation):
    proyecto = graphene.Field(ProyectoType)

    class Arguments:
        nombre = graphene.String(required=True)
        descripcion = graphene.String()
        id_usuario = graphene.ID(required=True)

    def mutate(self, info, nombre, descripcion=None, id_usuario=None):
        proyecto = Proyecto(
            nombre=nombre,
            descripcion=descripcion,
            id_usuario=User.objects.get(pk=id_usuario)
        )
        proyecto.save()

        return CreateProyecto(proyecto=proyecto)
    
class DeleteProyecto(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        proyecto = Proyecto.objects.get(pk=id)
        proyecto.delete()

        return DeleteProyecto(success=True)

class UpdateProyecto(graphene.Mutation):
    proyecto = graphene.Field(ProyectoType)

    class Arguments:
        id = graphene.ID(required=True)
        nombre = graphene.String()
        descripcion = graphene.String()
        id_usuario = graphene.ID()

    def mutate(self, info, id, nombre=None, descripcion=None, id_usuario=None):
        proyecto = Proyecto.objects.get(pk=id)

        if nombre is not None:
            proyecto.nombre = nombre
        if descripcion is not None:
            proyecto.descripcion = descripcion
        if id_usuario is not None:
            proyecto.id_usuario = User.objects.get(pk=id_usuario)

        proyecto.save()

        return UpdateProyecto(proyecto=proyecto)

class CreateProyectoTest(graphene.Mutation):
    proyecto_test = graphene.Field(ProyectoTestType)

    class Arguments:
        id_proyecto = graphene.ID(required=True)
        id_test = graphene.ID(required=True)

    def mutate(self, info, id_proyecto, id_test):
        proyecto_test = ProyectoTest(
            id_proyecto=Proyecto.objects.get(pk=id_proyecto),
            id_test=Test.objects.get(pk=id_test)
        )
        proyecto_test.save()

        return CreateProyectoTest(proyecto_test=proyecto_test)
    
class DeleteProyectoTest(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        proyecto_test = ProyectoTest.objects.get(pk=id)
        proyecto_test.delete()

        return DeleteProyectoTest(success=True)

class CreateProyectoDimension(graphene.Mutation):
    proyecto_dimension = graphene.Field(ProyectoDimensionType)

    class Arguments:
        id_proyecto = graphene.ID(required=True)
        id_dimension = graphene.ID(required=True)

    def mutate(self, info, id_proyecto, id_dimension):
        proyecto_dimension = ProyectoDimension(
            id_proyecto=Proyecto.objects.get(pk=id_proyecto),
            id_dimension=Dimension.objects.get(pk=id_dimension)
        )
        proyecto_dimension.save()

        return CreateProyectoDimension(proyecto_dimension=proyecto_dimension)
    
class DeleteProyectoDimension(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        proyecto_dimension = ProyectoDimension.objects.get(pk=id)
        proyecto_dimension.delete()

        return DeleteProyectoDimension(success=True)
    
class CreateProyectoPregunta(graphene.Mutation):
    proyecto_pregunta = graphene.Field(ProyectoPreguntaType)

    class Arguments:
        id_proyecto = graphene.ID(required=True)
        id_pregunta = graphene.ID(required=True)

    def mutate(self, info, id_proyecto, id_pregunta):
        proyecto_pregunta = ProyectoPregunta(
            id_proyecto=Proyecto.objects.get(pk=id_proyecto),
            id_pregunta=Pregunta.objects.get(pk=id_pregunta)
        )
        proyecto_pregunta.save()

        return CreateProyectoPregunta(proyecto_pregunta=proyecto_pregunta)

class DeleteProyectoPregunta(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        proyecto_pregunta = ProyectoPregunta.objects.get(pk=id)
        proyecto_pregunta.delete()

        return DeleteProyectoPregunta(success=True)
    
class Mutation(graphene.ObjectType):
    create_test = CreateTest.Field()
    delete_test = DeleteTest.Field()
    update_test = UpdateTest.Field()
    create_dimension = CreateDimension.Field()
    delete_dimension = DeleteDimension.Field()
    update_dimension = UpdateDimension.Field()
    create_pregunta = CreatePregunta.Field()
    delete_pregunta = DeletePregunta.Field()
    update_pregunta = UpdatePregunta.Field()
    create_proyecto = CreateProyecto.Field()
    delete_proyecto = DeleteProyecto.Field()
    update_proyecto = UpdateProyecto.Field()
    create_proyecto_test = CreateProyectoTest.Field()
    delete_proyecto_test = DeleteProyectoTest.Field()
    create_proyecto_dimension = CreateProyectoDimension.Field()
    delete_proyecto_dimension = DeleteProyectoDimension.Field()
    create_proyecto_pregunta = CreateProyectoPregunta.Field()
    delete_proyecto_pregunta = DeleteProyectoPregunta.Field()

class Query(graphene.ObjectType):
    all_tests = graphene.List(TestType)
    test_by_id = graphene.Field(TestType, id=graphene.ID())
    all_dimensions = graphene.List(DimensionType)
    dimension_by_id = graphene.Field(DimensionType, id=graphene.ID())
    all_preguntas = graphene.List(PreguntaType)
    pregunta_by_id = graphene.Field(PreguntaType, id=graphene.ID())
    all_proyectos = graphene.List(ProyectoType)
    proyecto_by_id = graphene.Field(ProyectoType, id=graphene.ID())
    all_proyecto_tests = graphene.List(ProyectoTestType)
    all_proyecto_dimensions = graphene.List(ProyectoDimensionType)
    all_proyecto_preguntas = graphene.List(ProyectoPreguntaType)
    proyectos_by_user = graphene.List(ProyectoType, id_usuario=graphene.ID())
    dimensiones_by_test = graphene.List(DimensionType, id_test=graphene.ID())
    preguntas_by_test = graphene.List(PreguntaType, id_test=graphene.ID())

    def resolve_all_tests(self, info, **kwargs):
        return Test.objects.all()
    
    def resolve_test_by_id(self, info, id):
        return Test.objects.get(pk=id)
    
    def resolve_all_dimensions(self, info, **kwargs):
        return Dimension.objects.all()
    
    def resolve_dimension_by_id(self, info, id):
        return Dimension.objects.get(pk=id)
    
    def resolve_all_preguntas(self, info, **kwargs):
        return Pregunta.objects.all()
    
    def resolve_pregunta_by_id(self, info, id):
        return Pregunta.objects.get(pk=id)
    
    def resolve_all_proyectos(self, info, **kwargs):
        return Proyecto.objects.all()
    
    def resolve_proyecto_by_id(self, info, id):
        return Proyecto.objects.get(pk=id)
    
    def resolve_all_proyecto_tests(self, info, **kwargs):
        return ProyectoTest.objects.all()
    
    def resolve_all_proyecto_dimensions(self, info, **kwargs):
        return ProyectoDimension.objects.all()
    
    def resolve_all_proyecto_preguntas(self, info, **kwargs):
        return ProyectoPregunta.objects.all()
    
    def resolve_proyectos_by_user(self, info, id_usuario):
        return Proyecto.objects.filter(id_usuario=id_usuario)
    
    def resolve_dimensiones_by_test(self, info, id_test):
        return Dimension.objects.filter(id_test=id_test)
    
    def resolve_preguntas_by_test(self, info, id_test):
        return Pregunta.objects.filter(id_dimension__id_test=id_test)
