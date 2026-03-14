from django.urls import path
from .views import GlobalStatsView, DemographicStatsView, ComorbidityStatsView, TimeTrendView

urlpatterns = [
    path('stats/global/', GlobalStatsView.as_view(), name='global-stats'),
    path('stats/demographics/', DemographicStatsView.as_view(), name='demographic-stats'),
    path('stats/comorbidities/', ComorbidityStatsView.as_view(), name='comorbidity-stats'),
    path('stats/trends/', TimeTrendView.as_view(), name='time-trends'),
]
