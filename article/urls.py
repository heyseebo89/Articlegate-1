from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('',views.home, name='article-home'),
    path('aboutus/',views.aboutus, name='article-aboutus'),
    path('article/<str:title>/<int:article_id>/',views.fullArticle, name='fullArticle'),
    path('add-article/',views.addArticle, name='addArticle'),
    path('edit-article/<str:title>/<int:article_id>/',views.editArticle, name='editArticle'),
    path('view-profile/<str:username>/',views.viewProfile, name='viewProfile'),
    path('article/search/',views.search, name='search'),
    # path('tag/<slug:tag_slug>/',views.home, name='post_tag')
    path('article/tag/<str:tagname>',views.tagName,name='tagName'),
]