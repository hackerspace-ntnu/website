from django.urls import path

from . import views

app_name = "userprofile"

urlpatterns = [
    path("", views.SelfProfileDetailView.as_view(), name="profile"),
    path("list/", views.ProfileListView.as_view(), name="members"),
    path("edit/", views.ProfileUpdateView.as_view(), name="edit_profile"),
    path("skills/", views.SelfSkillsView.as_view(), name="profile_skills"),
    path(
        "skills/<int:skill_pk>", views.SelfSkillsView.as_view(), name="profile_skills"
    ),
    path(
        "skills/category/<int:pk>",
        views.SkillsCategoryView.as_view(),
        name="profile_skills_category",
    ),
    path("<int:pk>/", views.ProfileDetailView.as_view(), name="profile_by_id"),
    path("<int:pk>/skills/", views.SkillsView.as_view(), name="profile_skills_by_id"),
    path(
        "<int:pk>/skills/<int:skill_pk>",
        views.SkillsView.as_view(),
        name="profile_skills_by_id",
    ),
    path(
        "<int:pk>/skills/approve/",
        views.ApproveSkillAPIView.as_view(),
        name="approve_skill_api_endpoint",
    ),
]
