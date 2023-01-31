from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:entry>", views.entry, name="entry"),
    path("<str:entry>", views.entry, name="entry"),
    # path("edit/<str:entry>", views.edit, name="edit"),
    path("edit/", views.edit, name="edit"),
    path("new/", views.new, name="new"),
    path("randomPage/", views.randomPage, name="randomPage"),
    path("search/", views.search, name="search")
]
