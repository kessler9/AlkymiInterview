import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


class FileApiViewSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        return super().get_manual_fields(path, method) + [
            coreapi.Field(
                "attachment",
                required=True,
                location="body",
                schema=coreschema.String(description='Use headers Content-Disposition: attachment; filename=Alkymi.csv and send attachment with a different tool or curl directive --data-binary'),
            ),
            coreapi.Field(
                'headerRow',
                required=False,
                location='query',
                schema=coreschema.String(
                    description='true/false whether or not to expect a header for the input csv'
                )
            )
        ] if method == 'POST' else list()
