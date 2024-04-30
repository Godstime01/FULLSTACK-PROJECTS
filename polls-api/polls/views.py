from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import Poll, Vote, Choice
from .serializers import (
    PollSerializer,
    VoteSerializer,
    ChoiceSerializer,
    UserSerializer,
)


class PollList(ListCreateAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    # def get(self, request):
    #     polls = Poll.objects.all()
    #     serializer = PollSerializer(polls, many=True).data
    #     return Response(serializer)


class PollDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    # def get(self, request, pk):
    #     poll = get_object_or_404(Poll, pk=pk)
    #     serializer = PollSerializer(poll).data
    #     return Response(serializer)


class ChoiceList(ListCreateAPIView):

    def get_queryset(self):
        queryset = Choice.objects.filter(poll__id=self.kwargs["pk"])
        return queryset

    serializer_class = ChoiceSerializer


class CreateVote(CreateAPIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {"choice": choice_pk, "poll": pk, "voted_by": voted_by}

        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)