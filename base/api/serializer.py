#this is a class that takes a certin model we wnat to serialized or object and turn it into a json object
#basicly it takes our python object and turn it into a json data
'''all we need to do is to firt import serializer, create a class  specify the model and the fields we want to
serialize'''

from rest_framework.serializers import ModelSerializer

from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields= '__all__'