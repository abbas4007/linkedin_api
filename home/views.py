from django.shortcuts import render,redirect
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.views import View
from .services import SearchService
from .serializers import LinkedInProfileSerializer



class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')

@api_view(['GET'])
def search_profiles(request) :
    try :
        keyword = request.GET.get('keyword', '').strip()

        filters = {}
        if request.GET.get('skill') :
            filters['skill'] = request.GET.get('skill')
        if request.GET.get('job_title') :
            filters['job_title'] = request.GET.get('job_title')
        if request.GET.get('company') :
            filters['company'] = request.GET.get('company')
        if request.GET.get('location') :
            filters['location'] = request.GET.get('location')
        if request.GET.get('industry') :
            filters['industry'] = request.GET.get('industry')

        results = SearchService.search_profiles(keyword, filters)

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        paginated_results = results[start :end]
        serializer = LinkedInProfileSerializer(paginated_results, many = True)

        return Response({
            'count' : results.count(),
            'page' : page,
            'page_size' : page_size,
            'results' : serializer.data
        })
    except Exception as e :
        import traceback
        return Response({
            'error' : str(e),
            'traceback' : traceback.format_exc()
        }, status = 500)

