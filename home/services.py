from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import LinkedInProfile


class SearchService :
    @staticmethod
    def search_profiles(keyword=None, filters=None) :
        queryset = LinkedInProfile.objects.all()


        if keyword and keyword.strip() :
            # simple search
            queryset = queryset.filter(
                Q(full_name__icontains = keyword) |
                Q(search_text__icontains = keyword) |
                Q(job_title__icontains = keyword) |
                Q(job_company_name__icontains = keyword) |
                Q(location__icontains = keyword) |
                Q(skills__icontains = keyword)
            )

        #search with filters
        if filters :

            if filters.get('skill') :
                queryset = queryset.filter(skills__icontains = filters['skill'])

            if filters.get('job_title') :
                queryset = queryset.filter(job_title__icontains = filters['job_title'])

            if filters.get('company') :
                queryset = queryset.filter(job_company_name__icontains = filters['company'])


            if filters.get('location') :
                queryset = queryset.filter(location__icontains = filters['location'])

            if filters.get('industry') :
                queryset = queryset.filter(industry__icontains = filters['industry'])

        return queryset