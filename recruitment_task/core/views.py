from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.businesslogic.errors import CannotInvestIntoProjectException
from core.businesslogic.investing import invest_into_project
from core.models import Project, Investor
from core.serializers import ProjectSerializer, ProjectDetailsSerializer, InvestorSerializer, InvestorDetailsSerializer


class ProjectsView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailsSerializer

    def update(self, request, *args, **kwargs):
        project_to_update = self.get_object()
        if project_to_update.funded:
            return Response(data={"details": "Cannot edit funded project."}, status=status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(project_to_update, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class InvestorsView(generics.ListCreateAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InvestorDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Investor.objects.all()
    serializer_class = InvestorDetailsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        investor_to_update = self.get_object()
        serializer = self.get_serializer(investor_to_update, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class InvestIntoProject(APIView):
    def post(self, request, pk, project_id):
        investor = get_object_or_404(Investor, pk=pk)
        project_to_invest_into = get_object_or_404(Project, pk=project_id)

        try:
            invest_into_project(investor, project_to_invest_into)
        except CannotInvestIntoProjectException as e:
            return Response(data={"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        investor.refresh_from_db()
        project_to_invest_into.refresh_from_db()
        return Response(
            data={
                "funded_project": ProjectSerializer(instance=project_to_invest_into).data,
                "remaining_amount": investor.remaining_amount
            }
        )

class MatchingInvestorsForProjects(APIView):

    def get(self,request,pk):
        project = get_object_or_404(Project.objects, pk=pk)
        investors = project.matching_investors()
        data={
            "Matching investors for projects: ": investors
        }
        return Response(data=data)

class MatchingProjectsForInvestors(APIView):
    def get(self,request,pk):
        investor = get_object_or_404(Investor, pk=pk)
        projects = investor.matching_projects()
        data={
            "Matching projects for investors: ": projects
        }
        return Response(data=data)