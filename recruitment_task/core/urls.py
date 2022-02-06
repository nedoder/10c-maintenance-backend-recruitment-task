from django.urls import path
from core import views

urlpatterns = [
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("projects/<int:pk>/", views.ProjectDetailsView.as_view(), name="project-details"),
    path("investors/", views.InvestorsView.as_view(), name="investors"),
    path("investors/<int:pk>/", views.InvestorDetailsView.as_view(), name="investor-details"),
    path("investors/<int:pk>/invest/<int:project_id>/", views.InvestIntoProject.as_view(), name="invest-into-project"),
    path("investors/<int:pk>/matches/", views.MatchingProjectsForInvestors.as_view(), name="projects-for-investors"),
    path("projects/<int:pk>/matches/", views.MatchingInvestorsForProjects.as_view(), name="investors-for-project"),
]
