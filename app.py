import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import pymysql
from sqlalchemy import create_engine 
import plotly.figure_factory as ff
import plotly.express as px
import warnings
import json
from dbsettings import db_server, db_user, db_password

warnings.simplefilter(action='ignore', category=FutureWarning)

mysqlEngine = create_engine('mysql+pymysql://' + db_user + ':' + db_password + '@' + db_server)

dfProgs = pd.read_sql_table('v_prog_list', mysqlEngine) 
dfProgLeagues = pd.read_sql_table('v_prog_league_list', mysqlEngine) 
dfProgTeams = pd.read_sql_table('v_prog_team_list', mysqlEngine) 
dfHitCareer = pd.read_sql_table('v_hitcareer', mysqlEngine) 
dfPitCareer = pd.read_sql_table('v_pitcareer', mysqlEngine) 
dfHitters = pd.read_sql_table('v_hitroster', mysqlEngine) 
dfPitchers = pd.read_sql_table('v_pitroster', mysqlEngine) 
dfStandings = pd.read_sql_table('v_division_standings', mysqlEngine) 
dfTmWLSpl = pd.read_sql_table('v_team_win_loss_splits', mysqlEngine) 
dfTmLog = pd.read_sql_table('v_team_log', mysqlEngine) 
dfDraftSum = pd.read_sql_table('v_draft_summary', mysqlEngine)
#dfFAHitters = pd.read_sql_table('v_hit_fa', mysqlEngine) 
#dfFAPitchers = pd.read_sql_table('v_pit_fa', mysqlEngine) 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets=[dbc.themes.BOOTSTRAP]
external_stylesheets = ['assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


progressions = dfProgs.set_index('ID').squeeze().to_dict()
rows = []
hitter_stats = ['Salary', 'OPS', 'RC650', 'L_OPS', 'R_OPS', '$/PA', '$100/WAR', 'futWAR', 'CurrWAR']
pitcher_stats = ['Salary', 'OOPS', 'RC600', 'L_OPS', 'R_OPS', '$/IP', '$100/WAR', 'futWAR', 'CurrWAR', 'FIP', 'WHIP']

min_slider = 1946

pos_colors = [(0.0, "#CACAAA"), (0.1, "#CACAAA "),
              (0.1, "#D7B3A0"), (0.2, "#D7B3A0"),
              (0.2, "#DBCBD8"), (0.3, "#DBCBD8"),
              (0.3, "#BA979C"), (0.4, "#BA979C"),
              (0.4, "#986261"), (0.5, "#986261"),
              (0.5, "#772E25"), (0.6, "#772E25"),
              (0.6, "#A7BBEC"), (0.7, "#A7BBEC"),
              (0.7, "#6785B5"), (0.8, "#6785B5"),
              (0.8, "#264f7d"), (0.9, "#264f7d"),
              (0.9, "#E6E6E6"), (1.0, "#E6E6E6")]

pit_colors = [(0.00, "#CACAAA"), (0.33, "#CACAAA "),
              (0.33, "#BA979C"), (0.67, "#BA979C"),
              (0.67, "#6785B5"), (1.0, "#6785B5")]

hit_cols = [
    {"name": ['Catalog', 'Player'], "id": 'Player'},
    {"name": ['Catalog', 'Salary'], "id": 'Salary'},
    {"name": ['Catalog', 'Pos'], "id": 'Pos'},
    {"name": ['Catalog', 'B'], "id": 'B'},
    {"name": ['Catalog', 'Season'], "id": 'Season'},
    {"name": ['Overall', 'Injury'], "id": 'Injury'},
    {"name": ['Overall', 'PA'], "id": 'PA'},
    {"name": ['Overall', 'AVG'], "id": 'AVG'},
    {"name": ['Overall', 'OBP'], "id": 'OBP'},
    {"name": ['Overall', 'SLG'], "id": 'SLG'},
    {"name": ['Overall', 'OPS'], "id": 'OPS'},
    {"name": ['Overall', 'RC650'], "id": 'RC650'},
    {"name": ['Overall', 'RC6'], "id": 'RC6'},
    {"name": ['Hit Ratings', 'Clutch'], "id": 'Clutch'},
    {"name": ['Hit Ratings', 'BS'], "id": 'BS'},
    {"name": ['Hit Ratings', 'BH'], "id": 'BH'},
    {"name": ['Hit Ratings', 'R'], "id": 'R'},
    {"name": ['Hit Ratings', 'S'], "id": 'S'},
    {"name": ['Hit Ratings', 'J'], "id": 'J'},
    {"name": ['Vs. LHP', 'Avg'], "id": 'L_Avg'},
    {"name": ['Vs. LHP', 'OBP'], "id": 'L_OBP'},
    {"name": ['Vs. LHP', 'SLG'], "id": 'L_SLG'},
    {"name": ['Vs. LHP', 'OPS'], "id": 'L_OPS'},
    {"name": ['Vs. LHP', 'RC6'], "id": 'L_RC6'},
    {"name": ['Vs. LHP', 'PA'], "id": 'L_PA'},
    {"name": ['Vs. LHP', '2B'], "id": 'L_2B'},
    {"name": ['Vs. LHP', '3B'], "id": 'L_3B'},
    {"name": ['Vs. LHP', 'HR'], "id": 'L_HR'},
    {"name": ['Vs. LHP', 'BB'], "id": 'L_BB'},
    {"name": ['Vs. RHP', 'Avg'], "id": 'R_Avg'},
    {"name": ['Vs. RHP', 'OBP'], "id": 'R_OBP'},
    {"name": ['Vs. RHP', 'SLG'], "id": 'R_SLG'},
    {"name": ['Vs. RHP', 'OPS'], "id": 'R_OPS'},
    {"name": ['Vs. RHP', 'RC6'], "id": 'R_RC6'},
    {"name": ['Vs. RHP', 'PA'], "id": 'R_PA'},
    {"name": ['Vs. RHP', '2B'], "id": 'R_2B'},
    {"name": ['Vs. RHP', '3B'], "id": 'R_3B'},
    {"name": ['Vs. RHP', 'HR'], "id": 'R_HR'},
    {"name": ['Vs. RHP', 'BB'], "id": 'R_BB'},
    {"name": ['C', 'E'], "id": 'C_E'},
    {"name": ['C', 'R'], "id": 'C_R'},
    {"name": ['C', 'PB'], "id": 'C_PB'},
    {"name": ['C', 'Th'], "id": 'C_Th'},
    {"name": ['1B', 'E'], "id": '1B_E'},
    {"name": ['1B', 'R'], "id": '1B_R'},
    {"name": ['2B', 'E'], "id": '2B_E'},
    {"name": ['2B', 'R'], "id": '2B_R'},
    {"name": ['3B', 'E'], "id": '3B_E'},
    {"name": ['3B', 'R'], "id": '3B_R'},
    {"name": ['SS', 'E'], "id": 'SS_E'},
    {"name": ['SS', 'R'], "id": 'SS_R'},
    {"name": ['LF', 'E'], "id": 'LF_E'},
    {"name": ['LF', 'R'], "id": 'LF_R'},
    {"name": ['CF', 'E'], "id": 'CF_E'},
    {"name": ['CF', 'R'], "id": 'CF_R'},
    {"name": ['RF', 'E'], "id": 'RF_E'},
    {"name": ['RF', 'R'], "id": 'RF_R'},
    {"name": ['OF', 'Th'], "id": 'OF_T'},
    {"name": ['', '$/PA'], "id": '$/PA'},
    {"name": ['WAR', 'futWAR'], "id": 'futWAR'},
    {"name": ['WAR', 'ContWar'], "id": 'ContWar'},
    {"name": ['WAR', 'NPWAR'], "id": 'NPWAR'},
    {"name": ['WAR', 'CurrWAR'], "id": 'CurrWAR'}
]
pit_cols = [
    {"name": ['Catalog', 'Player'], "id": 'Player'},
    {"name": ['Catalog', 'Salary'], "id": 'Salary'},
    {"name": ['Catalog', 'Pos'], "id": 'Pos'},
    {"name": ['Catalog', 'T'], "id": 'T'},
    {"name": ['Catalog', 'Season'], "id": 'Season'},
    {"name": ['Overall', 'Injury'], "id": 'Injury'},
    {"name": ['Overall', 'IP'], "id": 'IP'},
    {"name": ['Overall', 'ERA'], "id": 'ERA'},
    {"name": ['Overall', 'H9'], "id": 'H9'},
    {"name": ['Overall', 'BB9'], "id": 'BB9'},
    {"name": ['Overall', 'K9'], "id": 'K9'},
    {"name": ['Overall', 'HR9'], "id": 'HR9'},
    {"name": ['Overall', 'WHIP'], "id": 'WHIP'},
    {"name": ['Overall', 'RC6'], "id": 'RC600'},
    {"name": ['Overall', 'FIP'], "id": 'FIP'},
    {"name": ['Overall', 'OAVG'], "id": 'OAVG'},
    {"name": ['Overall', 'OOBP'], "id": 'OOBP'},
    {"name": ['Overall', 'OSLG'], "id": 'OSLG'},
    {"name": ['Overall', 'OOPS'], "id": 'OOPS'},
    {"name": ['Overall', 'GBpct'], "id": 'GBpct'},
    {"name": ['Pitch Ratings', 'SD'], "id": 'SD'},
    {"name": ['Pitch Ratings', 'RD'], "id": 'RD'},
    {"name": ['Pitch Ratings', 'H'], "id": 'H'},
    {"name": ['Pitch Ratings', 'Jam'], "id": 'Jam'},
    {"name": ['Pitch Ratings', 'E'], "id": 'P_E'},
    {"name": ['Pitch Ratings', 'R'], "id": 'P_R'},
    {"name": ['Vs. LHP', 'Avg'], "id": 'L_Avg'},
    {"name": ['Vs. LHP', 'OBP'], "id": 'L_OBP'},
    {"name": ['Vs. LHP', 'SLG'], "id": 'L_SLG'},
    {"name": ['Vs. LHP', 'OPS'], "id": 'L_OPS'},
    {"name": ['Vs. LHP', 'RC6'], "id": 'L_RC6'},
    {"name": ['Vs. LHP', '2B'], "id": 'L_2B'},
    {"name": ['Vs. LHP', '3B'], "id": 'L_3B'},
    {"name": ['Vs. LHP', 'HR'], "id": 'L_HR'},
    {"name": ['Vs. LHP', 'BB'], "id": 'L_BB'},
    {"name": ['Vs. RHP', 'Avg'], "id": 'R_Avg'},
    {"name": ['Vs. RHP', 'OBP'], "id": 'R_OBP'},
    {"name": ['Vs. RHP', 'SLG'], "id": 'R_SLG'},
    {"name": ['Vs. RHP', 'OPS'], "id": 'R_OPS'},
    {"name": ['Vs. RHP', 'RC6'], "id": 'R_RC6'},
    {"name": ['Vs. RHP', '2B'], "id": 'R_2B'},
    {"name": ['Vs. RHP', '3B'], "id": 'R_3B'},
    {"name": ['Vs. RHP', 'HR'], "id": 'R_HR'},
    {"name": ['Vs. RHP', 'BB'], "id": 'R_BB'},
    {"name": ['', '$/IP'], "id": '$/IP'},
    {"name": ['WAR', 'futWAR'], "id": 'futWAR'},
    {"name": ['WAR', 'ContWar'], "id": 'ContWar'},
    {"name": ['WAR', 'NPWAR'], "id": 'NPWAR'},
    {"name": ['WAR', 'CurrWAR'], "id": 'CurrWAR'}
]
standings_cols = [
    {"name": ['', 'Team'], "id": 'Team'},
    {"name": ['', 'Post'], "id": 'Post'},
    {"name": ['', 'W'], "id": 'W'},
    {"name": ['', 'L'], "id": 'L'},
    {"name": ['', 'Pct'], "id": 'Pct'},
    {"name": ['', 'GB'], "id": 'GB'},
    {"name": ['Runs', 'RS'], "id": 'RS'},
    {"name": ['Runs', 'RA'], "id": 'RA'},
    {"name": ['Runs', 'Diff'], "id": 'RDif'},
    {"name": ['Expected', 'Pct'], "id": 'XPct'},
    {"name": ['Expected', 'W'], "id": 'XW'},
    {"name": ['Expected', 'L'], "id": 'XL'},
    {"name": ['Expected', 'VsX'], "id": 'WvX'},
    {"name": ['One-Run', 'W'], "id": '1RW'},
    {"name": ['One-Run', 'L'], "id": '1RL'},
    {"name": ['One-Run', 'Pct'], "id": '1RPct'}
]
sty_align_left = [
    {
        'if': {'column_id': c},
        'textAlign': 'left'
    } for c in ['Team_Link', 'Player', 'Pos', 'Team', 'Post']
]
sty_cell_shade = [
    {
        'if': {'column_id': c},
        'backgroundColor': '#ececec'
    } for c in [
        'Injury', 'PA', 'AVG', 'OBP', 'SLG', 'OPS', 'RC650', 'RC6', 
        'L_Avg', 'L_OBP', 'L_SLG', 'L_OPS', 'L_RC6', 
        'R_Avg', 'R_OBP', 'R_SLG', 'R_OPS', 'R_RC6', 
        'C_E', 'C_R', 'C_PB', 'C_Th', '2B_E', '2B_R', 
        'SS_E', 'SS_R', 'CF_E', 'CF_R', 'OF_T', 
        'futWAR', 'ContWar', 'NPWAR', 'CurrWAR',
        'IP', 'ERA', 'H9', 'BB9', 'K9', 'HR9', 
        'OAVG', 'OOBP', 'OSLG', 'OOPS', 'GBpct',
        'RS', 'RA', 'RDif', 'H9', '1RW', '1RL', '1RPct'
    ]
]
sty_WAR = [ 
    {
        'if': {'column_id': str(x), 'filter_query': '{{{0}}} < 0'.format(x)},
        'color': 'red',
    } for x in ['futWAR', 'ContWar', 'NPWAR', 'CurrWAR']
]
sty_team_width = [
    {'if': {'column_id': 'Team'},
    'width': '200px'},
]
sty_cell_font = {
    'fontSize':12, 
    'font-family':'Arial',
    'width': '40px'
}
sty_standings_font = {
    'fontSize':14, 
    'font-family':'Arial',
    'width': '40px'
}
sty_header = {
    'backgroundColor': '#264f7d',
    'fontWeight': 'bold',
    'border': '1px solid white',
    'color': 'white'
}

app.layout = html.Div([
    html.Div(className="tb_pad", children=[
        dcc.Tabs(id='tabs', style={'font-family': 'Arial', 'font-size': '14px'}, value='hit_career', children=[
            dcc.Tab(id='hit_career', label='Hitters', value='hit_career', children=[
                html.Div(className="tb_pad", children=[
                    dash_table.DataTable(
                        id='hit_car_tab',
                        columns=hit_cols,
                        style_cell=sty_cell_font,
                        style_cell_conditional=sty_align_left + sty_cell_shade,
                        style_data_conditional=sty_WAR,            
                        style_header=sty_header,
                        style_as_list_view=True,
                        data=dfHitCareer.to_dict('records'),
                        merge_duplicate_headers=True,
                        filter_action="native",

                    )
                ])
            ]),
            dcc.Tab(id='pit_career', label='Pitchers', value='pit_career', children=[
                html.Div(className="tb_pad", children=[
                    dash_table.DataTable(
                        id='pit_car_tab',
                        columns=pit_cols,
                        style_cell=sty_cell_font,
                        style_cell_conditional=sty_align_left + sty_cell_shade,
                        style_data_conditional=sty_WAR,            
                        style_header=sty_header,
                        style_as_list_view=True,
                        data=dfPitCareer.to_dict('records'),
                        merge_duplicate_headers=True,
                        filter_action="native",

                    )
                ])
            ]),
            dcc.Tab(id='hit_comp', label='Hitter Comparison', value='hit_comp', children=[
                html.Div(className="tb_pad", children=[
                    html.Div(className="l_pad", children=[
                        dcc.Dropdown(
                            id='xaxis_column', 
                            style={'width': '280px'},
                            options=[{'label': i, 'value': i} for i in hitter_stats],
                            value='Salary'
                        ),
                    ],
                    style={'width': '15%', 'display': 'inline-flex'}
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='yaxis_column',
                            style={'width': '280px'},
                            options=[{'label': i, 'value': i} for i in hitter_stats],
                            value='RC650'
                        ),
                    ],
                    style={'width': '15%', 'display': 'inline-flex'}
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='positions',
                            style={'width': '280px'},
                            options=[
                                {'label': 'All', 'value': 'All'},
                                {'label': 'C', 'value': '2'},
                                {'label': '1B', 'value': '3'},
                                {'label': '2B', 'value': '4'},
                                {'label': '3B', 'value': '5'},
                                {'label': 'SS', 'value': '6'},
                                {'label': 'LF', 'value': '7'},
                                {'label': 'CF', 'value': '8'},
                                {'label': 'RF', 'value': '9'},
                                {'label': 'DH/PH/PR', 'value': '0'}
                            ],
                            value='All',
                            multi=True
                        ),
                    ],
                    style={'width': '15%', 'display': 'inline-flex'}
                    ),
                    html.Div([
                        "Min. PA: ", 
                        dcc.Input(id='min_pa', value='100', type='text')
                    ],
                    style={'width': '15%', 'display': 'inline-block'}
                    ),
                    html.Div([
                        "Season: ", 
                        dcc.Input(id='season', value='1946', type='text')
                    ],
                    style={'width': '15%', 'display': 'inline-block'}
                    )
                ], 
                style={'borderBottom': 'thin lightgrey solid', 'font-family': 'Arial, Helvetica, sans-serif', 'font-size': '12px', 'font-weight': 'bold'}
                ),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='hitter_graphic',
                            #hoverData={'points': [{'customdata': 'Player'}]}
                            hoverData={'points': [{'customdata': 'Musial, Stan'}]}
                        )     
                    ], 
                    style={'width': '59%', 'display': 'inline-block', 'padding': '0 20'}
                    ),
                    html.Div([
                        dcc.Graph(id='PA_time_series'),
                        dcc.Graph(id='WAR_time_series'),
                        dcc.Graph(id='OPS_time_series'),
                    ], 
                    style={'width': '39%', 'display': 'inline-block'}
                    )
                ]),
                
