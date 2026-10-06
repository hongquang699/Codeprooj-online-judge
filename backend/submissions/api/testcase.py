from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.result import ResultService

class SubmissionTestCaseAPIView(APIView):
    def get(self, request, submission_id):
        cases = ResultService.get_testcases(submission_id)
        return Response({'submission_id': submission_id, 'testcases': cases}, status=status.HTTP_200_OK)
