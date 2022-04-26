from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random
import datetime
import time
from datetime import date, timedelta
import plotly.express as px
import numpy as np
import pandas as pd
from raceplotly.plots import barplot
import plotly.graph_objects as go
import os
from plotlychart.settings import BASE_DIR
import plotly


# Create your views here.

def chart(request):

	#bar graph
	ds= pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'covid.csv'))
	ds.drop(['NewCases', 'NewDeaths', 'NewRecovered'], 
              axis=1, inplace=True)
	fig = px.bar(ds.head(15), x='Country/Region', y='TotalCases', height=500,
              hover_data=['Country/Region', 'Continent'], color='TotalCases')
	fig.update_yaxes(showgrid=False),
	fig.update_layout(margin=dict(t=70, b=0, l=70, r=40),
                        hovermode="x unified",
                        xaxis_tickangle=-45,
                        xaxis_title=' ', yaxis_title=" ",
                        plot_bgcolor='#fff', paper_bgcolor='#fff',
                        title_font=dict(size=25, color='#000', family="Lato, sans-serif"),
                        font=dict(color='#000'),
                        title="Country/Region Wise Covid-19",
                        hoverlabel_font_color = '#000',
                        transition = {'duration': 8000}
                          )
	bargraph = fig.to_html(full_html=False, default_height=500, default_width=700)

	
	#line graph
	stockds = px.data.stocks()
	stockfig = px.line(stockds, x='date', y=["MSFT","GOOG",'FB',"AMZN"],title="Stock of Microsoft,GOOGLE,Facebook,Amazon per year")
	stockfig.update_layout(
			    xaxis_title="",
			    yaxis_title="",
			    legend_title="MNC's"
			    )

	stockgraph = stockfig.to_html(full_html=False, default_height=500, default_width=700)

	context = {'bargraph': bargraph,'stockgraph':stockgraph}
	return render(request,"chart.html",context)

@csrf_exempt
def scatter_chart_with_covid(request):
	response = []
	ds= pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'covid.csv'))
	ds.drop(['NewCases', 'NewDeaths', 'NewRecovered'], 
              axis=1, inplace=True)
	figscatter = px.scatter(ds, x='Continent',y='TotalCases', 
           hover_data=['Country/Region', 'Continent'], 
           color='TotalCases', size='TotalCases', size_max=80)
	figscatter.update_layout(hovermode="x unified", title="Country/Region Wise Covid-19",)
	scatter_chart_with_covid = figscatter.to_html(full_html=False, default_height=500, default_width=1500)
	
	response.append({'scatter_chart_with_covid':scatter_chart_with_covid})
	return JsonResponse(response,safe=False)

@csrf_exempt
def sunburust_chart_with_population(request):
	result = []
	world_countries_data = pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'india-districts-census-2011.csv'))
	world_countries_data["World"] = "World"
	figsunbrust = px.sunburst(world_countries_data,
                  path=["World", "State", "District"],
                  values='Population',
                  width=1500, height=500,
                  color_continuous_scale="RdYlGn",
                  color='Population',
                  title="India's Population Per State"
                  )
	
	figsunbrust.update_layout(hoverlabel_font_color='black')
	figsunbrust.update_traces(hovertemplate = "%{label}: <br>Population: %{value} </br>")
	sunburust_chart_with_population = figsunbrust.to_html(full_html=False, default_height=500, default_width=1500)
	
	result.append({'sunburust_chart_with_population':sunburust_chart_with_population})
	return JsonResponse(result,safe=False)

@csrf_exempt
def pie_chart_with_population(request):
	result = []
	world_countries_data = pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'india-districts-census-2011.csv'))
	world_countries_data["World"] = "World"
	
	dspie = world_countries_data.groupby(world_countries_data['State']).sum()
	dspie.reset_index(inplace=True)
	
	figpie = px.pie(dspie, values="Population", names="State",title="India's Population Per State") 
	figpie.update_layout( margin=dict(l=20, r=20, t=20, b=20),showlegend=False)
	
	pie_chart_with_population = figpie.to_html(full_html=False, default_height=500, default_width=1500)
	result.append({'pie_chart_with_population':pie_chart_with_population})
	return JsonResponse(result,safe=False)

@csrf_exempt
def stacked_bar_chart_with_population_by_gender(request):
	result = []
	world_countries_data = pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'india-districts-census-2011.csv'))
	world_countries_data["World"] = "World"
	dspie = world_countries_data.groupby(world_countries_data['State']).sum()
	dspie.reset_index(inplace=True)
	
	branches = dspie['State']
	fy = dspie['Male']
	sy = dspie['Female']
	
	trace1 = go.Bar(
	   x = branches,
	   y = fy,
	   name = 'Male'
	)
	trace2 = go.Bar(
	   x = branches,
	   y = sy,
	   name = 'Female'
	)
	
	data = [trace1, trace2]
	layout = go.Layout(barmode = 'group',title="India's Population Per State", xaxis_tickangle=-45)
	figbarstack = go.Figure(data = data, layout = layout)
	figbarstack.write_html(os.path.join(BASE_DIR, 'assets/dist', 'barstackgraph.html'))
	stacked_bar_chart_with_population_by_gender = figbarstack.to_html(full_html=False, default_height=500, default_width=1500)
	
	result.append({'stacked_bar_chart_with_population_by_gender':stacked_bar_chart_with_population_by_gender})
	return JsonResponse(result,safe=False)

