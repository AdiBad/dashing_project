#FOR APP 
import dash	
import dash_bootstrap_components as dbc
import dash_html_components as html

#FOR AUTH
import dash_auth

#FOR CALLBACKS
from dash.dependencies import Input, Output, State

# Password protection
VALID_USERNAME_PASSWORD = {
    'eater': 'apples'
}

# Define app itself
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD
)
# Set app layout
app.layout = html.Div("Success!")

# run app
if __name__ == '__main__':
	app.run_server(debug=True,port=8051)