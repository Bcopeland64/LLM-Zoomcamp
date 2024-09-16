import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from src.utils.db import Database
import pandas as pd
from datetime import datetime, timedelta

app = dash.Dash(__name__)

def get_db():
    return Database('path/to/your/database.sqlite')

app.layout = html.Div([
    html.H1('RAG Chatbot Monitoring Dashboard'),
    
    dcc.Tabs([
        dcc.Tab(label='User Feedback', children=[
            dcc.Graph(id='feedback-over-time'),
            dcc.Graph(id='feedback-distribution'),
        ]),
        dcc.Tab(label='Query Analysis', children=[
            dcc.Graph(id='query-volume'),
            dcc.Graph(id='top-queries'),
        ]),
        dcc.Tab(label='System Performance', children=[
            dcc.Graph(id='response-time'),
            dcc.Graph(id='error-rate'),
        ]),
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    [Output('feedback-over-time', 'figure'),
     Output('feedback-distribution', 'figure'),
     Output('query-volume', 'figure'),
     Output('top-queries', 'figure'),
     Output('response-time', 'figure'),
     Output('error-rate', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    with get_db() as db:
        # Fetch data for feedback over time
        feedback_data = db.fetchall("""
            SELECT date(timestamp) as date, AVG(rating) as avg_rating
            FROM user_feedback
            GROUP BY date(timestamp)
            ORDER BY date
        """)
        feedback_df = pd.DataFrame(feedback_data)
        feedback_over_time = px.line(feedback_df, x='date', y='avg_rating', title='Average Feedback Over Time')

        # Fetch data for feedback distribution
        feedback_dist = db.fetchall("""
            SELECT rating, COUNT(*) as count
            FROM user_feedback
            GROUP BY rating
            ORDER BY rating
        """)
        feedback_dist_df = pd.DataFrame(feedback_dist)
        feedback_distribution = px.bar(feedback_dist_df, x='rating', y='count', title='Feedback Distribution')

        # Fetch data for query volume
        query_volume_data = db.fetchall("""
            SELECT date(timestamp) as date, COUNT(*) as count
            FROM user_feedback
            GROUP BY date(timestamp)
            ORDER BY date
        """)
        query_volume_df = pd.DataFrame(query_volume_data)
        query_volume = px.line(query_volume_df, x='date', y='count', title='Query Volume Over Time')

        # Fetch data for top queries
        top_queries_data = db.fetchall("""
            SELECT query, COUNT(*) as count
            FROM user_feedback
            GROUP BY query
            ORDER BY count DESC
            LIMIT 10
        """)
        top_queries_df = pd.DataFrame(top_queries_data)
        top_queries = px.bar(top_queries_df, x='query', y='count', title='Top 10 Queries')

        # Simulated data for response time (replace with actual data if available)
        response_time_data = [{'date': datetime.now() - timedelta(days=i), 'time': 0.5 + i*0.1} for i in range(7)]
        response_time_df = pd.DataFrame(response_time_data)
        response_time = px.line(response_time_df, x='date', y='time', title='Average Response Time')

        # Simulated data for error rate (replace with actual data if available)
        error_rate_data = [{'date': datetime.now() - timedelta(days=i), 'rate': 0.05 - i*0.005} for i in range(7)]
        error_rate_df = pd.DataFrame(error_rate_data)
        error_rate = px.line(error_rate_df, x='date', y='rate', title='Error Rate')

    return feedback_over_time, feedback_distribution, query_volume, top_queries, response_time, error_rate

if __name__ == '__main__':
    app.run_server(debug=True)