@csrf_exempt
def line_chart_with_covid_data_country(request):
	result = []

	confirmed_dataset = pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'covid-19-confirmed-global.csv'))
	selected_countries=['India','China','Italy','Spain','France','Australia','Germany','Japan','Korea, South','Pakistan',
	                    'Russia','United Kingdom','Canada','Iran','Brazil','Singapore','South Africa','US']
	dataframe=confirmed_dataset[confirmed_dataset['Country/Region'].isin(selected_countries) ]
	ds = dataframe.groupby(confirmed_dataset['Country/Region']).sum().drop(['Lat','Long'], axis=1)
	df_t=ds.transpose()
	df_t.reset_index(inplace=True)
	df_t.rename(columns={'Country/Region':'Index_Col', 'index':'Dates'}, inplace=True)
	data=df_t.melt(id_vars=["Dates"], var_name="Country", value_name="Confirmed_Count")
	
	figdropdown = go.Figure()

	country_list = list(data['Country'].unique())
	data['Dates'] = pd.to_datetime(data['Dates'])
	data = data.loc[(data['Dates'] > '2020-12-31')]
 
	for country in country_list:
	    figdropdown.add_trace(
	        go.Scatter(
	            x = data['Dates'][data['Country']==country],
	            y = data['Confirmed_Count'][data['Country']==country],
	            name = country, visible = True
	        )
	    )
	    
	buttons = []

	for i, country in enumerate(country_list):
	    args = [False] * len(country_list)
	    args[i] = True
	    
	    button = dict(label = country,
	                  method = "update",
	                  args=[{"visible": args}])
	    
	    buttons.append(button)
	    
	figdropdown.update_layout(
	    updatemenus=[dict(
	                    active=-1,
	                    type="dropdown",
	                    buttons=buttons,
	                    x = 0,
	                    y = 1.2,
	                    xanchor = 'left',
	                    yanchor = 'bottom'
	                )], 
	    autosize=False,
	    width=1500,
	    height=800,
	    title="Country/Region Wise Covid-19",
	    xaxis_tickangle=-45,
	    
	)
	#figdropdown.write_html(os.path.join(BASE_DIR, 'assets/dist', 'linegraph.html'))
	line_chart_with_covid_data_country = figdropdown.to_html(full_html=False, default_height=700, default_width=1500)
	
	
	result.append({'line_chart_with_covid_data_country':line_chart_with_covid_data_country})

	return JsonResponse(result,safe=False)

@csrf_exempt
def bar_race_chart_with_covid_data_country(request):
	result = []

	confirmed_dataset = pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'covid-19-confirmed-global.csv'))
	selected_countries=['India','China','Italy','Spain','France','Australia','Germany','Japan','Korea, South','Pakistan',
	                    'Russia','United Kingdom','Canada','Iran','Brazil','Singapore','South Africa','US']
	df1=confirmed_dataset[confirmed_dataset['Country/Region'].isin(selected_countries) ]
	ds = df1.groupby(confirmed_dataset['Country/Region']).sum().drop(['Lat','Long'], axis=1)
	df_t=ds.transpose()
	df_t.reset_index(inplace=True)
	df_t.rename(columns={'Country/Region':'Index_Col', 'index':'Dates'}, inplace=True)
	data=df_t.melt(id_vars=["Dates"], var_name="Country", value_name="Confirmed_Count")
	
	
	country = data["Country"]
	confirmed = data["Confirmed_Count"]
	date = data['Dates']

	
	# Create Animated Bar Chart and store figure as fig
	figrace = px.bar(
	    data,
	    x=confirmed,
	    y=country,
	    color=country,
	    animation_frame=date,
	    animation_group=country,
	)
	figrace.update_layout(margin=dict(t=70, b=0, l=70, r=40),
                        xaxis_tickangle=-45,
                        xaxis_title=' ', yaxis_title=" ",
                        plot_bgcolor='#fff', paper_bgcolor='#fff',
                        title_font=dict(size=25, color='#000', family="Lato, sans-serif"),
                        font=dict(color='#000'),
                        title="Country/Region Wise Covid-19",
                        hoverlabel_font_color = '#000',
                        transition = {'duration': 8000},
                        showlegend=False
                          )
	# Save Chart and export to HTML
	#plotly.offline.plot(figrace, filename=os.path.join(BASE_DIR, 'assets/dist', 'covidrace.html'),auto_open = False)
	bar_race_chart_with_covid_data_country = figrace.to_html(full_html=False, default_height=700, default_width=1500)
	
	result.append({'bar_race_chart_with_covid_data_country':bar_race_chart_with_covid_data_country})


	return JsonResponse(result,safe=False)

@csrf_exempt
def bar_race_chart_with_covid_data_india(request):
	result = []
	dataframe = pd.read_csv('https://data.covid19india.org/csv/latest/states.csv')
	dataframe = dataframe.drop(columns=['Recovered','Deceased','Other','Tested'], axis=1)

	dataframe['Date'] = pd.to_datetime(dataframe['Date'], errors='coerce')
	dataframe.sort_values(by='Date', ascending=True, inplace=True)
	dataframe_filter = dataframe.groupby([dataframe['Date'].dt.strftime('%Y %B'),df['State']]).sum()
	dataframe_filter.reset_index(inplace=True)
	


	figure = px.bar(
            dataframe_filter,
            x=dataframe_filter['Confirmed'],
            y=dataframe_filter['State'],
            color=dataframe_filter['State'],
            animation_frame=dataframe_filter['Date'],
            animation_group=dataframe_filter['State'],
            )

	

	#Save Chart and export to HTML
	plotly.offline.plot(figure,filename=os.path.join(BASE_DIR, 'assets/dist', 'my_raceplot3.html'),auto_open = False)
	

	return JsonResponse(result,safe=False)
	




	