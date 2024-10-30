from rest_framework.response import Response
from rest_framework import status


class ServiceResponse:
    def __init__(self, data=None, message=None, status=status.HTTP_200_OK):
        self.data = data
        self.message = message
        self.status = status

    def to_response(self) -> Response:
        """
        Convert to a DRF Response object.
        """
        response_data = {
            'status': self.status,
            'message': self.message,
            'data': self.data
        }
        return Response(response_data, status=self.status)
