from flask_potion import ModelResource, fields
from models import Todo


class TodoResource(ModelResource):
    class Meta:
        model = Todo
        # id_field_class = fields.String()