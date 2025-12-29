import dash
import dash_auth
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'demo'
}

GOLD = "#b4a378"
CHARCOAL = "#4a5559"
CREAM = "#f9f7f2"
WHITE = "#ffffff"

BRONZE = "#8c7d55"    
SLATE = "#738286"     
MUD = "#d1c7ad"         

DEAL_BAND_MAP = {
    "$0-5K": "#e5ded1",
    "$5-10K": MUD,
    "$10-20K": GOLD,
    "$20-30K": SLATE,
    "$30K+": CHARCOAL
}

BAND_ORDER = ["$0-5K", "$5-10K", "$10-20K", "$20-30K", "$30K+"]

TAB_STYLE = {
    'padding': '12px',
    'fontWeight': '400',
    'backgroundColor': CREAM,
    'border': f'1px solid {GOLD}',
    'borderBottom': 'none',
    'color': CHARCOAL,
    'fontSize': '13px',
    'letterSpacing': '1px',
    'fontFamily': 'Helvetica, Arial, sans-serif'
}

TAB_SELECTED_STYLE = {
    'padding': '12px',
    'fontWeight': 'bold',
    'backgroundColor': WHITE,
    'borderTop': f'3px solid {GOLD}', 
    'borderLeft': f'1px solid {GOLD}',
    'borderRight': f'1px solid {GOLD}',
    'borderBottom': 'none',
    'color': CHARCOAL,
    'fontSize': '13px',
    'letterSpacing': '1px'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

def apply_style(fig, title):

    fig.update_layout(
        title={'text': title, 'font': {'color': CHARCOAL, 'size': 16}},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Helvetica, Arial, sans-serif'},
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(showgrid=True, gridcolor="#e9e9e9", color=CHARCOAL, title_text=""),
        yaxis=dict(showgrid=False, color=CHARCOAL, title_text="")
    )
    

    # Get number of bars if bar chart
    is_bar = fig.data[0].type == 'bar'
    num_traces = len(fig.data)

    # Return heatmap as-is
    trace_type = fig.data[0].type
    if trace_type == 'heatmap':
        return fig
    
    if num_traces == 1:
        color_attr = {'marker_color': GOLD}
        if is_bar: color_attr['width'] = 0.5 
        fig.update_traces(**color_attr)
        
    elif num_traces == 2:
        fig.data[0].marker.color = GOLD
        fig.data[1].marker.color = CHARCOAL
        if is_bar: fig.update_traces(width=0.3)
        
    elif num_traces > 2:
        for trace in fig.data:
            if trace.name in DEAL_BAND_MAP:
                trace.marker.color = DEAL_BAND_MAP[trace.name]
        if is_bar: fig.update_traces(width=0.15)
            
    return fig

grouped_segments_df = pd.read_csv('./data/grouped_segments_df.csv')
conv_rate_revenue_band = pd.read_csv('./data/conv_rate_revenue_band.csv')
client_type_df = pd.read_csv('./data/client_type_df.csv')
deals_clean_df = pd.read_csv('./data/deals_clean.csv')

client_segments = sorted(grouped_segments_df['client_segment'].unique().tolist())

app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/whitelabel.png", style={"width": "100%", "marginBottom": "40px"}), 
        html.P("Data Scope: Jan 2022 – Present", 
            style={"fontSize": "12px", "color": "#8c7d55", "marginTop": "-30px", "marginBottom": "30px", "textAlign": "center"}),
        html.H5("DASHBOARD FILTERS", style={"color": CHARCOAL, "letterSpacing": "2px", "fontSize": "14px"}),
        html.Hr(),
        html.P("Client Segment", className="small mb-1", style={"color": CHARCOAL}),
        dcc.Dropdown(
            id='client-segment-dropdown',
            options=[{'label': 'All Segments', 'value': 'ALL'}] + [{'label': seg, 'value': seg} for seg in client_segments],
            multi=True,
            value=['ALL'],
            className="mb-4",
            style={'fontSize': '12px'}
        ),
    ], style={
        "position": "fixed", "top": 0, "left": 0, "bottom": 0,
        "width": "18rem", "padding": "2rem 1rem", "backgroundColor": CREAM,
        "borderRight": f"1px solid {GOLD}"
    }),

    html.Div([
    dcc.Tabs([
        # TAB 1: Client Segment Overview
        dcc.Tab(label='Client Segment Overview', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE, children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div(id='kpi-overview-1'), width=3),
                    dbc.Col(html.Div(id='kpi-overview-2'), width=3),
                    dbc.Col(html.Div(id='kpi-overview-3'), width=3),
                    dbc.Col(html.Div(id='kpi-overview-4'), width=3),
                ], className="mt-4 mb-4", style={"paddingLeft": "15px"}),
                
                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-1', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=6),
                    
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-2', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=6),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-3', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=6),
                    
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-4', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=6),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-5', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ]),
            ], fluid=True)
        ]),
        # TAB 2: Segment Deep Dive
        dcc.Tab(label='Segment Deep Dive', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE, children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-6', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-7', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-8', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-9', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4")
            ], fluid=True)
        ]),
        # TAB 3: Opportunity Analysis
        dcc.Tab(label='Opportunity Analysis', style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE, children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.P("Focus Quadrant", className="small mb-1", style={"color": CHARCOAL, "marginTop": "20px"}),
                        dcc.Dropdown(
                            id='quadrant-filter',
                            options=[
                                {'label': 'All Quadrants', 'value': 'ALL'},
                                {'label': 'Strategic Priority', 'value': 'Priority'},
                                {'label': 'Revenue Leakage', 'value': 'Leakage'},
                                {'label': 'Efficiency Wins', 'value': 'Efficiency'},
                                {'label': 'Low ROI', 'value': 'LowROI'}
                            ],
                            value='ALL',
                            clearable=False,
                            style={'fontSize': '12px'}
                        ),
                    ], width=4)
                ], className="mb-2"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-priority-matrix', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-lvi', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4"),

                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([dcc.Graph(id='chart-missed-rev', config={'displayModeBar': False})])
                    ], style={"border": "none", "boxShadow": "0 4px 6px rgba(0,0,0,0.15)"}), width=12),
                ], className="mb-4"),

            ], fluid=True)
        ]),

    ])
], style={"marginLeft": "18rem", "padding": "2rem", "backgroundColor": WHITE})
])

