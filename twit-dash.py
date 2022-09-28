
from re import X
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import twit_data_analysis as tda

twitter_data_file = '~/Github/PythonPrograms/twitter-portfolio-project/data/roe-wade-10000-original-sentiment-added.json'
twitter_data = pd.read_json(twitter_data_file)
twit_data_obj = tda.tweet_analysis(twitter_data)

template = 'seaborn'

figure_parans = {
                'layout':{
                    'plot_bgcolor':'#1e1e1e',
                    'paper_bgcolor':'#1e1e1e'
                },
                'font':{
                    'color':'white'
                }
            }

color_dict = {
    'dropdown_background' : '#1b3752'
}

app = dash.Dash()

app.layout = html.Div(
    children = [
        html.Div(
            children = [
                # Header
                html.H1(
                    'Twitter response to Roe v Wade', 
                style={'textAlign':'center', 'color':'#FFFFFF','font-size':30,'margin-bottom':0, 'margin-top':-10,'margin-right':-10,'margin-left':-5,'background-color':'#3e7cb9'}
                ),
                html.Br(),
                html.Br()
            ], style={'background-color':color_dict['dropdown_background']}
        ),
        # Input box
        html.Div(
            children = [
                # html.H3(
                #     "Summary type: ",
                #     style={'color':'white'},
                # ),
                # dcc.Input(id='input_page', value='Select page.',
                # style={'textAlign':'center','height':'30px','font-size':20,'color':'#71bbd8','background-color':'#3a3a3a'}),
                # html.Br(),
                # html.Br(),
                dcc.Dropdown(id='input_page',
                    options=[
                        {'label':'Tweet Sentiment Summary','value':'page1'},
                        {'label':'Tweet meta-statistics','value':'page2'}
                    ],
                    value='page2',
                    style = {'width': '50%',  'align-items': 'center', 'justify-content': 'center'}
                    # style={'justify-content':'center','width':'50%'}
                ),
            ],
            style={'display':'flex','background-color':color_dict['dropdown_background']}
        ),
        html.Div(
            children = [
                html.Br(),
                html.Br()
            ], style={'background-color':color_dict['dropdown_background']}
        ),
        # Graph segment 1
        html.Div(
            children = [
                html.Div(dcc.Graph(
                    id='pos1',
                    figure = {
                        'layout':{
                            'plot_bgcolor':'#1e1e1e',
                            'paper_bgcolor':'#1e1e1e'
                        },
                        'font':{
                            'color':'white'
                        },
                    }
                    )),
                html.Div(dcc.Graph(id='pos2',figure={**figure_parans})),
            ],
            style={'display':'flex','align':'center','background-color':'#ffffff'}
        ),
        # Graph segment 2
        html.Div(
            [
                html.Div(dcc.Graph(id='pos3',figure={**figure_parans})),
                html.Div(dcc.Graph(id='pos4',figure={**figure_parans}))
            ],
            style={'display':'flex','background-color':'#ffffff'}
        )
    ],
)

@app.callback([
    Output(component_id='pos1',component_property='figure'),
    Output(component_id='pos2',component_property='figure'),
    Output(component_id='pos3',component_property='figure'),
    Output(component_id='pos4',component_property='figure'),
],
Input(component_id='input_page', 
component_property='value'))
def get_graph(page):
    common_layout_params = {
        'showlegend':False
    }
    tweet_count_axis = {
        'xaxis_title':'Score',
        'yaxis_title':'Number of Tweets'
    }

    if page=='page1':
        print('calling get_graph page 1')
        negative_tweets = px.histogram(data_frame=twit_data_obj.neg_tweet_counts,title='Distribution of Negative Scores', color_discrete_sequence=['indianred'],template=template).update_layout(common_layout_params,**tweet_count_axis)
        positive_tweets = px.histogram(data_frame=twit_data_obj.pos_tweet_counts, title='Distribution of Positive Scores',color_discrete_sequence=['green'],template=template).update_layout(common_layout_params,**tweet_count_axis)
        neutral_tweets = px.histogram(data_frame=twit_data_obj.neut_tweet_counts,title='Distribution of Neutral Scores',color_discrete_sequence=['skyblue'],template=template).update_layout(common_layout_params,**tweet_count_axis)
        print(twit_data_obj.net_sent_tweet_counts.index.to_list())
        tweet_sent_score = px.bar(data_frame=twit_data_obj.net_sent_tweet_counts,title='Comparison of Overall Sentiments', color=twit_data_obj.net_sent_tweet_counts.index,template=template).update_layout(common_layout_params,xaxis_title='Tweet Sentiment',yaxis_title='Number of Tweets')
        return [negative_tweets, positive_tweets, neutral_tweets, tweet_sent_score]
    
    elif page=='page2':
        print('calling get_graph page 2')
        print(twit_data_obj.corr_data)
        x=[0,1,2,3]
        y=[0,1,2,3]
        # negative_tweets=px.line(x=x,y=y)
        corr = twit_data_obj.corr_data
        corr_matrix=go.Figure(data=[go.Heatmap(
                x = corr.columns,
                y = corr.index,
                z = np.array(corr),
                text=corr.values,
                colorscale='RdBu',
                texttemplate='%{text:.2f}'
            )]).update_layout(title='Correlation matrix',template=template)
        source_dist = px.bar(data_frame=twit_data_obj.tweet_source_counts_grouped,orientation='h',title='Twitter Clients', template=template).update_layout(showlegend=False)
        lang_dist = px.pie(values=twit_data_obj.lang_counts_grouped,names=twit_data_obj.lang_counts_grouped.index,title='Tweet Languages',hole=0.3,template=template).update_traces(textposition='inside', textinfo='percent+label')
        sent_evol=px.area(data_frame=twit_data_obj.sent_evol_df,x='tweet_time',y=['pos_tweet_count','neg_tweet_count'],title='Evolution of Sentiments').update_layout(xaxis_title='Date and Time', yaxis_title = 'Number of Tweets',title_x=0.5,legend={'orientation':'h','x':0.01,'y':0.99})
        return [corr_matrix, source_dist, lang_dist, sent_evol]


if __name__ == '__main__':
    app.run_server()
