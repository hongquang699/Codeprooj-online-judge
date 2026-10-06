from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.rejudge import RejudgeService

class RejudgeAPIView(APIView):
    def post(self, request, submission_id):
        # Admin or moderator or authorized user
        ok, msg = RejudgeService.rejudge(submission_id, async_judge=True)
        if not ok:
            return Response({'error': msg}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'message': msg, 'submission_id': submission_id}, status=status.HTTP_200_OK)