# Callback and function for Tab 1: Client Segment Overview
@app.callback(
    [Output('chart-1', 'figure'), Output('chart-2', 'figure'), Output('chart-3', 'figure'), Output('chart-4', 'figure'), Output('chart-5', 'figure'),
     Output('kpi-overview-1', 'children'), Output('kpi-overview-2', 'children'), Output('kpi-overview-3', 'children'), Output('kpi-overview-4', 'children')],
    Input('client-segment-dropdown', 'value')
)
def update_charts(selected_segments):
    if not selected_segments: return [px.scatter(title="Select Segment")] * 5 + [html.Div()] * 4
    if 'ALL' in selected_segments: selected_segments = client_segments
    
    df = grouped_segments_df[grouped_segments_df['client_segment'].isin(selected_segments)]
    df_deals = deals_clean_df[deals_clean_df['client_segment'].isin(selected_segments)]

    # Chart 1: Conversion Rate by Segment
    df1 = df.sort_values('conversion_rate', ascending=False)
    f1 = apply_style(
        px.bar(df1, x='client_segment', y='conversion_rate',
               labels={'client_segment': 'Client Segment', 'conversion_rate': 'Conversion Rate'}), 
        "CONVERSION BY SEGMENT (%)"
    )
    # Chart 2: Average Lead Time by Segment
    df2 = df.sort_values('avg_lead_time', ascending=False)
    f2 = apply_style(
        px.bar(df2, x='client_segment', y='avg_lead_time',
               labels={'client_segment': 'Client Segment', 'avg_lead_time': 'Average Lead Time (Days)'}), 
        "AVERAGE LEAD TIME (DAYS)"
    )

    # Chart 3: Average Deal Size by Segment
    df3 = df.sort_values('avg_deal_size', ascending=False)
    f3 = apply_style(
        px.bar(df3, x='client_segment', y='avg_deal_size',
               labels={'client_segment': 'Client Segment', 'avg_deal_size': 'Average Deal Size ($)'}), 
        "AVERAGE DEAL SIZE ($)"
    )

    # Chart 4: Segment Revenue
    df4 = df.sort_values('segment_revenue', ascending=False)
    f4 = apply_style(
        px.bar(df4, x='client_segment', y='segment_revenue',
               labels={'client_segment': 'Client Segment', 'segment_revenue': 'Segment Revenue ($)'}), 
        "SEGMENT REVENUE ($)"
    )

    # Chart 5: Deal Volume % vs Revenue Share %
    df5 = df.sort_values('percent_total_revenue', ascending=False)
    df5_renamed = df5.rename(columns={
        'pct_total_deals': 'Deal Volume %',
        'percent_total_revenue': 'Revenue Share %'
    })
    f5 = apply_style(
        px.bar(
            df5_renamed, 
            y='client_segment', 
            x=['Deal Volume %', 'Revenue Share %'], 
            orientation='h', 
            barmode='group',
            labels={
            'variable': ''
            }
        ), 
        "DEAL VOLUME vs REVENUE SHARE"
    )

    kpi1 = html.Div([
        html.P("TOTAL REVENUE", className="small mb-0", style={"letterSpacing": "1px", "color": CHARCOAL}),
        html.H4(f"${df_deals[df_deals['converted'] == True]['decimal_value'].sum():,.0f}", style={"color": CHARCOAL})
    ])
    
    kpi2 = html.Div([
        html.P("AVG CONVERSION", className="small mb-0", style={"letterSpacing": "1px", "color": CHARCOAL}),
        html.H4(f"{df_deals['converted'].mean():.1%}", style={"color": CHARCOAL})
    ])
    
    kpi3 = html.Div([
        html.P("CONVERTED DEALS", className="small mb-0", style={"letterSpacing": "1px", "color": CHARCOAL}),
        html.H4(f"{df['converted_deals'].sum():,}", style={"color": CHARCOAL})
    ])
    
    kpi4 = html.Div([
        html.P("AVG LEAD TIME", className="small mb-0", style={"letterSpacing": "1px", "color": CHARCOAL}),
        html.H4(f"{df_deals['lead_time'].mean():.0f} Days", style={"color": CHARCOAL})
    ])
    
    return f1, f2, f3, f4, f5, kpi1, kpi2, kpi3, kpi4