#                html.Div([
#                    dcc.Markdown("""
#                        **Hover Data**
#
#                        Mouse over values in the graph.
#                    """),
#                    html.Pre(id='hover-data')
#                ], className='three columns')


            ]),
            dcc.Tab(id='pit_comp', label='Pitcher Comparison', value='pit_comp', children=[
                html.Div(className="tb_pad", children=[
                    html.Div(className="l_pad", children=[
                        dcc.Dropdown(
                            id='pit_xaxis_column', 
                            style={'width': '280px'},
                            options=[{'label': i, 'value': i} for i in pitcher_stats],
                            value='Salary'
                        ),
                    ],
                    style={'width': '15%', 'display': 'inline-flex'}
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='pit_yaxis_column',
                            style={'width': '280px'},
                            options=[{'label': i, 'value': i} for i in pitcher_stats],
                            value='FIP'
                        ),
                    ],
                    style={'width': '15%', 'display': 'inline-flex'}
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='pit_types',
                            style={'width': '280px'},
                            options=[
                                {'label': 'All', 'value': 'All'},
                                {'label': 'SP', 'value': '1'},
                                {'label': 'RP', 'value': '2'},
                                {'label': 'CL', 'value': '3'}
                            ],
                            value='All',
                            multi=True
                        ),
                    ],
                    style={'width': '15%', 'display': 'inline-flex'}
                    ),
                    html.Div([
                        "Min. IP: ", 
                        dcc.Input(id='min_ip', value='40', type='text')
                    ],
                    style={'width': '15%', 'display': 'inline-block'}
                    ),
                    html.Div([
                        "Season: ", 
                        dcc.Input(id='pit_season', value='1946', type='text')
                    ],
                    style={'width': '15%', 'display': 'inline-block'}
                    )
                ], 
                style={'font-family': 'Arial, Helvetica, sans-serif', 'font-size': '12px', 'font-weight': 'bold'}
                ),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='pitcher_graphic',
                            #hoverData={'points': [{'customdata': 'Player'}]}
                            hoverData={'points': [{'customdata': 'Spahn, Warren'}]}
                        )     
                    ], 
                    style={'width': '59%', 'display': 'inline-block', 'padding': '0 20'}
                    ),
                    html.Div([
                        dcc.Graph(id='pit_IP_time_series'),
                        dcc.Graph(id='pit_WAR_time_series'),
                        dcc.Graph(id='pit_OPS_time_series'),
                    ], 
                    style={'width': '39%', 'display': 'inline-block'}
                    )
                   
                ])
            ]),
            dcc.Tab(id='progs', label='Progressions', value='progs', children=[
                html.Div(className="tb_pad", 
                children=[
                    html.Div([
                        dcc.Dropdown(
                            id='progression', 
                            style={'width': '280px'},
                            options=[{'label': v, 'value': k} for k, v in progressions.items()],
                            value='bbb'
                        )
                    ],
                    style={'width': '15%', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Dropdown(
                            id='league', 
                            style={'width': '280px'}
                        )
                    ], 
                    style={'width': '15%', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Dropdown(
                            id='team', 
                            style={'width': '280px'}
                        )
                    ], 
                    style={'width': '15%', 'display': 'inline-block'})
                ], 
                style={'font-family': 'Arial, Helvetica, sans-serif', 'font-size': '12px', 'font-weight': 'bold'}
                ),
                html.Div(className="tb_pad", children=[
                    dcc.Tabs(id='progtabs', style={'font-family': 'Arial', 'font-size': '14px'}, value='roster', children=[
                        dcc.Tab(id='roster', label='Roster', value='roster', children=[
                            html.Div(className="tb_pad", children=[
                                dash_table.DataTable(
                                    id='hitters',
                                    columns=hit_cols,
                                    style_cell=sty_cell_font,
                                    style_cell_conditional=sty_align_left + sty_cell_shade,
                                    style_data_conditional=sty_WAR,            
                                    style_header=sty_header,
                                    style_as_list_view=True,
                                    data=rows,
                                    merge_duplicate_headers=True,
                                )
                            ]),

                            html.Div(className="tb_pad", children=[
                                dash_table.DataTable(
                                    id='pitchers',
                                    columns=pit_cols,
                                    style_cell=sty_cell_font,
                                    style_cell_conditional=sty_align_left + sty_cell_shade,
                                    style_data_conditional=sty_WAR,            
                                    style_header=sty_header,
                                    style_as_list_view=True,
                                    data=rows,
                                    merge_duplicate_headers=True,
                                )
                            ]),
                        ]),

                        dcc.Tab(id='results', label='Results', value='results', children=[
                            html.Div(className="l_pad", children=[
                                html.Div([
                                    html.Div([
                                        html.H4(id='division'),
                                        dash_table.DataTable(
                                            id='standings',
                                            columns=standings_cols,
                                            style_cell=sty_standings_font,
                                            style_cell_conditional=sty_align_left + sty_cell_shade + sty_team_width,
                                            style_header=sty_header,
                                            style_as_list_view=True,
                                            data=rows,
                                            merge_duplicate_headers=True,
                                        ), 
                                    ])  
                                ], style = {'display': 'inline-flex', 'height': '300px', 'width': '800px', 'padding-top': '40px'}),
                                html.Div([    
                                    dcc.Graph(id="WL_splits",
                                    config={
                                        'displayModeBar': False
                                    })
                                ], style = {'height': '400px', 'vertical-align': 'top'}),
                            ], style = {'display': 'inline-flex', 'height': '350px', 'width': '90%', 'vertical-align': 'top', 'columnCount': 2}),
                            html.Div([
                                html.Div(className="l_pad", children=[
                                    dcc.RadioItems(
                                        id='standings_type',
                                        options=[{'label': i, 'value': i} for i in ['Selected Team', 'Division']],
                                        value='Selected Team',
                                        labelStyle={'display': 'inline-block'}
                                    )                                    
                                ]),
                                html.Div([
                                    dcc.Graph(
                                        id='team_log',
                                    )   
                                ])
                            ]),
                        ]),
                    ]),
                ], 
                style={'font-family': 'Arial, Helvetica, sans-serif', 'font-size': '12px'}
                ),
            ]),
