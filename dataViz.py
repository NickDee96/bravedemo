import pandas as pd
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
ska=pd.read_csv("https://raw.githubusercontent.com/NickDee96/onetlib_analysis/master/roles.csv")
techSkills=pd.read_csv("https://raw.githubusercontent.com/NickDee96/onetlib_analysis/master/tech_skillz.csv")

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


b=roleDetails('Surgeons')
b.hot_tech




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
                "font":"Roboto",
                "color":"#09ACF7",
                "size":"20"}
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='Role Chooser',
                options=[{'label': i, 'value': i} for i in r],
                value='Statisticians'
            ),
        ])
    ]),
    html.Div([
        dcc.Graph(id="role_det"),
        html.H3([
            "Technologies used",
        ],style={'text-align': 'center',
                    "font":"Roboto",
                    "color":"#09ACF7",
                    "size":"20"}),
        dcc.Markdown(id="hot_tech",style={'color': "#5B717A",
                                         'fontSize': 16,
                                         "font":"Roboto"})

        ])
])

@app.callback(
    Output("role_det", 'figure'),
    [Input("Role Chooser", 'value')])

def getRoleplot(role):
    a=roleDetails(role)
    t1=datetime.now()
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
    t2=datetime.now()
    t3=(t2-t1).total_seconds()
    print("Processed in {} seconds".format(t3))
    return fig


@app.callback(
    Output("hot_tech","children"),
    [Input("Role Chooser", 'value')])
def getTech(role):
    a=roleDetails(role)   
    return ", ".join(a.hot_tech)

if __name__=="__main":
    app.run_server()

