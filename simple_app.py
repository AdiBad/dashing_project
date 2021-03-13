#FOR APP 
import dash	
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

#FOR AUTH
import dash_auth

#FOR DATA PROCESSING
import pandas as pd

#FOR GRAPH
import dash_cytoscape as cyto

#FOR DASH TABLE
import dash_table

# Password protection
VALID_USERNAME_PASSWORD = {
    'eater': 'apples'
}

#Reading data
node_data = pd.read_csv('graph.tsv', delimiter='\t')

#Make unique lists of nodes & edges from node_data
nodes = set()	#necessary for a future line of code
all_edges = []
all_nodes = []

for index, row in node_data.iterrows():
	
	source = row['node1']
	target = row['node2']
	interaction = row['interaction']

	# put information for current row of the dataframe into dictionaries
	all_source = {'data': {'id': source, 'label': source}}
	all_target = {'data': {'id': target, 'label': target}}
	all_edge = {'data': {'id': source+target, 'source': source, 'target': target,'interaction': interaction}}

	# Add nodes if not already in the set
	if source not in nodes:
		nodes.add(source)
		all_nodes.append(all_source)	  # data: { [here comes that data contained for the node as a dictionary] }

	if target not in nodes:
		nodes.add(target)
		all_nodes.append(all_target)
	
	all_edges.append(all_edge)


# Default variable declared for label
label = 'data(label)'


# Default style of graph
default_stylesheet  = [
	{
		'selector': 'node',						# for all nodes
		'style': {
			'opacity': 1,
			'label': label,
			'background-color': '#666fff',	# background-color = color of node
			'color': '#000000',					# label color = black
		}
	},
	{
		'selector': 'edge',						# for the edges
		'style': {
			'line-color': '#C5D3E2',			
			'curve-style': 'haystack'
		}
	}
]


# This will appear above the cytoscape node graph
node_graph_layout = dbc.Row(
	[
		dbc.Col(
			[
				# Drop down layout 
				html.P("Choose graph layout style:",style={'color':'white'}),
				dcc.Dropdown(
					id='dropdown-layout',
					options=[
						{'label': 'random',
						'value': 'random'},
						{'label': 'grid',
						'value': 'grid'},
						{'label': 'circle',
						'value': 'circle'},
						{'label': 'concentric',
						'value': 'concentric'},
						{'label': 'breadthfirst',
						'value': 'breadthfirst'},
						{'label': 'cose',
						'value': 'cose'},
						{'label': 'euler',
						'value': 'euler'},
						{'label': 'cose-bilkent',
						'value': 'cose-bilkent'},
						{'label': 'cola',
						'value': 'cola'},
						{'label': 'spread',
						'value': 'spread'},
						{'label': 'dagre',
						'value': 'dagre'},
						{'label': 'klay',
						'value': 'klay'}
					], value='grid'
				),
				
			]
		)
	]
)

# Necessary to get more cytoscape layouts like cose-bilkent
cyto.load_extra_layouts()


data_table =  dbc.FormGroup([
	dash_table.DataTable(
		id='interaction_table',
		columns=[{'name': i, 'id': i, 'deletable': False} for i in ['node1','node2','interaction']],
		data = node_data.to_dict('records'),
		page_size = 15,					
		filter_action='native',
		filter_query='',
		sort_action='native',
		sort_mode='multi',
		sort_by=[],
		style_cell={'textAlign': 'left', 'maxWidth': '350px', 'whiteSpace': 'normal'},
		style_cell_conditional=(
		[
			{
				'if': {'column_id': c},
				'backgroundColor': '#79e9de'
			} for c in ['node1']
		]+
		[
			{
				'if': {'column_id': c},
				'backgroundColor': '#d8f8f5'
			} for c in ['node2']
			
		]),
	),
])

# Cystoscape graph itselfs
node_graph = dbc.Row(
	[
		dbc.Col(
			html.Div(children=[
				cyto.Cytoscape(
					id='cake-graph',
					elements = all_edges + all_nodes,
					style = {
						'width': '100%',				# Take up 100% of the width of the space it has been assigned
						'height': '80vh'				# 80% of the total screen height
					},
					stylesheet = default_stylesheet,  	# stylesheet for nodes and edges
					responsive = True					# Changes size according to browser window
				)
			])
		)
	]
)


# Left side panel
left_side_panel = html.Div(
		[
			html.H3(
				'CAKE', 
				style= 
				{
					'textAlign': 'center',
					'color': 'white'
				}
			),
			# Draws horizontal line
			html.Hr(),
			html.Div(
				id='graph_space',
				children=
				[
				node_graph_layout, node_graph, data_table
				])
		
		
		],
		style=
			{
			'position': 'fixed',
			'top': 0,
			'left': 0,
			'bottom': 0,
			'width': '50%',
			'padding': '15px 20px',
			'background-color': '#738678'
			}
)

# Defined some default text styles
CARD_TEXT_STYLE = {
	'margin-left': 10,
	'margin-right': 5,
	'font-size': 20
}

# Right side panel
right_side_panel = html.Div(
    [
        dbc.FormGroup(
            [
				
				dbc.Card(
					children=[
						dbc.CardHeader([html.H4('Ingredient details')]),
						dbc.CardBody([
							html.Div([
								html.P('Ingredient name: ', style=CARD_TEXT_STYLE),
								html.P('Nothing selected', id = 'selectedNode-id', style={'margin-left': 1})
							], className='row'),

							html.Main("Currently displaying {} nodes ".format(len(set(nodes))), id='total_nodes')
                        ]
                        )
                    ]
                ),
				html.Br(),
				dbc.Card(
					children=[
						dbc.CardHeader([html.H4('Tab views')]),
						dbc.CardBody([
			dbc.Nav([
			dbc.NavLink("Table view", href="/table_view", id="table_view_link"),
			dbc.NavLink("Graph view", href="/graph_view", id="graph_view_link"),	
		],vertical=True)])]),
		html.Hr()
			
            ]
        )
    ],
    style =
		{
		'position': 'fixed',
		'top': 0,
		'right': 0,
		'bottom': 0,
		'width': '50%',
		'padding': '20px 10px',
		'background-color': '#b2bdb5'
		}
)

# Define app itself
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Changes layout of graph
@app.callback(
	Output('cake-graph', 'layout'),
	[Input('dropdown-layout', 'value')
])
def update_cytoscape_layout(layout):
	return {'name': layout}

#Display something when node or edge selected
@app.callback( Output('selectedNode-id', 'children'),
				[Input('cake-graph', 'tapNodeData'),Input('cake-graph', 'tapEdgeData')])
def displaySelectedNodeData(data1,data2):
	print(dash.callback_context.triggered)
	
	if 'tapNodeData' in str(dash.callback_context.triggered):
		return ('Node info: ', str(data1))
	elif 'tapEdgeData' in str(dash.callback_context.triggered):
		return ('Edge info: ', str(data2))
	else:
		return 'Nothing selected'

# Changes layout of left side panel based on url
@app.callback(Output('graph_space', 'children'),
				[Input('url', 'pathname')])
def updateTab(pathname):
	if pathname == '/':
		page=html.Div([html.P(
		html.H3("No data to display!"),style={'color':'white','text-align':'center'}),
		])
		return page
	if pathname == '/graph_view':
		return (node_graph_layout, node_graph)
	if pathname == '/table_view':
		return data_table
	

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD
)

# Set app layout
app.layout = html.Div([dcc.Location(id="url"),left_side_panel,right_side_panel])

# Run app
if __name__ == '__main__':
	app.run_server(debug=True,port=8051)