#            dcc.Tab(id='FA_hit', label='FA Hitters', value='FA_hit', children=[
#                html.Div([
#                    dash_table.DataTable(
#                        id='fa_hitters',
#                        columns=hit_cols,
#                        style_cell=sty_cell_font,
#                        style_cell_conditional=sty_align_left + sty_cell_shade,
#                        style_data_conditional=sty_WAR,            
#                        style_header=sty_header,
#                        style_as_list_view=True,
#                        data=rows,
#                        merge_duplicate_headers=True,
#                        filter_action="native",
#                    )
#                ]),
#            ]),
#            dcc.Tab(id='FA_pit', label='FA Pitchers', value='FA_pit', children=[
#                html.Div([
#                    dash_table.DataTable(
#                        id='fa_pitchers',
#                        columns=pit_cols,
#                        style_cell=sty_cell_font,
#                        style_cell_conditional=sty_align_left + sty_cell_shade,
#                        style_data_conditional=sty_WAR,            
#                        style_header=sty_header,
#                        style_as_list_view=True,
#                        data=rows,
#                        merge_duplicate_headers=True,
#                        filter_action="native",
#                    )
#                ]),
#            ]),
        ])
    ]),

])

@app.callback(
    Output('hitter_graphic', 'figure'),
    [Input('xaxis_column', 'value'),
     Input('yaxis_column', 'value'),
     Input('positions', 'value'),
     Input('min_pa', 'value'),
     Input('season', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, positions_value, min_pa, season):
    dffHitGraph = dfHitCareer[dfHitCareer['Season'] == int(season)]
    dffHitGraph = dffHitGraph[dffHitGraph['PA'] >= int(min_pa)]
    if positions_value == 'All':
        dffHitGraph = dffHitGraph
    else:
        pos_list = [char for char in positions_value]
        dffHitGraph = dffHitGraph[dfHitCareer['PosNums'].astype(str).str.contains('|'.join(pos_list))]

    fig = px.scatter(dffHitGraph, 
                    x=xaxis_column_name, y=yaxis_column_name, size='PA', 
                    hover_name=dffHitGraph['Player'], 
                    color="PrimPosNum",
                    color_continuous_scale=pos_colors, 
                    range_color=[0.5, 10.5],
                    size_max=30, 
                    height=700,
                    labels={"PrimPosNum": "Primary Position"}
                    )

    fig.update_traces(customdata=dffHitGraph['Player'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 20, 'r': 0}, hovermode='closest')


    return fig

def create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y):
    fig = px.scatter(dff, x='Season', y=y_col)
    #fig.add_hline(y=1, line_dash="dot", line_color="green")
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=1, range=[min_season - 0.8, max_season + 0.8])
    fig.update_yaxes(range=[min_y, max_y])

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, 
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ), legend_title_text='')

    return fig

