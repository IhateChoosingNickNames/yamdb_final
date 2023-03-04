from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    RetrievePatchMeView, RetrieveTokenView, ReviewViewSet,
                    SignUpViewSet, TitleViewSet, UsersViewSet)

router_v1 = DefaultRouter()
router_v1.register(r"users", UsersViewSet)
router_v1.register(r"auth/signup", SignUpViewSet, basename="signup")
router_v1.register("categories", CategoryViewSet)
router_v1.register("genres", GenreViewSet)
router_v1.register("titles", TitleViewSet, basename="title")
router_v1.register(
    r"titles/(?P<title_id>[1-9]\d*)/reviews", ReviewViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>[1-9]\d*)/reviews/(?P<review_id>[1-9]\d*)/comments",
    CommentViewSet,
    basename="review_comments",
)


urlpatterns = [
    path("v1/users/me/", RetrievePatchMeView.as_view()),
    path("v1/", include(router_v1.urls)),
    path("v1/auth/token/", RetrieveTokenView.as_view()),
]
