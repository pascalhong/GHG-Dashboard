import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & CORPORATE STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Corporate GHG Dashboard 2024",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für den Corporate Look
st.markdown("""
    <style>
    /* Hintergrund leicht abgedunkelt für besseren Kontrast der Charts */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Sidebar anpassen */
    [data-testid="stSidebar"] {
        background-color: #0f2537;
        color: white;
    }
    /* KPI Metric Cards stylen */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #10b981; /* Grüner Akzent */
    }
    /* Streamlit Main Menu und Footer verstecken für Clean Look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Corporate Farbpalette für Charts (Blau, Grün, Grau, Orange-Töne)
CORP_COLORS = ['#10b981', '#0ea5e9', '#334155', '#f59e0b', '#8b5cf6', '#ef4444']

# -----------------------------------------------------------------------------
# 2. DATA LOADING & PREPROCESSING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # HIER KOMMT DEIN EIGENTLICHER CODE ZUM LADEN DER EXCEL HINEIN:
    # file = "GHG_Master_Data_Clean.xlsx"
    # df = pd.read_excel(file, sheet_name="Master_Long")
    # sites_df = pd.read_excel(file, sheet_name="Sites_Clean")
    
    # --- Dummy-Daten zur Veranschaulichung des Layouts (Bitte durch deine Daten ersetzen) ---
    data = {
        'Reporting period': [2024]*100,
        'Region': ['Europe', 'North America', 'Asia Pacific', 'Europe', 'North America'] * 20,
        'Site': ['HQ Zurich', 'Boston Plant', 'Singapore Office', 'Leipzig Prod', 'Toronto Dist'] * 20,
        'Scope': ['Scope 1', 'Scope 2', 'Scope 3', 'Scope 3', 'Scope 1'] * 20,
        'Category': ['Stationary Combustion', 'Purchased Electricity', 'Business Travel', 'Waste', 'Mobile Combustion'] * 20,
        'Value_for_chart': [150.5, 420.0, 50.2, 25.0, 80.0] * 20, # Emissionswert in tCO2e
        'Data Quality': ['Actual', 'Estimate', 'Actual', 'Estimate', 'Actual'] * 20
    }
    df = pd.DataFrame(data)
    # -----------------------------------------------------------------------------------------
    
    # Sicherstellen, dass die Wert-Spalte numerisch ist
    if 'Value_for_chart' in df.columns:
        df['Value_for_chart'] = pd.to_numeric(df['Value_for_chart'], errors="coerce")
        
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & GLOBALE FILTER
# -----------------------------------------------------------------------------
st.sidebar.markdown("##**Sustainability Portal**")
st.sidebar.caption("Reporting Period: 2024")
st.sidebar.markdown("---")

# Menü-Steuerung
page = st.sidebar.radio("Navigation", [
    "Executive Summary", 
    "Scope Deep-Dive", 
    "Site Performance", 
    "Data Quality & Audit"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### Globale Filter")

# Dynamische Filter basierend auf den Daten
if 'Region' in df.columns:
    regions = df['Region'].dropna().unique().tolist()
    selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
    df = df[df['Region'].isin(selected_regions)]

if 'Site' in df.columns:
    sites = df['Site'].dropna().unique().tolist()
    selected_sites = st.sidebar.multiselect("Standorte", sites, default=sites)
    df = df[df['Site'].isin(selected_sites)]

# -----------------------------------------------------------------------------
# 4. DASHBOARD PAGES (VIEWS)
# -----------------------------------------------------------------------------

# ================= PAGE 1: EXECUTIVE SUMMARY =================
if page == "Executive Summary":
    st.title("Executive Summary")
    st.markdown("Unternehmensweiter Überblick der Treibhausgasemissionen (in tCO₂e).")
    
    # KPIs berechnen
    total_emissions = df['Value_for_chart'].sum()
    scope1 = df[df['Scope'] == 'Scope 1']['Value_for_chart'].sum() if 'Scope 1' in df['Scope'].values else 0
    scope2 = df[df['Scope'] == 'Scope 2']['Value_for_chart'].sum() if 'Scope 2' in df['Scope'].values else 0
    scope3 = df[df['Scope'] == 'Scope 3']['Value_for_chart'].sum() if 'Scope 3' in df['Scope'].values else 0
    
    # KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Total Carbon Footprint (tCO₂e)", value=f"{total_emissions:,.0f}")
    col2.metric(label="Scope 1", value=f"{scope1:,.0f}")
    col3.metric(label="Scope 2", value=f"{scope2:,.0f}")
    col4.metric(label="Scope 3", value=f"{scope3:,.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualisierungen Row 1
    col_chart1, col_chart2 = st.columns([1, 1.5])
    
    with col_chart1:
        st.subheader("Emissionsverteilung")
        scope_dist = df.groupby('Scope', as_index=False)['Value_for_chart'].sum()
        fig_donut = px.pie(scope_dist, values='Value_for_chart', names='Scope', hole=0.6,
                           color_discrete_sequence=CORP_COLORS)
        fig_donut.update_layout(margin=dict(t=20, b=20, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)",
                                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_chart2:
        st.subheader("Top Emissions-Kategorien")
        top_cats = df.groupby('Category', as_index=False)['Value_for_chart'].sum().sort_values(by='Value_for_chart', ascending=False).head(7)
        fig_bar = px.bar(top_cats, x='Value_for_chart', y='Category', orientation='h',
                         color_discrete_sequence=[CORP_COLORS[1]])
        fig_bar.update_layout(margin=dict(t=20, b=20, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)", 
                              yaxis={'categoryorder':'total ascending'}, xaxis_title="Emissionen (tCO₂e)", yaxis_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

# ================= PAGE 2: SCOPE DEEP-DIVE =================
elif page == "🔍 Scope Deep-Dive":
    st.title("🔍 Scope Deep-Dive")
    st.markdown("Identifiziere Hotspots entlang der gesamten Wertschöpfungskette.")
    
    # Interaktive Auswahl
    scope_sel = st.selectbox("Scope filtern:", ["Alle Scopes", "Scope 1", "Scope 2", "Scope 3"])
    plot_df = df if scope_sel == "Alle Scopes" else df[df['Scope'] == scope_sel]
    
    # Advanced Treemap (Sehr beliebt in Corporate Dashboards)
    st.subheader("Hierarchische Emissionsstruktur (Treemap)")
    st.caption("Klicke auf eine Box, um hineinzuzoomen (Scope -> Kategorie -> Standort).")
    
    fig_tree = px.treemap(
        plot_df, 
        path=['Scope', 'Category', 'Site'], 
        values='Value_for_chart',
        color='Value_for_chart', 
        color_continuous_scale='Teal'
    )
    fig_tree.update_layout(margin=dict(t=20, b=20, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_tree, use_container_width=True)

# ================= PAGE 3: SITE PERFORMANCE =================
elif page == "Site Performance":
    st.title("Site Performance")
    st.markdown("Vergleich der Emissionsdaten auf Standortebene.")
    
    site_emissions = df.groupby(['Site', 'Region'], as_index=False)['Value_for_chart'].sum().sort_values(by='Value_for_chart', ascending=False)
    
    fig_site = px.bar(
        site_emissions, 
        x='Site', 
        y='Value_for_chart', 
        color='Region',
        color_discrete_sequence=CORP_COLORS,
        text_auto='.2s'
    )
    fig_site.update_layout(
        xaxis_tickangle=-45, 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title="tCO₂e",
        xaxis_title=""
    )
    st.plotly_chart(fig_site, use_container_width=True)

# ================= PAGE 4: DATA QUALITY & AUDIT =================
elif page == "Data Quality & Audit":
    st.title("Data Quality & Audit")
    st.markdown("Überprüfung der Datenqualität (Reale Messwerte vs. Extrapolationen/Schätzungen) für das Audit-Reporting.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Data Quality Split")
        if 'Data Quality' in df.columns:
            dq_df = df.groupby('Data Quality', as_index=False)['Value_for_chart'].sum()
            fig_dq = px.pie(dq_df, values='Value_for_chart', names='Data Quality', 
                            color='Data Quality', 
                            color_discrete_map={'Actual': '#10b981', 'Estimate': '#ef4444', 'Spend-based': '#f59e0b'})
            fig_dq.update_layout(margin=dict(t=20, b=20, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_dq, use_container_width=True)
        else:
            st.warning("Spalte 'Data Quality' nicht im Datensatz gefunden.")
            
    with col2:
        st.subheader("Rohdaten Detail-Tabelle")
        # Detailtabelle sauber formatieren
        display_columns = ["Reporting period", "Scope", "Region", "Site", "Category", "Value_for_chart", "Data Quality"]
        display_columns = [col for col in display_columns if col in df.columns]
        
        st.dataframe(df[display_columns], use_container_width=True, height=300)
        
        # Sicherer CSV Export Button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Aktuellen Datensatz exportieren (CSV)",
            data=csv_data,
            file_name='ghg_audit_export_2024.csv',
            mime='text/csv',
            help="Lädt die aktuell gefilterten Daten zur weiteren Bearbeitung im Excel herunter."
        )