# Callback and function for Tab 2: Segment Deep Dive
@app.callback(
    [Output('chart-6', 'figure'), Output('chart-7', 'figure'), Output('chart-8', 'figure'), Output('chart-9', 'figure')],
    Input('client-segment-dropdown', 'value')
)
def update_deep_dive_charts(selected_segments):
    if not selected_segments: return [px.scatter(title="Select Segment")] * 4
    if 'ALL' in selected_segments: selected_segments = client_segments
    
    df = conv_rate_revenue_band[conv_rate_revenue_band['client_segment'].isin(selected_segments)]
    
    # Chart 6: Conversion Rate per Deal Band per Segment
    f6 = apply_style(
        px.bar(
            df, 
            x='client_segment', 
            y='conversion_rate', 
            color='deal_band', 
            barmode='group',
            category_orders={"deal_band": BAND_ORDER},
            labels={'conversion_rate': 'Conv. Rate (%)', 'deal_band': 'Deal Band'}
        ), 
        "CONVERSION RATE BY DEAL BAND (%)"
    )

    # Chart 7: Inquiry Volume by Deal Band
    f7 = px.bar(
        df, x='client_segment', y='total_deals',
        color='deal_band', barmode='group',
        category_orders={"deal_band": BAND_ORDER},
        labels={'count': 'Number of Inquiries', 'client_segment': 'Segment'}
    )
    f7 = apply_style(f7, "INQUIRY VOLUME BY DEAL BAND")

    # Chart 8: Revenue Mix per Deal Band per Segment
    f8 = apply_style(
        px.bar(
            df, 
            x='client_segment', 
            y='percent_rev_within_segment', 
            color='deal_band', 
            barmode='group',
            category_orders={"deal_band": BAND_ORDER},
            labels={'percent_rev_within_segment': 'Revenue Mix (%)', 'deal_band': 'Deal Band'}
        ), 
        "REVENUE MIX BY DEAL BAND (%)"
    )

    # Chart 9: Inquiries vs. Wins (by Segment)
    df9 = df.groupby('client_segment')[['total_deals', 'converted_deals']].sum().reset_index()
    df9 = df9.sort_values('total_deals', ascending=True)

    f9 = go.Figure()
    f9.add_trace(go.Bar(
        y=df9['client_segment'],
        x=df9['total_deals'],
        name='Total Inquiries',
        marker_color=CHARCOAL,
        orientation='h'
    ))

    f9.add_trace(go.Bar(
        y=df9['client_segment'],
        x=df9['converted_deals'],
        name='Converted Deals',
        marker_color=GOLD,
        orientation='h'
    ))

    f9 = apply_style(f9, "INQUIRIES vs. WINS")

    f9.update_layout(
        barmode='group',
        bargap=0.2,
        xaxis_tickformat=',',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return f6, f7, f8, f9

# Callback and function for Tab 3: Opportunity Analysis
@app.callback(
    [Output('chart-priority-matrix', 'figure'), Output('chart-lvi', 'figure'), Output('chart-missed-rev', 'figure'),],
    [Input('client-segment-dropdown', 'value'),
     Input('quadrant-filter', 'value')]
)
def update_opportunity_charts(selected_segments, selected_quad):
    if not selected_segments: 
        return [px.scatter(title="Select Segment")] * 3
        
    if 'ALL' in selected_segments: 
        selected_segments = client_segments
    
    df = conv_rate_revenue_band[conv_rate_revenue_band['client_segment'].isin(selected_segments)].copy()
    df['revenue_per_lead'] = df['total_revenue_segment'] / df['total_deals']
    
    x_mid, x_max = 50.0, 100.0
    y_mid = df['revenue_per_lead'].max() / 2 if not df.empty else 1
    y_max = df['revenue_per_lead'].max() * 1.2 if not df.empty else 1000

    x_range, y_range = [0, x_max], [0, y_max]

    if selected_quad == 'Priority':
        df = df[(df['conversion_rate'] >= x_mid) & (df['revenue_per_lead'] >= y_mid)]
        x_range, y_range = [x_mid, x_max], [y_mid, y_max]
    elif selected_quad == 'Leakage':
        df = df[(df['conversion_rate'] < x_mid) & (df['revenue_per_lead'] >= y_mid)]
        x_range, y_range = [0, x_mid], [y_mid, y_max]
    elif selected_quad == 'Efficiency':
        df = df[(df['conversion_rate'] >= x_mid) & (df['revenue_per_lead'] < y_mid)]
        x_range, y_range = [x_mid, x_max], [0, y_mid]
    elif selected_quad == 'LowROI':
        df = df[(df['conversion_rate'] < x_mid) & (df['revenue_per_lead'] < y_mid)]
        x_range, y_range = [0, x_mid], [0, y_mid]

    # Chart 10: Deal Band Priority Matrix
    f10 = px.scatter(
        df, 
        x='conversion_rate', 
        y='revenue_per_lead', 
        size='total_revenue_segment',
        color='deal_band', 
        hover_name='client_segment',
        custom_data=['client_segment', 'deal_band', 'conversion_rate', 'revenue_per_lead', 'total_revenue_segment'],
        category_orders={"deal_band": BAND_ORDER},
        color_discrete_map=DEAL_BAND_MAP
    )

    f10.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",                
            "Band: %{customdata[1]}",                 
            "Conversion: %{customdata[2]:.1f}%",      
            "Revenue/Lead: $%{customdata[3]:,.0f}",   
            "Total Revenue: $%{customdata[4]:,.0f}",  
            "<extra></extra>"                         
        ])
    )

    all_annos = {
        'Priority': dict(x=0.95, y=0.95, xref="paper", yref="paper", align="right", showarrow=False,
                         text="<b>STRATEGIC PRIORITY</b><br><span style='font-size:10px; color:#6c757d'>High Value / High Conversion</span>", 
                         font=dict(color=CHARCOAL, size=13)),
        'Leakage': dict(x=0.05, y=0.95, xref="paper", yref="paper", align="left", showarrow=False,
                        text="<b>REVENUE LEAKAGE</b><br><span style='font-size:10px; color:#6c757d'>High Value / Low Conversion</span>", 
                        font=dict(color=CHARCOAL, size=12)),
        'Efficiency': dict(x=0.95, y=0.05, xref="paper", yref="paper", align="right", showarrow=False,
                           text="<b>EFFICIENCY WINS</b><br><span style='font-size:10px; color:#6c757d'>Low Value / High Conversion</span>", 
                           font=dict(color=CHARCOAL, size=12)),
        'LowROI': dict(x=0.05, y=0.05, xref="paper", yref="paper", align="left", showarrow=False,
                       text="<b>LOW ROI</b><br><span style='font-size:10px; color:#6c757d'>Low Value / Low Conversion</span>", 
                       font=dict(color="#adb5bd", size=11))
    }

    if selected_quad == 'ALL':
        display_annos = list(all_annos.values())
    else:
        active_anno = all_annos[selected_quad].copy()
        active_anno.update(x=0.5, y=1.05, align="center") 
        display_annos = [active_anno]

    f10.update_layout(
        shapes=[
            dict(type="rect", x0=x_mid, x1=x_max, y0=y_mid, y1=y_max, fillcolor=GOLD, opacity=0.1, layer="below", line_width=0),
            dict(type="rect", x0=0, x1=x_mid, y0=y_mid, y1=y_max, fillcolor=SLATE, opacity=0.05, layer="below", line_width=0),
            dict(type="rect", x0=x_mid, x1=x_max, y0=0, y1=y_mid, fillcolor=MUD, opacity=0.08, layer="below", line_width=0),
            dict(type="rect", x0=0, x1=x_mid, y0=0, y1=y_mid, fillcolor="#f8f9fa", opacity=1.0, layer="below", line_width=0),
        ],
        annotations=display_annos
    )

    f10 = apply_style(f10, "DEAL BAND PRIORITY MATRIX")

    f10.update_xaxes(
        title=dict(text="CONVERSION RATE (%)", font=dict(size=12, color=CHARCOAL)),
        range=x_range, 
        showgrid=True, 
        gridcolor="#f1f3f5", 
        zeroline=False,
        dtick=20
    )

    f10.update_yaxes(
        title=dict(text="HISTORICAL REVENUE PER INQUIRY ($)", font=dict(size=12, color=CHARCOAL)),
        range=y_range, 
        showgrid=True, 
        gridcolor="#f1f3f5", 
        zeroline=False, 
        tickprefix="$", 
        tickformat=",.0s",
        dtick=10000,
        nticks=0 
    )
    
    heatmap_df = df.pivot(index='client_segment', columns='deal_band', values='expected_value')
    heatmap_df = heatmap_df.reindex(columns=[b for b in BAND_ORDER if b in heatmap_df.columns])
    
    f11 = go.Figure(data=go.Heatmap(
        z=heatmap_df.values,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        colorscale=[[0, CREAM], [0.5, GOLD], [1, CHARCOAL]],
        hoverongaps=False,
        hovertemplate="Segment: %{y}<br>Band: %{x}<br>Expected Value: $%{z:,.0f}<extra></extra>",
        text=heatmap_df.values,
        texttemplate="$%{text:,.0s}", 
        textfont={"size": 10, "family": "Helvetica"}
    ))

    f11 = apply_style(f11, "LEAD VALUE INDEX (EXPECTED REVENUE PER LEAD)")
    f11.update_layout(yaxis=dict(showgrid=False, title=""), xaxis=dict(side="top"))

    # Chart 12: Missed Revenue by Segment
    f12 = px.bar(df, y='client_segment', x='missed_revenue', color='deal_band', orientation='h',
                 category_orders={"deal_band": BAND_ORDER}, color_discrete_map=DEAL_BAND_MAP)
    f12 = apply_style(f12, "MISSED REVENUE")
    f12.update_xaxes(tickprefix="$", tickformat=",.0s")
    f12.update_traces(width=0.8)

    return f10, f11, f12

if __name__ == '__main__':
    app.run(debug=True)