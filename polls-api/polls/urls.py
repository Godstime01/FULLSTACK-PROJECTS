from django.urls import path
from .views import PollList, PollDetail, ChoiceList, CreateVote, UserCreate, LoginView

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Polls API")


urlpatterns = [
    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:pk>/", PollDetail.as_view(), name="polls-detail"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path(
        "polls/<int:pk>/choices/<int:choice_pk>/vote/",
        CreateVote.as_view(),
        name="create_vote",
    ),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("docs/", schema_view),
]
