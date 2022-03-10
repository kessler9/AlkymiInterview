from rest_framework import serializers
from TemporalProcessor.models import File, Row, Temporal
import json


class TemporalSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['row'] = representation['row_index']
        del representation['row_index']
        return representation

    class Meta:
        model = Temporal
        fields = ['row', 'column', 'startIdx', 'endIdx', 'text', 'temporal', 'row_index']


class ArrayRelatedField(serializers.RelatedField):
    def __init__(self, **kwargs):
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, instance):
        return json.loads(instance.raw_row)


class RowSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['raw_row'] = json.loads(representation['raw_row'])
        return representation

    class Meta:
        model = Row
        fields = ['raw_row']


class FileSerializer(serializers.ModelSerializer):
    rows = ArrayRelatedField(many=True)
    temporals = TemporalSerializer(many=True)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['header'] = json.loads(representation['header']) if representation['header'] else None
        return representation

    class Meta:
        model = File
        fields = ['uid', 'header', 'rows', 'temporals']