@app.callback(
    Output('PA_time_series', 'figure'),
    #Input('hitter_graphic', 'hoverData'))
    [Input('hitter_graphic', 'hoverData'),
    Input('season', 'value')])
def update_pa_timeseries(hoverData, season):
    player_name = hoverData['points'][0]['customdata']
    min_season = int(season)
    max_season = int(season) + 9
    y_col = 'PA' 
    min_y = -50
    max_y = 800
    ref_line = 500
    dff = dfHitCareer[dfHitCareer['Player'] == player_name]
    dff = dff[(dff['Season'] >= min_season) & (dff['Season'] <= max_season)]
    title = '<b>{}</b><br>{}'.format(player_name, 'PA')
    return create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y)    

@app.callback(
    Output('WAR_time_series', 'figure'),
    #Input('hitter_graphic', 'hoverData'))
    [Input('hitter_graphic', 'hoverData'),
    Input('season', 'value')])
def update_war_timeseries(hoverData, season):
    player_name = hoverData['points'][0]['customdata']
    min_season = int(season)
    max_season = int(season) + 9
    y_col = 'CurrWAR' 
    min_y = -1
    max_y = 15
    ref_line = 5
    dff = dfHitCareer[dfHitCareer['Player'] == player_name]
    dff = dff[(dff['Season'] >= min_season) & (dff['Season'] <= max_season)]
    title = 'WAR'
    return create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y)    

