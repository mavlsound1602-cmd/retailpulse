import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title='RetailPulse', layout='wide')
st.title('RetailPulse — Demand Forecasting & Inventory Dashboard')
st.caption('Supply Chain Analytics | Corporación Favorita Dataset')

DATA = 'app_data'

@st.cache_data
def load_data():
    df = pd.read_csv(f'{DATA}/business_outputs.csv')
    oil = pd.read_csv(f'{DATA}/oil.csv', parse_dates=['date'])
    store_perf = pd.read_csv(f'{DATA}/store_performance.csv')
    weekly = pd.read_csv(f'{DATA}/weekly_seasonality.csv')
    yoy = pd.read_csv(f'{DATA}/yoy_growth.csv')
    oil_sales = pd.read_csv(f'{DATA}/oil_vs_sales.csv')
    sarima = pd.read_csv(f'{DATA}/sarima_results.csv')
    return df, oil, store_perf, weekly, yoy, oil_sales, sarima

with st.spinner('Loading data...'):
    df, oil, store_perf, weekly, yoy, oil_sales, sarima = load_data()

tab1, tab2, tab3, tab4, tab5 = st.tabs(['P&L & Inventory', 'Store Performance', 'Seasonality', 'External Signals', 'Model Comparison'])

with tab1:
    st.subheader('P&L Overview')
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric('Annual Revenue', f"${df['annual_revenue'].sum()/1e6:.2f}M")
    k2.metric('Revenue at Risk', f"${df['annual_revenue_at_risk'].sum()/1e6:.2f}M", delta=f"{df['annual_revenue_at_risk'].sum()/df['annual_revenue'].sum()*100:.1f}%", delta_color='inverse')
    k3.metric('Stockout Cost', f"${df['annual_stockout_cost'].sum()/1e6:.2f}M", delta_color='inverse')
    k4.metric('Critical Alerts', f"{len(df[df['alert_urgency']=='Critical'])}", delta_color='inverse')
    k5.metric('Reorder Alerts', f"{len(df[df['alert_urgency']=='Reorder Now'])}")
    st.divider()
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Revenue at Risk by Family')
        fam = df.groupby('family').agg(annual_revenue=('annual_revenue','sum'), revenue_at_risk=('annual_revenue_at_risk','sum')).reset_index().sort_values('revenue_at_risk', ascending=False).head(10)
        fig = go.Figure()
        fig.add_bar(x=fam['family'], y=fam['annual_revenue'], name='Total Revenue', marker_color='#1D9E75')
        fig.add_bar(x=fam['family'], y=fam['revenue_at_risk'], name='At Risk', marker_color='#D85A30')
        fig.update_layout(height=320, barmode='overlay', xaxis_tickangle=-35, legend=dict(orientation='h', y=1.1), margin=dict(t=10,b=80))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader('Stock Alert Status')
        alert_counts = df['alert_urgency'].value_counts().reset_index()
        alert_counts.columns = ['status','count']
        fig2 = px.pie(alert_counts, values='count', names='status',
                      color='status', color_discrete_map={'OK':'#1D9E75','Reorder Now':'#EF9F27','Critical':'#D85A30'})
        fig2.update_layout(height=320, margin=dict(t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True)
    st.subheader('Reorder Alert Table')
    urgency_filter = st.multiselect('Filter by status', ['OK','Reorder Now','Critical'], default=['Reorder Now','Critical'])
    alert_df = df[df['alert_urgency'].isin(urgency_filter)].sort_values(['alert_urgency','annual_revenue_at_risk'], ascending=[True,False])
    alert_df = alert_df[['item_nbr','family','ABC_XYZ','alert_urgency','current_stock','reorder_point','eoq','annual_revenue','annual_revenue_at_risk','annual_stockout_cost']]
    st.dataframe(alert_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader('Store Performance')
    col1,col2 = st.columns(2)
    with col1:
        top10 = store_perf.head(10)
        fig3 = px.bar(top10, x='store_nbr', y='total_units', color='type',
                      labels={'store_nbr':'Store','total_units':'Total Units'},
                      color_discrete_sequence=['#1D9E75','#378ADD','#EF9F27','#D85A30','#888780'])
        fig3.update_layout(height=320, margin=dict(t=10,b=10), xaxis={'type':'category'})
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        fig4 = px.scatter(store_perf, x='avg_transaction', y='total_units',
                          color='type', size='unique_items_sold', hover_data=['city','store_nbr'],
                          labels={'avg_transaction':'Avg Basket Size','total_units':'Total Units'},
                          color_discrete_sequence=['#1D9E75','#378ADD','#EF9F27','#D85A30','#888780'])
        fig4.update_layout(height=320, margin=dict(t=10,b=10))
        st.plotly_chart(fig4, use_container_width=True)
    st.subheader('All Stores')
    st.dataframe(store_perf.sort_values('total_units', ascending=False), use_container_width=True, hide_index=True)

with tab3:
    st.subheader('Seasonality Analysis')
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('##### Day of week pattern')
        day_order = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        weekly['day_name'] = pd.Categorical(weekly['day_name'], categories=day_order, ordered=True)
        weekly = weekly.sort_values('day_name')
        fig5 = px.bar(weekly, x='day_name', y='avg_daily_units',
                      color='avg_daily_units', color_continuous_scale='Teal',
                      labels={'day_name':'Day','avg_daily_units':'Avg Units'})
        fig5.update_layout(height=300, margin=dict(t=10,b=10), coloraxis_showscale=False)
        st.plotly_chart(fig5, use_container_width=True)
    with col2:
        st.markdown('##### YoY growth by month (2015 to 2016)')
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        yoy['month_name'] = yoy['month'].apply(lambda x: month_names[x-1])
        fig6 = px.bar(yoy, x='month_name', y='yoy_growth_pct',
                      color='yoy_growth_pct',
                      color_continuous_scale=['#D85A30','#EF9F27','#1D9E75'],
                      labels={'month_name':'Month','yoy_growth_pct':'YoY Growth %'})
        fig6.update_layout(height=300, margin=dict(t=10,b=10), coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)
    st.subheader('Multi-year Monthly Trend')
    fig7 = go.Figure()
    for yr, col in [('y2014','#888780'),('y2015','#378ADD'),('y2016','#1D9E75')]:
        fig7.add_trace(go.Scatter(x=month_names, y=yoy[yr]/1e6, mode='lines+markers',
                                  name=yr[-4:], line=dict(color=col, width=2)))
    fig7.update_layout(height=300, margin=dict(t=10,b=10), yaxis_title='Units (M)', legend=dict(orientation='h', y=1.1))
    st.plotly_chart(fig7, use_container_width=True)

with tab4:
    st.subheader('External Signals')
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('##### Oil price vs avg daily sales')
        fig8 = px.line(oil_sales, x='oil_price_bucket', y='avg_daily_units',
                       markers=True, labels={'oil_price_bucket':'Oil Price ($/barrel)','avg_daily_units':'Avg Daily Units'},
                       color_discrete_sequence=['#D85A30'])
        fig8.update_layout(height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig8, use_container_width=True)
    with col2:
        st.markdown('##### Oil price trend over time')
        fig9 = px.line(oil.dropna(), x='date', y='dcoilwtico',
                       labels={'dcoilwtico':'USD/barrel'},
                       color_discrete_sequence=['#D85A30'])
        fig9.update_layout(height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig9, use_container_width=True)
    st.divider()
    st.subheader('Inventory Calculator')
    col1,col2,col3 = st.columns(3)
    with col1:
        avg_demand = st.number_input('Avg daily demand (units)', value=147.0, step=1.0)
        std_demand = st.number_input('Std dev of demand', value=52.0, step=1.0)
    with col2:
        lead_time = st.number_input('Lead time (days)', value=7, step=1)
        service_level = st.selectbox('Service level', ['90% (z=1.28)','95% (z=1.65)','99% (z=2.33)'])
        z = float(service_level.split('z=')[1].replace(')',''))
    with col3:
        ordering_cost = st.number_input('Ordering cost ($)', value=50.0, step=5.0)
        holding_cost = st.number_input('Holding cost ($/unit/year)', value=2.0, step=0.5)
    safety_stock = z * std_demand * np.sqrt(lead_time)
    reorder_point = (avg_demand * lead_time) + safety_stock
    eoq = np.sqrt((2 * avg_demand * 365 * ordering_cost) / holding_cost)
    r1,r2,r3,r4 = st.columns(4)
    r1.metric('Safety Stock', f'{safety_stock:.0f} units')
    r2.metric('Reorder Point', f'{reorder_point:.0f} units')
    r3.metric('EOQ', f'{eoq:.0f} units')
    r4.metric('Orders/Year', f'{avg_demand*365/eoq:.0f}')

with tab5:
    st.subheader('Model Comparison — LightGBM vs SARIMA')
    k1,k2,k3 = st.columns(3)
    k1.metric('LightGBM MAE%', '18.1%', delta='baseline')
    k2.metric('SARIMA MAE%', '16.4%', delta='-1.7% better', delta_color='inverse')
    k3.metric('Winner on AY items', 'SARIMA')
    st.divider()
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('##### MAE% comparison')
        fig_cmp = go.Figure()
        fig_cmp.add_bar(x=['LightGBM','SARIMA'], y=[18.1, 16.4],
                        marker_color=['#378ADD','#1D9E75'],
                        text=['18.1%','16.4%'], textposition='outside')
        fig_cmp.update_layout(height=300, margin=dict(t=20,b=10),
                               yaxis=dict(range=[0,25], title='MAE %'),
                               showlegend=False)
        st.plotly_chart(fig_cmp, use_container_width=True)
    with col2:
        st.markdown('##### Model routing by segment')
        routing_df = pd.DataFrame([
            {'Segment':'AX','Model':'SARIMA','Reason':'Stable — weekly seasonality sufficient'},
            {'Segment':'AY','Model':'SARIMA','Reason':'Moderate variability — outperforms LightGBM'},
            {'Segment':'AZ','Model':'LightGBM','Reason':'Erratic — needs ML feature power'},
            {'Segment':'BX','Model':'SARIMA','Reason':'Stable enough for classical model'},
            {'Segment':'BY','Model':'LightGBM','Reason':'Moderate value — ML for flexibility'},
            {'Segment':'BZ','Model':'LightGBM','Reason':'Erratic — ML handles it better'},
            {'Segment':'CX','Model':'Moving Avg','Reason':'Low value — simple model sufficient'},
            {'Segment':'CY','Model':'Moving Avg','Reason':'Low value — simple model sufficient'},
            {'Segment':'CZ','Model':'None','Reason':'Too erratic and low value'},
        ])
        st.dataframe(routing_df, use_container_width=True, hide_index=True)
    st.divider()
    st.markdown('##### SARIMA inventory output')
    st.dataframe(sarima, use_container_width=True, hide_index=True)
    st.info('SARIMA outperforms LightGBM on AY items because weekly seasonality is the dominant signal. LightGBM wins on AZ items where oil prices, promotions, and holidays drive erratic spikes.')
