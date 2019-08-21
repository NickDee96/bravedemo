import pandas as pd
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict, Counter
ska=pd.read_csv("roles.csv")
techSkills=pd.read_csv("tech_skillz.csv")
skillCount=techSkills['tech_skill'].value_counts()
skillDf=pd.DataFrame(skillCount).reset_index()
skillDf.columns=["tech_skill","count"]
skills=list(skillDf["tech_skill"])

r=list(ska["Role"].value_counts().index)
r.sort()

s=list()
class roleDetails:
    def __init__(self,roleName):
        role_ska=ska[ska["Role"]==roleName]
        self.role_ss=role_ska[role_ska["Content Model"]=="Soft Skills"][['SAK', 'Importance Value','Level Value']].reset_index(drop=True)
        self.role_kdg=role_ska[role_ska["Content Model"]=="Knowledge"][['SAK', 'Importance Value','Level Value']].reset_index(drop=True)
        self.role_skl=role_ska[role_ska["Content Model"]=="Skills"][['SAK', 'Importance Value','Level Value']].reset_index(drop=True)
        role_skills=techSkills[techSkills["role_name"]==roleName]
        self.hot_tech=list(role_skills[role_skills["hot_technology"]=="Y"]["tech_skill"])
        self.outdated_tech=list(role_skills[role_skills["hot_technology"]=="N"]["tech_skill"])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1(
        children='O*net Analysis',
        style={'text-align': 'center',
                "font":"Roboto",
                "color":"#09ACF7",
                "size":"24"}
    ),
        html.H2(
        children='Brave Venture Labs',
        style={'text-align': 'center',
                "font":"Lustria",
                "color":"#09ACF7",
                "size":"20"}
    ),
        html.H3(
        children='Search by Role',
        style={'text-align': 'center',
                "font":"Lustria",
                "color":"#5B717A",
                "size":"17"}
    ),
    html.Div([
        html.Div([
            html.Div([
                    dcc.Dropdown(
                        id='Role Chooser',
                        options=[{'label': i, 'value': i} for i in r],
                        value='Statisticians'
                    ),
                    dcc.Graph(id="role_det")
                    ]
                )
                ],style= {'width': '49%', 'display': 'inline-block'}),
            html.Div([
                        html.H3([
                                "Technologies used",
                            ],style={'text-align': 'center',
                                        "font":"Roboto",
                                        "color":"#09ACF7",
                                        "size":"20"}),
                        dcc.Markdown(id="hot_tech",style={'color': "#5B717A",
                                                             'fontSize': 16,
                                                             "font":"Roboto"})
            ],style= {'width': '49%',
                     'display': 'inline-block',
                     'vertical-align': 'top',
                     'horizontal-align':"right"})
    ]),
    html.Div([
        html.Div([
            html.H3(
                children='Search by Skill',
                style={'text-align': 'center',
                        "font":"Lustria",
                        "color":"#5B717A",
                        "size":"17"}
                    ),
            dcc.Dropdown(
                        id='Skill Chooser',
                        options=[{'label': i, 'value': i} for i in skills],
                        multi=True,
                        value='Python',
                    ),
            html.H4(id="skill chooser" ,
                    style={'text-align': 'center',
                                        "font":"Roboto",
                                        "color":"#09ACF7",
                                        "size":"16"}),
            dcc.Graph(id="roles-appearing")
            
        ],style= {'width': '49%', 'display': 'inline-block'})
    ])   
])







@app.callback(
    Output("role_det", 'figure'),
    [Input("Role Chooser", 'value')])

def getRoleplot(role):
    a=roleDetails(role)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=a.role_kdg["Importance Value"],
                                y=a.role_kdg["Level Value"],
                                mode="markers",name="Knowledge",
                                hovertext=a.role_kdg["SAK"],
                                marker=dict(
                                    color='#09ACF7',
                                    size=10,
                                )
                ))
    fig.add_trace(go.Scatter(x=a.role_skl["Importance Value"],
                                y=a.role_skl["Level Value"],
                                mode="markers",
                                name="Skills",
                                hovertext=a.role_skl["SAK"],
                                marker=dict(
                                    color='#FF1E91',
                                    size=10,
                                    )))
    fig.add_trace(go.Scatter(x=a.role_ss["Importance Value"],
                                y=a.role_ss["Level Value"],
                                mode="markers",
                                name="Soft Skills",
                                hovertext=a.role_ss["SAK"],
                                marker=dict(
                                    color='#00E676',
                                    size=10,
                                    )))
    fig.update_layout(
        title=go.layout.Title(
            text=("<b>{} <b> <br>Plot of Skills, Knowledge and Soft Skills".format(role)),
            xref="paper",
            x=0,
            font=dict(
                    family="Roboto",
                    size=24,
                    color="#09ACF7"
                )
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Importance Value",
                font=dict(
                    family="Roboto Regular",
                    size=18,
                    color="#5B717A"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Level Value",
                font=dict(
                    family="Roboto Regular",
                    size=18,
                    color="#5B717A"
                )
            )
        )
    )
    return fig


@app.callback(
    Output("hot_tech","children"),
    [Input("Role Chooser", 'value')])
def getTech(role):
    a=roleDetails(role)   
    return ", ".join(a.hot_tech)

@app.callback(
    Output("skill chooser","children"),
    [Input('Skill Chooser','value')]
)

def getPercentage(skill):
    if type(skill)=="str":
        perc=round(float(skillDf[skillDf["tech_skill"]==skill]["count"]/1100)*100,2)
        out=(skill+" occurs in "+str(perc)+"% of O*Net's roles. The roles are listed below.")
    else:
        perc=round(float(skillDf[skillDf["tech_skill"]==skill[0]]["count"]/1100)*100,2)
        out=(skill[0]+" occurs in "+str(perc)+"% of O*Net's roles. The roles are listed below.")
    return out

@app.callback(
    Output("roles-appearing","figure"),
    [Input('Skill Chooser','value')]
)
def getroles(skill_list):
    s=list()
    for i in skill_list:
        skills=list(techSkills[techSkills["tech_skill"]==i]["role_name"])
        s=s+skills
        class OrderedCounter(Counter, OrderedDict): 
            pass
    mskills = [k for k, v in OrderedCounter(s).items() if v > len(skill_list)-1]
    fig2 = go.Figure(data=[go.Table(header=dict(values=['Roles']),
                 cells=dict(values=[mskills]))
                     ])
    return fig2



if __name__ == "__main__":
    app.run_server()