@app.callback(
    Output('OPS_time_series', 'figure'),
    #Input('hitter_graphic', 'hoverData'))
    [Input('hitter_graphic', 'hoverData'),
    Input('season', 'value')])
def update_ops_timeseries(hoverData, season):
    player_name = hoverData['points'][0]['customdata']
    min_season = int(season)
    max_season = int(season) + 9
    #y_col = 'OPS' 
    y_col = ['L_OPS', 'R_OPS']
    min_y = 0.4
    max_y = 1.5
    ref_line = 0.7
    dff = dfHitCareer[dfHitCareer['Player'] == player_name]
    dff = dff[(dff['Season'] >= min_season) & (dff['Season'] <= max_season)]
    title = 'OPS'
    return create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y)     

#@app.callback(
#    Output('hover-data', 'children'),
#    Input('hitter_graphic', 'hoverData'))
#def display_hover_data(hoverData):
#    return json.dumps(hoverData, indent=2)

@app.callback(
    Output('pitcher_graphic', 'figure'),
    [Input('pit_xaxis_column', 'value'),
     Input('pit_yaxis_column', 'value'),
     Input('pit_types', 'value'),
     Input('min_ip', 'value'),
     Input('pit_season', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, pit_types, min_ip, pit_season):
    dffPitGraph = dfPitCareer[dfPitCareer['Season'] == int(pit_season)]
    dffPitGraph['IP'] = pd.to_numeric(dffPitGraph['IP'])
    dffPitGraph = dffPitGraph[dffPitGraph['IP'] >= float(min_ip)]
    if pit_types == 'All':
        dffPitGraph = dffPitGraph
    else:
        pit_types_list = [char for char in pit_types]
        dffPitGraph = dffPitGraph[dfPitCareer['PitTypes'].astype(str).str.contains('|'.join(pit_types_list))]

    fig = px.scatter(dffPitGraph, 
                    x=xaxis_column_name, y=yaxis_column_name, size="IP", color="PitType", color_continuous_scale=pit_colors, 
                    hover_name=dffPitGraph['Player'],
                    range_color=[0.5,3.5],
                    size_max=30, 
                    height=700)

    fig.update_traces(customdata=dffPitGraph['Player'])
    #fig.update_traces(customdata=dffHitGraph[['Player', 'Season']])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 20, 'r': 0}, hovermode='closest')

    return fig

def create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y):
    fig = px.scatter(dff, x='Season', y=y_col)
    #fig.add_hline(y=1, line_dash="dot", line_color="green")
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=1, range=[min_season - 0.8, max_season + 0.8])
    fig.update_yaxes(range=[min_y, max_y])

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, 
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ), legend_title_text='')

    return fig

