import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import json 
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import config
import contentdash as cd
from datetime import datetime

pwd= config.db_pwd
host=config.db_host
engine = create_engine('postgresql://postgres:'+pwd+'@'+host+'/datathon')


yellow_2 = pd.read_sql('select * from transport.yellow_counts', engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
yellow_2['neig'] = [a[:2] for a in yellow_2['nta']]

green = pd.read_sql('select * from transport.green_counts', engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
green['neig'] = [a[:2] for a in green['nta']]

uber = pd.read_sql('select * from transport.uber_counts', engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
uber['neig'] = [a[:2] for a in uber['nta']]


ntas = pd.read_sql('select * from other.centroids', engine.connect(), parse_dates=('OCCURRED_ON_DATE',)).sort_values(by=['borough','nta_code']).reset_index()
ntas = ntas.append({'nta_code':'ALL','borough':'all', 'nta_name':'all','lon':-73.95754,'lat':40.709471},ignore_index=True)

years = pd.DataFrame([[2014,2015],[2014,2015]]).T
years.columns=['Year','Number']

months = pd.DataFrame([['April','May','June','July','August','September'],[4,5,6,7,8,9]]).T
months.columns=['Month','Number']

days = pd.DataFrame([['Monday','Tusday','Wednesday','Thursday','Friday','Saturday','Sunday'],[1,2,3,4,5,6,0]]).T
days.columns=['Day','Number']

transport_color = pd.DataFrame([['count_ye',0.2],['count_gr',0.5],['count',1]])

groups = ['year','month','dow','hour','neig','nta']
ama_1 = yellow_2.groupby(groups)['count'].sum()
ver_1 = green.groupby(groups)['count'].sum()
ube_1 = uber.groupby(groups)['count'].sum()

merged = pd.merge(pd.merge(ama_1, ver_1, on=(groups), how ='outer',suffixes=('_ye','_gr')), ube_1, on =(groups), how='outer', suffixes=('','_ub')).fillna(0)

token = 'pk.eyJ1IjoibmV3dXNlcmZvcmV2ZXIiLCJhIjoiY2o2M3d1dTZiMGZobzMzbnp2Z2NiN3lmdyJ9.cQFKe3F3ovbfxTsM9E0ZSQ'

shp_path = 'C:\\Users\\HP\\Documents\\GitHub\\personal\\Datathon\\Ny_uno\\'
shp_path_c = 'C:\\Users\\lenovo\\Documents\\Github_Personal\\personal\\Datathon\\Ny_uno\\'
shp = '/home/ec2-user/datathon/ny/'
with open(shp +'Ny_geojson.geojson') as f:
    geojson = json.loads(f.read())
    2
for nta in range(len(geojson['features'])):
    geojson['features'][nta]['id']=geojson['features'][nta]['properties']['ntacode']

yellow_2=0
green=0
uber=0

app = dash.Dash(__name__) 
app.layout=html.Div(children=[
                        html.Header(children=[
                                        html.Div(children=[
                                                    html.H1(' Transportation in New York by NTAs'),
                                                    html.H2('Which transportation is easier to take in NY by NTAs and hour of the day')]
                                                )
                                             ]
                                    ),
                        html.Nav(className='floating-menu', 
                                 children=[
                                         html.H3('Contents'),
                                         html.A('• Dashboard',href='#cosa'),
                                         html.A('• Topic question', href='#Topic'),
                                         html.A('• Cleaning process',href='#Cleaning'),
                                         html.A('• Exploratory analysis',href='#expl'),
                                         html.A('• Conlusions',href='#concl')                                                
                                          ]
                                ),                                        
                        html.Div(className='mapa',
                                 children=[
                                         html.Div(className='row',
                                                  children=[
                                                          html.Div(className='column',
                                                                   children=[
                                                                           html.P("1. Select the year",id='cosa'),
                                                                           dcc.Dropdown(
                                                                                  id = 'year',
                                                                                  options = [{'label':years['Year'][a], 'value':years['Number'][a]} for a in range(len(years))],
                                                                                  value = 2014,
                                                                                  clearable = False,
                                                                                  optionHeight = 35)
                                                                           ]),
                                                          html.Div(className='column',
                                                                   children=[
                                                                           html.P("1. Select the month"),
                                                                           dcc.Dropdown(
                                                                                  id = 'month',
                                                                                  options = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(len(months))],
                                                                                  value = 4,
                                                                                  clearable=False,
                                                                                  disabled = False,
                                                                                  optionHeight=35)
                                                                           ]),
                                                          html.Div(className='column',
                                                                   children=[
                                                                           html.P("3. Select the day of the week"),
                                                                           dcc.Dropdown(
                                                                                  id = 'dow',
                                                                                  options = [{'label':days['Day'][a], 'value':days['Number'][a]} for a in range(len(days))],
                                                                                  value = 1,
                                                                                  clearable = False,
                                                                                  disabled = False,
                                                                                  optionHeight=35)
                                                                           ]),
                                                          html.Div(className='column',
                                                                   children=[
                                                                           html.P("3. Select an hour"),
                                                                           dcc.Dropdown(
                                                                                  id = 'hour',
                                                                                  options = [{'label':a, 'value':a} for a in np.arange(24)],
                                                                                  value = 12,
                                                                                  clearable = False,
                                                                                  disabled = False,
                                                                                  optionHeight=35)
                                                                           ])
                                                          ]),
                                         html.Div(className='row',
                                                  children=[
                                                          html.Div(className='column2',
                                                                   children=[
                                                                           html.P("1. Select the borough you're at",id='step'),
                                                                           dcc.Dropdown(
                                                                                  id = 'borough',
                                                                                  options = [{'label':a, 'value':a} for a in list(ntas['borough'].unique())],
                                                                                  value='all',
                                                                                  clearable=False,
                                                                                  optionHeight=35)
                                                                           ]),
                                                          html.Div(className='column2',
                                                                   children=[
                                                                           html.P("1. Select the nta you're at"),
                                                                           dcc.Dropdown(
                                                                                  id = 'nta',
                                                                                  options = [{'label':ntas['nta_name'][a], 'value':ntas['nta_code'][a]} for a in range(len(ntas))],
                                                                                  value='ALL',
                                                                                  clearable=False,
                                                                                  disabled = True,
                                                                                  optionHeight=35)
                                                                           ]),                                                          
                                                          ]),
                                           dcc.Graph(
                                                       id='map-plot',
                                                       figure={ 
                                                          'data': [go.Choroplethmapbox(
                                                                      geojson=geojson,
                                                                      locations = merged.loc[2014,4,1,12].index.get_level_values('nta'),
                                                                      z = [transport_color[transport_color[0]==a][1].values[0] for a in merged.loc[2014,4,1,12].div(merged.loc[2014,4,1,12].sum(axis=1),axis=0).idxmax(axis=1).values],
                                                                      text = ntas['nta_name'],
                                                                      colorscale=[[0,'rgb( 255, 243, 0 )'],
                                                                                  [0.33,'rgb( 255, 243, 0 )'],
                                                                                  [0.33,'rgb( 38, 126, 45)'],
                                                                                  [0.66,'rgb( 38, 126, 45)'],
                                                                                  [0.66,'rgb( 0,0,0)'],
                                                                                  [1,'rgb(0,0,0)']],
                                                                      colorbar_title="Thousands USD",
                                                                      colorbar={'x':0, 
                                                                                #'tickfont':{'color' :'rgb(200,200,200)'},
                                                                                'thickness':10,
                                                                                'tickvals':[0.16,0.5,0.83],
                                                                                'ticktext':['Yellow cab','Green cab','Uber'],
                                                                                'tickwidth':3,
                                                                                'tickfont':{'size':15}
                                                                                })],
                                                          'layout': go.Layout(
                                                                      mapbox_style="outdoors",
                                                                      mapbox_accesstoken=token,
                                                                      mapbox_zoom=9,
                                                                      margin = {'l' : 0, 'r' : 0, 'b' : 0, 't' : 0, 'pad' : 0},
                                                                      mapbox_center = {"lat": 40.709471, "lon": -73.95754}
                                                                      )
                                                              }
                                                        ),
                                            html.Div(className='row',
                                                     children=[
                                                             html.Div(className='column3',
                                                                      children=[
                                                                              html.H2(children="Yellow cabs"),
                                                                              html.H3(children='',id='yellow')
                                                                              ]),
                                                             html.Div(className='column3',
                                                                      children=[
                                                                              html.H2(children="Green cabs"),
                                                                              html.H3(children='',id='green')
                                                                          ]),
                                                             html.Div(className='column3',
                                                                      children=[
                                                                              html.H2(children="Uber"),
                                                                              html.H3(children='',id='uber')
                                                                          ]),
                                                             ]),
                                            html.Div(className='contents',
                                                     children=[
                                                             html.Div(className='descript topic',
                                                                      children=[
                                                                              html.H3('Topic Quesition',className='vertical_tex')]),
                                                             html.Div(className='cont',
                                                                      children=[
                                                                              html.A(id='Topic'),
                                                                              html.H3('Topic Question'),
                                                                              html.P(cd.intro_1),
                                                                              #html.Br(),
                                                                              html.P(cd.intro_2)
                                                                               ]
                                                                      ),
                                                             html.Div(className='descript cleani',
                                                                      children=[
                                                                              html.H3('Cleansing',className='vertical_tex')
                                                                              ]
                                                                      ),
                                                             html.Div(className='cont',
                                                                      children=[
                                                                              html.A(id='Cleaning'),
                                                                              html.H3('Cleaning Process'),
                                                                              html.Img(src='/assets/outside.png',className='imag'),
                                                                              html.P(cd.cleaning),
                                                                              html.P(cd.cleaning_1),
                                                                              html.P(cd.cleaning_2),                                                                              
                                                                              html.P(cd.cleaning_3),
                                                                              html.P(cd.cleaning_4)
                                                                              ]
                                                                      ),
                                                             html.Div(className='descript expl',
                                                                      children=[
                                                                              html.H3('Exploratory Data Analysis', className='vertical_tex')
                                                                              ]
                                                                      ),
                                                             html.Div(className='cont',
                                                                      children=[
                                                                              html.A(id='expl'),
                                                                              html.H3('Exploratory data analysis'),
                                                                              html.P(cd.expl),
                                                                              html.P(cd.expl_1),
                                                                              html.Img(src='/assets/all45.png',className='imag_t'),
                                                                              html.P(cd.expl_2),
                                                                              html.P(cd.expl_3),
                                                                              html.Img(src='/assets/boro.svg',className='imag_t'),
                                                                              html.P(cd.expl_4),
                                                                              html.P(cd.expl_5),
                                                                              html.Img(src='/assets/dow.png',className='imag'),
                                                                              html.P(cd.expl_6),
                                                                              html.P(cd.expl_7),
                                                                              html.P(cd.expl_8),
                                                                              html.Img(src='/assets/man.png',className='imag_t'),
                                                                              html.Img(src='/assets/mang.png',className='imag'),
                                                                              html.P(cd.expl_9),
                                                                              html.P(cd.expl_10),
                                                                              ]
                                                                      ),
                                                             html.Div(className='descript concl',
                                                                      children=[
                                                                              html.H3('Conlcusions', className='vertical_tex')
                                                                              ]
                                                                      ),
                                                             html.Div(className='cont',
                                                                      children=[
                                                                              html.A(id='concl'),
                                                                              html.H3('Conlcusions'),
                                                                              html.P(cd.conc),
                                                                              html.P(cd.conc_1),
                                                                              html.P(cd.conc_3),
                                                                              html.P(cd.conc_4),
                                                                              html.P(cd.conc_5),                                                                              
                                                                              ]
                                                                      )
                                      ])
                                            
                                         ]
                                )
                              ]
                     )               

@app.callback([dash.dependencies.Output('nta','options'),
                dash.dependencies.Output('map-plot','figure'),
                dash.dependencies.Output('nta','disabled'),
                dash.dependencies.Output('hour','disabled'),
                dash.dependencies.Output('yellow','children'),
                dash.dependencies.Output('green','children'),
                dash.dependencies.Output('uber','children'),
                dash.dependencies.Output('month','options'),
                dash.dependencies.Output('hour','options'),],
              [dash.dependencies.Input('borough','value'),
                dash.dependencies.Input('nta','value'),
                dash.dependencies.Input('hour','value'),
                dash.dependencies.Input('year','value'),
                dash.dependencies.Input('month','value'),
                dash.dependencies.Input('dow','value')])



def aval_ntas(bor,nta,hour,year,month,dow):
    fil = merged.loc[year,month,dow,hour]
    base = fil.div(fil.sum(axis=1),axis=0)
    if bor=='all':
        a = [{'label':ntas['nta_name'][a], 'value':ntas['nta_code'][a]} for a in range(len(ntas)) if ntas['nta_code'][a] in base.index.get_level_values('nta')]
        center = {"lat": 40.709471, "lon": -73.95754}
        loc = base.index.get_level_values('nta')
        temp = [transport_color[transport_color[0]==a][1].values[0] for a in base.idxmax(axis=1)]
        temp.append(0)
        temp.append(1)
        zeta = temp
        zoom = 9
        dis_n = True
        dis_h = False
        b = ''
        c = ''
        d = ''
        if year==2015:
            e = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(3)]
        else:
            e = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(len(months))]
        f = [{'label':a, 'value':a} for a in np.arange(24)]
    elif (bor!='all' and nta=='ALL') or (bor!='all' and bor!=ntas['borough'][ntas['nta_code']==nta].values[0]):
        a = [{'label':ntas['nta_name'][a], 'value':ntas['nta_code'][a]} for a in list(ntas['nta_code'][ntas['borough']==bor].index) if ntas['nta_code'][a] in base.index.get_level_values('nta')]
        nta_in_bor = list(ntas['nta_code'][ntas['borough']==bor])
        data = base[base.index.get_level_values('nta').isin(nta_in_bor)].idxmax(axis=1)
        loc = list(data.index.get_level_values('nta'))
        temp = [transport_color[transport_color[0]==a][1].values[0] for a in data]
        temp.append(0)
        temp.append(1)
        zeta = temp
        center = {'lat': ntas['lat'][ntas['borough']==bor].mean(),'lon':ntas['lon'][ntas['borough']==bor].mean()}
        zoom = 10
        dis_n = False
        dis_h = False        
        b = ''
        c = ''
        d = ''
        if year==2015:
            e = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(3)]
        else:
            e = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(len(months))]
        f = [{'label':a, 'value':a} for a in np.arange(24)]
    elif bor!='all' and nta!='ALL':
        a = [{'label':ntas['nta_name'][a], 'value':ntas['nta_code'][a]} for a in list(ntas['nta_code'][ntas['borough']==bor].index) if ntas['nta_code'][a] in base.index.get_level_values('nta')]
        nta_in_bor = list(ntas['nta_code'][ntas['borough']==bor])
        data = base[base.index.get_level_values('nta').isin(nta_in_bor)].idxmax(axis=1)
        loc = list(data.index.get_level_values('nta'))
        temp = [transport_color[transport_color[0]==a][1].values[0] for a in data]
        temp.append(0)
        temp.append(1)
        zeta = temp
        center = {'lat': ntas['lat'][ntas['nta_code']==nta].values[0],'lon':ntas['lon'][ntas['nta_code']==nta].values[0]}
        zoom = 12
        dis_n = False
        dis_h = False
        b = str(int(base.loc[base.index.get_level_values('nta')==nta]['count_ye'].values[0]*100))+'%'
        c = str(int(base.loc[base.index.get_level_values('nta')==nta]['count_gr'].values[0]*100))+'%'
        d = str(int(base.loc[base.index.get_level_values('nta')==nta]['count'].values[0]*100))+'%'
        if year==2015:
            e = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(3)]
        else:
            e = [{'label':months['Month'][a], 'value':months['Number'][a]} for a in range(len(months))]
        fil_1 = merged.loc[year,month,dow]
        f = [{'label':a, 'value':a} for a in list(fil_1.loc[fil_1.index.get_level_values('nta')==nta].index.get_level_values('hour').sort_values())]
        
    return [a,
            {'data': [go.Choroplethmapbox(
                        geojson=geojson,
                        locations = loc,
                        z = zeta,
                        #text = states_grouped['Sales_State'],
                        colorscale=[[0,'rgb( 255, 243, 0 )'],
                                    [0.33,'rgb( 255, 243, 0 )'],
                                    [0.33,'rgb( 38, 126, 45)'],
                                    [0.66,'rgb( 38, 126, 45)'],
                                    [0.66,'rgb( 0,0,0)'],
                                    [1,'rgb(0,0,0)']],
                        colorbar_title="Recommended cab",
                        colorbar={'x':0, 
                                  #'tickfont':{'color' :'rgb(200,200,200)'},
                                  'thickness':10,
                                  'tickvals':[0.16,0.5,0.83],
                                  'ticktext':['Yellow cab','Green cab','Uber'],
                                  'tickwidth':3,
                                  'tickfont':{'size':15}}
                        )],
              'layout': go.Layout(
                          mapbox_style="outdoors",
                          mapbox_accesstoken=token,
                          mapbox_zoom = zoom,
                          margin = {'l' : 0, 'r' : 0, 'b' : 0, 't' : 0, 'pad' : 0},
                          mapbox_center = center)},
            dis_n,
            dis_h,b,c,d,e,f]

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port='5555')

        