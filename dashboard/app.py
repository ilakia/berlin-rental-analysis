import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Page config
st.set_page_config(
    page_title="Berlin Rental Market",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    
    .hero {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563EB 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        margin: 0 0 0.4rem 0;
        color: white;
    }
    .hero p {
        font-size: 1.05rem;
        opacity: 0.85;
        margin: 0;
        font-weight: 300;
    }
    
    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 600;
        color: #0F172A;
        line-height: 1;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 0.2rem;
    }
    
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #0F172A;
        margin: 0 0 1rem 0;
    }
    
    .insight-box {
        background: #EFF6FF;
        border-left: 4px solid #2563EB;
        border-radius: 0 8px 8px 0;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        color: #1E40AF;
    }

    div[data-testid="stSidebar"] {
        background: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    
    .stSelectbox label, .stSlider label {
        font-weight: 500 !important;
        color: #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, 'processed/listings_clean.csv'))
    neighbourhood_summary = pd.read_csv(os.path.join(BASE_DIR, 'processed/neighbourhood_summary.csv'))
    accommodates_analysis = pd.read_csv(os.path.join(BASE_DIR, 'processed/accommodates_analysis.csv'))
    return df, neighbourhood_summary, accommodates_analysis

df, neighbourhood_summary, accommodates_analysis = load_data()

# Plotly base theme
CHART_THEME = dict(
    font_family="DM Sans",
    font_color="#0F172A",
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=40, b=20, l=10, r=10)
)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 🔍 Filters")
    st.markdown("---")
    room_types = ['All'] + sorted(df['room_type'].unique().tolist())
    selected_room_type = st.selectbox("Room Type", room_types)
    top_n = st.slider("Top N Neighbourhoods", 10, 30, 15)
    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("""
    This dashboard analyses **Berlin Airbnb listings** using real data from Inside Airbnb.  
    
    **Data:** 9,220 listings across 138 neighbourhoods.  
    **Last updated:** March 2026.
    """)

# Apply filter
df_filtered = df[df['room_type'] == selected_room_type] if selected_room_type != 'All' else df.copy()

# ── HERO ──
st.markdown("""
<div class="hero">
    <h1>🏙️ Berlin Rental Market</h1>
    <p>Exploring Airbnb pricing trends, neighbourhood value, and guest patterns across Berlin</p>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──
col1, col2, col3, col4 = st.columns(4)
metrics = [
    (col1, "Total Listings", f"{len(df_filtered):,}", "Active on Airbnb"),
    (col2, "Average Price", f"€{df_filtered['price'].mean():.0f}", "Per night"),
    (col3, "Median Price", f"€{df_filtered['price'].median():.0f}", "Per night"),
    (col4, "Neighbourhoods", str(df_filtered['neighbourhood_cleansed'].nunique()), "Across Berlin"),
]
for col, label, value, sub in metrics:
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── KEY INSIGHTS ──
st.markdown('<p class="section-title">💡 Key Insights</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="insight-box">📍 <b>Alexanderplatz</b> is the most listed neighbourhood with 710 listings</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="insight-box">💰 <b>Size drives price</b> more than ratings — accommodates has 0.53 correlation with price</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="insight-box">⭐ <b>Superhosts</b> charge €16 more on average and maintain 4.86 vs 4.66 ratings</div>', unsafe_allow_html=True)

st.markdown("---")

# ── NEIGHBOURHOOD ANALYSIS ──
st.markdown('<p class="section-title">🗺️ Neighbourhood Analysis</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    top_neighbourhoods = (
        df_filtered.groupby('neighbourhood_cleansed')['price']
        .mean().sort_values(ascending=False)
        .head(top_n).reset_index()
    )
    fig1 = px.bar(
        top_neighbourhoods,
        x='price', y='neighbourhood_cleansed',
        orientation='h',
        title=f'Top {top_n} Most Expensive Neighbourhoods',
        labels={'price': 'Avg Price (€)', 'neighbourhood_cleansed': ''},
        color='price',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(**CHART_THEME, height=500,
        yaxis=dict(categoryorder='total ascending', gridcolor='#F1F5F9'),
        xaxis=dict(gridcolor='#F1F5F9'),
        coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    value_data = neighbourhood_summary[neighbourhood_summary['listing_count'] >= 20].copy()
    value_data['value_score'] = (value_data['avg_rating'] / value_data['avg_price'] * 100).round(3)
    top_value = value_data.sort_values('value_score', ascending=False).head(top_n)
    fig2 = px.bar(
        top_value,
        x='value_score', y='neighbourhood_cleansed',
        orientation='h',
        title=f'Top {top_n} Best Value Neighbourhoods',
        labels={'value_score': 'Value Score (Rating/Price)', 'neighbourhood_cleansed': ''},
        color='value_score',
        color_continuous_scale='Greens'
    )
    fig2.update_layout(**CHART_THEME, height=500,
        yaxis=dict(categoryorder='total ascending', gridcolor='#F1F5F9'),
        xaxis=dict(gridcolor='#F1F5F9'),
        coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── MARKET INSIGHTS ──
st.markdown('<p class="section-title">📈 Market Insights</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    room_type_data = df_filtered.groupby('room_type')['price'].mean().round(2).reset_index()
    room_type_data.columns = ['room_type', 'avg_price']
    room_type_data = room_type_data.sort_values('avg_price', ascending=False)
    fig3 = px.bar(
        room_type_data,
        x='room_type', y='avg_price',
        title='Average Price by Room Type',
        labels={'avg_price': 'Avg Price (€)', 'room_type': ''},
        color='avg_price',
        color_continuous_scale='Blues'
    )
    fig3.update_layout(**CHART_THEME,
        yaxis=dict(gridcolor='#F1F5F9'),
        coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    fig4 = px.line(
        accommodates_analysis.reset_index(),
        x='accommodates', y='avg_price',
        title='Price vs Number of Guests',
        labels={'avg_price': 'Avg Price (€)', 'accommodates': 'Number of Guests'},
        markers=True,
        color_discrete_sequence=['#2563EB']
    )
    fig4.update_layout(**CHART_THEME,
        yaxis=dict(gridcolor='#F1F5F9'),
        xaxis=dict(gridcolor='#F1F5F9'))
    fig4.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── MAP ──
st.markdown('<p class="section-title">📍 Listings by Neighbourhood — Price & Density</p>', unsafe_allow_html=True)

map_data = df_filtered.groupby('neighbourhood_cleansed').agg(
    avg_price=('price', 'mean'),
    count=('id', 'count'),
    lat=('latitude', 'mean'),
    lon=('longitude', 'mean')
).reset_index()

fig_map = px.scatter_mapbox(
    map_data,
    lat='lat', lon='lon',
    color='avg_price',
    size='count',
    hover_name='neighbourhood_cleansed',
    hover_data={'avg_price': ':.0f', 'count': True, 'lat': False, 'lon': False},
    color_continuous_scale=[
        [0, '#22c55e'],
        [0.4, '#eab308'],
        [0.7, '#f97316'],
        [1, '#ef4444']
    ],
    size_max=45,
    zoom=10,
    center=dict(lat=52.52, lon=13.405),
    labels={'avg_price': 'Avg Price (€)', 'count': 'Listings'}
)
fig_map.update_traces(
    marker=dict(opacity=0.75, sizemode='area'),
    hovertemplate="<b>%{hovertext}</b><br>Avg Price: €%{customdata[0]:.0f}<br>Listings: %{customdata[1]}<extra></extra>"
)
fig_map.update_layout(
    mapbox_style='open-street-map',
    height=580,
    margin=dict(r=0, t=0, l=0, b=0),
    paper_bgcolor='white',
    coloraxis_colorbar=dict(
        title='Avg Price (€)',
        thickness=15,
        len=0.6,
        tickformat='€.0f'
    )
)
st.plotly_chart(fig_map, use_container_width=True)
st.markdown("---")

# ── SECTION 5: PRICE PREDICTOR ──
st.markdown('<p class="section-title">🤖 Price Predictor</p>', unsafe_allow_html=True)
st.markdown("Estimate a fair nightly price for a listing based on its features.")

import pickle
import json

@st.cache_resource
def load_model():
    import json
    import pickle
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    with open(os.path.join(BASE_DIR, 'models/dropdown_values.json'), 'r') as f:
        dropdowns = json.load(f)

    # Retrain model fresh
    df_model = pd.read_csv(os.path.join(BASE_DIR, 'processed/listings_clean.csv'))
    features = ['neighbourhood_cleansed', 'room_type', 'accommodates', 'bedrooms', 'beds', 'bathrooms']
    model_df = df_model[features + ['price']].dropna()
    X, y = model_df[features], model_df['price']

    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['neighbourhood_cleansed', 'room_type']),
        ('num', 'passthrough', ['accommodates', 'bedrooms', 'beds', 'bathrooms'])
    ])
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', LinearRegression())])
    pipeline.fit(X, y)

    return pipeline, dropdowns

model, dropdowns = load_model()

col1, col2, col3 = st.columns(3)

with col1:
    pred_neighbourhood = st.selectbox("Neighbourhood", dropdowns['neighbourhoods'], key='pred_neighbourhood')
    pred_room_type = st.selectbox("Room Type", dropdowns['room_types'], key='pred_room_type')

with col2:
    pred_accommodates = st.slider("Guests", 1, 12, 2, key='pred_accommodates')
    pred_bedrooms = st.slider("Bedrooms", 0, 6, 1, key='pred_bedrooms')

with col3:
    pred_beds = st.slider("Beds", 1, 8, 1, key='pred_beds')
    pred_bathrooms = st.slider("Bathrooms", 1, 4, 1, key='pred_bathrooms')

import pandas as pd

input_data = pd.DataFrame([{
    'neighbourhood_cleansed': pred_neighbourhood,
    'room_type': pred_room_type,
    'accommodates': pred_accommodates,
    'bedrooms': pred_bedrooms,
    'beds': pred_beds,
    'bathrooms': float(pred_bathrooms)
}])

predicted_price = model.predict(input_data)[0]
predicted_price = max(10, predicted_price)

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2563EB 100%); 
                padding: 1.5rem; border-radius: 16px; text-align: center; color: white;">
        <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.3rem;">ESTIMATED PRICE</div>
        <div style="font-size: 3rem; font-weight: 700;">€{predicted_price:.0f}</div>
        <div style="font-size: 0.85rem; opacity: 0.8;">per night</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

# ── DATA EXPLORER ──
st.markdown('<p class="section-title">🔎 Explore Listings</p>', unsafe_allow_html=True)
st.dataframe(
    df_filtered[['name', 'neighbourhood_cleansed', 'room_type', 'price', 'accommodates', 'review_scores_rating']]
    .rename(columns={
        'name': 'Name',
        'neighbourhood_cleansed': 'Neighbourhood',
        'room_type': 'Room Type',
        'price': 'Price (€)',
        'accommodates': 'Guests',
        'review_scores_rating': 'Rating'
    })
    .sort_values('Price (€)', ascending=False)
    .reset_index(drop=True),
    use_container_width=True,
    height=400
)

st.markdown("<br><center><span style='color:#94A3B8; font-size:0.8rem'>Data source: Inside Airbnb · Berlin, Germany · 2026</span></center>", unsafe_allow_html=True)