@app.callback(
    Output('pit_IP_time_series', 'figure'),
    #Input('hitter_graphic', 'hoverData'))
    [Input('pitcher_graphic', 'hoverData'),
    Input('pit_season', 'value')])
def update_ip_timeseries(hoverData, season):
    player_name = hoverData['points'][0]['customdata']
    min_season = int(season)
    max_season = int(season) + 9
    y_col = 'IP' 
    min_y = -50
    max_y = 400
    ref_line = 500
    dff = dfPitCareer[dfPitCareer['Player'] == player_name]
    dff = dff[(dff['Season'] >= min_season) & (dff['Season'] <= max_season)]
    title = '<b>{}</b><br>{}'.format(player_name, 'IP')
    return create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y)    

@app.callback(
    Output('pit_WAR_time_series', 'figure'),
    #Input('hitter_graphic', 'hoverData'))
    [Input('pitcher_graphic', 'hoverData'),
    Input('pit_season', 'value')])
def update_war_timeseries(hoverData, season):
    player_name = hoverData['points'][0]['customdata']
    min_season = int(season)
    max_season = int(season) + 9
    y_col = 'CurrWAR' 
    min_y = -1
    max_y = 15
    ref_line = 5
    dff = dfPitCareer[dfPitCareer['Player'] == player_name]
    dff = dff[(dff['Season'] >= min_season) & (dff['Season'] <= max_season)]
    title = 'WAR'
    return create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y)    

