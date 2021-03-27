from django.urls import path
from . import views

app_name = 'pushkin'
urlpatterns = [
    path("", views.index, name="index"),

    path("author_create", views.AuthorCreate.as_view(), name="author_create"),
    path("author_update/<int:pk>", views.AuthorUpdate.as_view(), name="author_update"),
    path("author_delete/<int:pk>", views.author_delete, name="author_delete"),
    path("author_detail/<int:pk>", views.AuthorDetail.as_view(), name="author_detail"),
    path("author_list", views.AuthorList.as_view(), name="author_list"),
    path("author_list/<str:mode>", views.AuthorList.as_view(), name="author_list"),

    path("author_info/<int:id>", views.author_info, name="author_info"),
    path("author_info/<int:id>/<str:mode>", views.author_info, name="author_info"),
    path("author_info/<int:id>/<str:mode>/<str:w_re>", views.author_info, name="author_info"),
    path("active_count/", views.active_count, name="active_count"),

    path("writing_create", views.WritingCreate.as_view(), name="writing_create"),
    path("writing_update/<int:pk>", views.WritingUpdate.as_view(), name="writing_update"),
    path("writing_delete/<int:pk>", views.writing_delete, name="writing_delete"),
    path("writing_detail/<int:pk>", views.WritingDetail.as_view(), name="writing_detail"),

    path("writing_info/<int:pk>", views.WritingInfo.as_view(), name="writing_info"),
    path("writing_read/<int:pk>", views.WritingRead.as_view(), name="writing_read"),
    path("writing_list", views.WritingList.as_view(), name="writing_list"),

    # path("plot_writings_stats/<str:param>", views.plot_writings_stats, name="plot_writings_stats"),
    # path("plot_authors_stats/<str:param>", views.plot_authors_stats, name="plot_authors_stats"),
    path("plot_stats/<str:mode>/<str:param>", views.plot_stats, name="plot_stats"),

    path("all_active", views.all_active, name="all_active"),
    path("all_passive", views.all_passive, name="all_passive"),
    path("all_active/<str:mode>", views.all_active, name="all_active"),
    path("all_passive/<str:mode>", views.all_passive, name="all_passive"),

    path("author_active", views.author_active, name="author_active"),
    path("author_passive", views.author_passive, name="author_passive"),

    path("author_active/<int:id>", views.author_active, name="author_active"),
    path("author_passive/<int:id>", views.author_passive, name="author_passive"),
    path("author_active/<int:id>/<str:mode>", views.author_active, name="author_active"),
    path("author_passive/<int:id>/<str:mode>", views.author_passive, name="author_passive"),

    path("writing_check_active", views.writing_check_active, name="writing_check_active"),
    path("writing_set_selected_genre", views.writing_set_selected_genre, name="writing_set_selected_genre"),

    path("delete_selected", views.delete_selected, name="delete_selected"),

    path("search", views.search, name="search"),

    path("sample_create", views.sample_create, name="sample_create"),

    path("markovify_author/<int:id>", views.markovify_author, name="markovify_author"),
    path("markovify_writing/<int:id>", views.markovify_writing, name="markovify_writing"),

    path("library_view", views.library_view, name="library_view"),
    path("library_info", views.library_info, name="library_info"),
    path("library_clean", views.library_clean, name="library_clean"),
    path("library_load", views.library_load, name="library_load"),
]