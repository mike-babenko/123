
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px


spacex_df = pd.read_csv("spacex_launch_dash.csv")
# Calculate minimum and maximum payload for configuring the slider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()


app = dash.Dash(__name__)


app.layout = html.Div(children=[
    
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    

    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    
  
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
      
        df = spacex_df[spacex_df['class'] == 1]  
        fig = px.pie(df, names='Launch Site',
                     title='Total Successful Launches by Site')
        return fig
    else:
       
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_count = df[df['class'] == 1].shape[0]
        failure_count = df[df['class'] == 0].shape[0]
        fig = px.pie(names=['Success', 'Failure'], values=[success_count, failure_count],
                     title=f'Total Launch Outcomes for site {selected_site}')
        return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    # Filter data by payload range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    
    if selected_site == 'ALL':
       
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
        return fig
    else:
       
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {selected_site}')
        return fig


if __name__ == '__main__':
    app.run()