@app.callback(
    Output('pit_OPS_time_series', 'figure'),
    #Input('hitter_graphic', 'hoverData'))
    [Input('pitcher_graphic', 'hoverData'),
    Input('pit_season', 'value')])
def update_ops_timeseries(hoverData, season):
    player_name = hoverData['points'][0]['customdata']
    min_season = int(season)
    max_season = int(season) + 9
    #y_col = 'OPS' 
    y_col = ['L_OPS', 'R_OPS']
    min_y = 0.4
    max_y = 1.5
    ref_line = 0.7
    dff = dfPitCareer[dfPitCareer['Player'] == player_name]
    dff = dff[(dff['Season'] >= min_season) & (dff['Season'] <= max_season)]
    title = 'OPS'
    return create_time_series(dff, title, min_season, max_season, y_col, min_y, max_y)     



@app.callback(
    Output('league', 'options'),
    Input('progression', 'value'))
def set_league_options(selected_prog):
    leagues= {}
    if selected_prog is not None:
        dffProgLeagues = dfProgLeagues[dfProgLeagues['Prog_ID'] == selected_prog]
        dffProgLeagues = dffProgLeagues.drop('Prog_ID', axis=1)
        leagues = dffProgLeagues.set_index('CurTeam').squeeze(axis=1).to_dict()
    return [{'label': v, 'value': k} for k, v in leagues.items()]
    
@app.callback(
    Output('team', 'options'),
    #[Output('team', 'options'),
    # Output('fa_hitters', 'data'),
    # Output('fa_pitchers', 'data')],
    Input('league', 'value'))
def set_team_options(selected_league):
    teams= {}
    fa_hit_rows= []
    fa_pit_rows= []
    if selected_league is not None:
        dffProgTeams = dfProgTeams[dfProgTeams['CurTeam'] == selected_league]
        dffProgTeams = dffProgTeams.drop('CurTeam', axis=1)
        teams = dffProgTeams.set_index('Team_Link').squeeze().to_dict()

        #dffFAHitters = dfFAHitters[dfFAHitters['CurTeam'] == selected_league]
        #fa_hit_rows = dffFAHitters.to_dict('records')

        #dffFAPitchers = dfFAPitchers[dfFAPitchers['CurTeam'] == selected_league]
        #fa_pit_rows = dffFAPitchers.to_dict('records')

    return [{'label': v, 'value': k} for k, v in teams.items()]#, fa_hit_rows, fa_pit_rows

@app.callback(
    [Output('hitters', 'data'),
     Output('pitchers', 'data'),
     Output('division', 'children'),
     Output('standings', 'data'),
     Output('WL_splits', 'figure'),
     Output('team_log', 'figure')],
    [Input('team', 'value'),
     Input('standings_type', 'value')])
