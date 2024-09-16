from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests

app = Dash(__name__)

app.layout = html.Div([
    html.H1('NFL Rules Chatbot Monitoring Dashboard'),
    dcc.Graph(id='query-feedback-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('query-feedback-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    # Fetch stats from the main application
    response = requests.get('http://localhost:8000/stats')
    stats = response.json()
    
    # Create a DataFrame for the graph
    df = pd.DataFrame({
        'Metric': ['Total Queries', 'Total Feedback', 'Average Rating'],
        'Value': [stats['total_queries'], stats['total_feedback'], stats['average_rating']]
    })
    
    # Create the bar chart
    fig = px.bar(df, x='Metric', y='Value', title='Chatbot Performance Metrics')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
