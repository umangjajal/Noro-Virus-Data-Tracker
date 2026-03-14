from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from drf_spectacular.utils import extend_schema
from database import get_db
from .serializers import FeedbackSerializer

class FeedbackCreateView(APIView):
    @extend_schema(request=FeedbackSerializer, responses={201: FeedbackSerializer})
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            db = get_db()
            feedback_collection = db['feedback']
            
            data = serializer.validated_data
            data['created_at'] = datetime.now()
            
            feedback_collection.insert_one(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
