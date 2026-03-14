from rest_framework import serializers

class CaseStatsSerializer(serializers.Serializer):
    total_cases = serializers.IntegerField()
    total_deaths = serializers.IntegerField()
    total_recovered = serializers.IntegerField()
    active_cases = serializers.IntegerField()

class DemographicsSerializer(serializers.Serializer):
    country_distribution = serializers.DictField()
    age_group_distribution = serializers.DictField()
    sex_distribution = serializers.DictField()

class ComorbidityStatsSerializer(serializers.Serializer):
    diabetes_cases = serializers.IntegerField()
    high_bp_cases = serializers.IntegerField()
    heart_disease_cases = serializers.IntegerField()
    copd_cases = serializers.IntegerField()

class TimeTrendSerializer(serializers.Serializer):
    year = serializers.CharField()
    count = serializers.IntegerField()
