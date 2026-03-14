from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from database import get_db
from .serializers import (
    CaseStatsSerializer, 
    DemographicsSerializer, 
    ComorbidityStatsSerializer, 
    TimeTrendSerializer
)

class GlobalStatsView(APIView):
    @extend_schema(responses={200: CaseStatsSerializer})
    def get(self, request):
        db = get_db()
        cases_collection = db['cases']
        
        total_cases = cases_collection.count_documents({})
        total_deaths = cases_collection.count_documents({"Is_Dead": 1})
        total_recovered = cases_collection.count_documents({"Is_Recovered": 1})
        active_cases = total_cases - total_deaths - total_recovered

        data = {
            "total_cases": total_cases,
            "total_deaths": total_deaths,
            "total_recovered": total_recovered,
            "active_cases": active_cases
        }
        return Response(data)

class DemographicStatsView(APIView):
    @extend_schema(responses={200: DemographicsSerializer})
    def get(self, request):
        db = get_db()
        cases_collection = db['cases']
        
        # Aggregate Country Distribution (Top 5)
        country_pipeline = [
            {"$group": {"_id": "$Country", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        countries = list(cases_collection.aggregate(country_pipeline))
        country_dist = {c['_id']: c['count'] for c in countries}

        # Sex Distribution
        sex_pipeline = [{"$group": {"_id": "$Sex", "count": {"$sum": 1}}}]
        sexes = list(cases_collection.aggregate(sex_pipeline))
        sex_dist = {s['_id']: s['count'] for s in sexes}

        # Age Group Distribution (Basic buckets)
        age_pipeline = [
            {
                "$bucket": {
                    "groupBy": "$Age",
                    "boundaries": [0, 18, 35, 50, 100],
                    "default": "Other",
                    "output": {"count": {"$sum": 1}}
                }
            }
        ]
        ages = list(cases_collection.aggregate(age_pipeline))
        age_map = {0: "0-18", 18: "19-35", 35: "36-50", 50: "51+"}
        age_dist = {age_map.get(a['_id'], "Other"): a['count'] for a in ages}

        return Response({
            "country_distribution": country_dist,
            "sex_distribution": sex_dist,
            "age_group_distribution": age_dist
        })

class ComorbidityStatsView(APIView):
    @extend_schema(responses={200: ComorbidityStatsSerializer})
    def get(self, request):
        db = get_db()
        cases_collection = db['cases']
        
        data = {
            "diabetes_cases": cases_collection.count_documents({"Has_Diabetes": 1}),
            "high_bp_cases": cases_collection.count_documents({"Has_High_BP": 1}),
            "heart_disease_cases": cases_collection.count_documents({"Has_Heart_Disease": 1}),
            "copd_cases": cases_collection.count_documents({"Has_COPD": 1})
        }
        return Response(data)

class TimeTrendView(APIView):
    @extend_schema(responses={200: TimeTrendSerializer(many=True)})
    def get(self, request):
        db = get_db()
        cases_collection = db['cases']
        
        # Aggregate by year from Report_Date
        pipeline = [
            {
                "$project": {
                    "year": {"$year": {"$toDate": "$Report_Date"}}
                }
            },
            {"$group": {"_id": "$year", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        trends = list(cases_collection.aggregate(pipeline))
        formatted_trends = [{"year": str(t['_id']), "count": t['count']} for t in trends if t['_id']]
        
        return Response(formatted_trends)
