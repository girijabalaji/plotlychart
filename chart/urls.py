from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart, name='chart'),
    path('scatter_chart_with_covid', views.scatter_chart_with_covid, name='scatter_chart_with_covid'),
    path('sunburust_chart_with_population', views.sunburust_chart_with_population, name='sunburust_chart_with_population'),
    path('pie_chart_with_population', views.pie_chart_with_population, name='pie_chart_with_population'),
    path('stacked_bar_chart_with_population_by_gender', views.stacked_bar_chart_with_population_by_gender, name='stacked_bar_chart_with_population_by_gender'),
    path('line_chart_with_covid_data_country', views.line_chart_with_covid_data_country, name='line_chart_with_covid_data_country'),
    path('bar_race_chart_with_covid_data_country', views.bar_race_chart_with_covid_data_country, name='bar_race_chart_with_covid_data_country'),
    path('bar_race_chart_with_covid_data_india', views.bar_race_chart_with_covid_data_india, name='bar_race_chart_with_covid_data_india'),
   
]