def update_table(selected_team, standings_type):
    hit_rows= []
    pit_rows= []
    division= ''
    standings_rows= []
    fig_splits= {}
    fig_team_log= {}
    if selected_team is not None:
        dffHitters = dfHitters[dfHitters['Team_Link'] == selected_team]
        hit_rows = dffHitters.to_dict('records')
        
        dffPitchers = dfPitchers[dfPitchers['Team_Link'] == selected_team]
        pit_rows = dffPitchers.to_dict('records')
        
        dffStandings = dfStandings[dfStandings['Team_Link'] == selected_team]
        division = dffStandings.iloc[0]['Division']
        standings_rows = dffStandings.to_dict('records')
        
        dffTmWLSpl = dfTmWLSpl[dfTmWLSpl['Team_Link'] == selected_team]
        dfPcts = dffTmWLSpl[['Away_LH_Pct', 'Away_RH_Pct', 'Away_Pct', 'Home_LH_Pct', 'Home_RH_Pct', 'Home_Pct', 'LH_Pct', 'RH_Pct', 'Pct']].copy()
        pcts_list = dfPcts.values.tolist()[0]
        floats_list = [float(item) for item in pcts_list]
        splits_list = dffTmWLSpl.values.tolist()[0]

        x = ['Vs. LHS', 'Vs. RHS', 'Total']
        y = ['Away', 'Home', 'Total']
        z = [[floats_list[0], floats_list[1], floats_list[2]],
            [floats_list[3], floats_list[4], floats_list[5]],
            [floats_list[6], floats_list[7], floats_list[8]]]

        al_text = str(int(splits_list[2]))+'-'+str(int(splits_list[3]))+' '+splits_list[4]
        ar_text = str(int(splits_list[5]))+'-'+str(int(splits_list[6]))+' '+splits_list[7]
        at_text = str(int(splits_list[8]))+'-'+str(int(splits_list[9]))+' '+splits_list[10]

        hl_text = str(int(splits_list[11]))+'-'+str(int(splits_list[12]))+' '+splits_list[13]
        hr_text = str(int(splits_list[14]))+'-'+str(int(splits_list[15]))+' '+splits_list[16]
        ht_text = str(int(splits_list[17]))+'-'+str(int(splits_list[18]))+' '+splits_list[19]

        tl_text = str(int(splits_list[20]))+'-'+str(int(splits_list[21]))+' '+splits_list[22]
        tr_text = str(int(splits_list[23]))+'-'+str(int(splits_list[24]))+' '+splits_list[25]
        tt_text = str(int(splits_list[26]))+'-'+str(int(splits_list[27]))+' '+splits_list[28]
        
        z_text = [[al_text, ar_text, at_text],
                [hl_text, hr_text, ht_text],
                [tl_text, tr_text, tt_text]]  

        #colorscale = [[0, 'rgb(255,127,14)'], [0.5, 'white'], [1, 'rgb(31,119,180)']]
        colorscale = [[0, 'red'], [0.5, 'white'], [1, 'blue']]
        #colorscale = 'ylgnbu'
        font_colors = ['black', 'blue', 'white']
        fig_splits = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, hoverinfo='none', colorscale=colorscale, zauto=False, zmin=0.25, zmax=0.75)   
        fig_splits['layout']['xaxis']['tickfont']['family'] = "Arial"
        fig_splits['layout']['xaxis']['tickfont']['size'] = 14
        fig_splits['layout']['yaxis']['tickfont']['family'] = "Arial"
        fig_splits['layout']['yaxis']['tickfont']['size'] = 14
        fig_splits.update_layout(yaxis_autorange='reversed', height=400, width=400)

        if standings_type == 'Selected Team':
            dffLog = dfTmLog[dfTmLog['Team_Link'] == selected_team]
            y_col = ['Win Pct', 'Pythag. Pct', 'Last 10 Pct']
            color = None
        else:
            dfDraftSum = pd.read_sql_table('v_draft_summary', mysqlEngine) 
            dfDiv = dfDraftSum[dfDraftSum['Team_Link'] == selected_team]
            dffLog = pd.merge(dfDiv, dfTmLog, how='inner', on=['CurTeam','Association' , 'Division'])
            y_col=['Win Pct']
            color = 'Team_Name'
        
        
        fig_team_log = px.scatter(dffLog, 
                        x='Team_Game_Num', y=y_col, 
                        
                        color=color, 
                        #color_continuous_scale=pit_colors, 
                        #hover_name=dffPitGraph['Player'],
                        #range_color=[0.5,3.5],
                        #size_max=30, 
                        height=500, 
                        width=1500)

        #fig_team_log.add_hline(y=0.5, line_dash="dot", line_color="green")
        fig_team_log.update_xaxes(range=[-5, 165], title_text='Team Game #')
        fig_team_log.update_yaxes(range=[-0.05, 1.05], title_text='Win %')

        fig_team_log.update_traces(mode='lines')

        fig_team_log.add_shape(type="line",
            xref="x", yref="y",
            x0=-5, y0=0.5, x1=165, y1=0.5,
            line=dict(
                color="lightslategray",
                width=1,
                dash="dot"
            ),
        )

        fig_team_log.update_layout(margin={'l': 40, 'b': 40, 't': 20, 'r': 0}, hovermode='closest', yaxis_tickformat = '.3f')

    return hit_rows, pit_rows, division, standings_rows, fig_splits, fig_team_log
    
if __name__ == '__main__':
    app.run_server(debug=True)