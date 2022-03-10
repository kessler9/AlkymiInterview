import csv
import json
from io import StringIO
from distutils.util import strtobool
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from TemporalProcessor.models import File, Row, Temporal
from TemporalProcessor.serializers import FileSerializer, RowSerializer, TemporalSerializer
from .tasks import resolve_temporals
from .schema import FileApiViewSchema


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class RowViewSet(viewsets.ModelViewSet):
    queryset = Row.objects.all()
    serializer_class = RowSerializer

class TemporalViewSet(viewsets.ModelViewSet):
    queryset = Temporal.objects.all()
    serializer_class = TemporalSerializer


class FileApiView(APIView):
    parser_classes = [FileUploadParser]
    schema = FileApiViewSchema()

    def get(self, request, *args, **kwargs):
        serializer = FileSerializer(File.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        with StringIO(request.FILES['file'].read().decode()) as fh:
            _file = File()
            _file.save()
            with open(f'{_file.uid}.csv', 'w+') as handoff_file:
                reader = csv.reader(fh, quotechar='"')
                writer = csv.writer(handoff_file, quotechar='"')
                grab_header = strtobool(request.query_params['headerRow'])
                for row in reader:
                    if grab_header:
                        _file.header = json.dumps(row)
                        _file.save()
                        grab_header = False
                        continue
                    writer.writerow(row)
            resolve_temporals.delay(_file.uid)
            serializer = FileSerializer(_file)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class FileApiDetailView(APIView):
    def get(self, request, uid):
        serializer = FileSerializer(File.objects.get(uid=uid))
        return Response(serializer.data, status=status.HTTP_200_OK)
