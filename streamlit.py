import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
view = st.sidebar.selectbox("Choose dashboard view:", ["Overview Analysis", "Affiliate Analysis", "New View (Coming Soon)"])

def load_data(file_name):
    conn = st.connection('s3', type=FilesConnection)
    df = conn.read(file_name, input_format="csv", ttl=600)
    return df

def show_overview():
    
    df_overview = load_data("thorchain-data/thorchain_overview.csv")
    df_overview["month_name"] = pd.Categorical(df_overview["month_name"], ordered=True, categories=df_overview["month_name"][::-1])
    df_overview = df_overview.sort_values("month_name") 

    st.title("⚡️ Thorchain Overview Dashboard")
    st.caption("Unified view of Thorchain activity")

    st.markdown("### 💰 Key Metrics")
    overview_kpi1, overview_kpi2 = st.columns(2)
    overview_kpi1.metric("Swap Volume (Apr 2025)", f"${df_overview['volume'].iloc[-2]:,.0f}", delta = f"{df_overview['volume_growth'].iloc[-2]:,.0f}%")
    overview_kpi2.metric("Number of Swaps (Apr 2025)", f"{df_overview['n_swaps'].iloc[-2]:,.0f}", delta = f"{df_overview['swaps_growth'].iloc[-2]:,.0f}%")
    overview_kpi3, overview_kpi4 = st.columns(2)
    overview_kpi3.metric("Liquidity Fees (Apr 2025)", f"${df_overview['liquidity_fee'].iloc[-2]:,.0f}", delta = f"{df_overview['liquidity_fee_growth'].iloc[-2]:,.0f}%")
    overview_kpi4.metric("Number of New Users (Apr 2025)", f"{df_overview['n_new_user'].iloc[-2]:,.0f}", delta = f"{df_overview['new_user_growth'].iloc[-2]:,.0f}%")

    st.markdown("---")
    st.markdown("### 📊 Monthly Swap Volume & Growth Rate")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_overview["month_name"],
        y=df_overview["volume"],
        name="Swap Volume (USD)",
        marker=dict(color="#ADD8E6",line=dict(width=0)),
        yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=df_overview["month_name"],
        y=df_overview["volume_growth"],
        name="Volume Growth (%)",
        mode="lines+markers",
        marker=dict(color="#4682B4"),
        yaxis="y2"
    ))
    fig.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Swap Volume (USD)", side="left", showgrid=True, zeroline=True, rangemode="tozero"),
        yaxis2=dict(title="Growth (%)", overlaying="y", side="right", showgrid = False, zeroline=True, rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 👥 Monthly Swappers & Growth Rate")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_overview["month_name"],
        y=df_overview["n_swappers"],
        name="Swappers",
        marker=dict(color="#98FB98", line=dict(width=0)),
        yaxis="y1"
    ))
    fig2.add_trace(go.Scatter(
        x=df_overview["month_name"],
        y=df_overview["swappers_growth"],
        name="Swapper Growth (%)",
        mode="lines+markers",
        marker=dict(color="#2E8B57"),
        yaxis="y2"
    ))
    fig2.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Number of Swappers", side="left", showgrid=True, tickformat="~s", zeroline=True, rangemode="tozero"),
        yaxis2=dict(title="Growth (%)", side="right", overlaying="y", showgrid=False, tickformat=".1f", zeroline=True, rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🔄 Monthly Number of Swaps & Growth Rate")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=df_overview["month_name"],
        y=df_overview["n_swaps"],
        name="Number of Swaps",
        marker=dict(color="#DDA0DD", line=dict(width=0)),
        yaxis="y1"
    ))
    fig3.add_trace(go.Scatter(
        x=df_overview["month_name"],
        y=df_overview["swaps_growth"],
        name="Swap Growth (%)",
        mode="lines+markers",
        marker=dict(color="#9370DB"),
        yaxis="y2"
    ))
    fig3.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Swaps", side="left", showgrid=True, tickformat="~s", zeroline=True, rangemode="tozero"),
        yaxis2=dict(title="Growth (%)", side="right", overlaying="y", showgrid=False, tickformat=".1f", zeroline=True, rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 💰 Monthly Liquidity Fees & Growth Rate")
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=df_overview["month_name"],
        y=df_overview["liquidity_fee"],
        name="Liquidity Fee (USD)",
        marker=dict(color="#F08080", line=dict(width=0)),
        yaxis="y1"
    ))
    fig4.add_trace(go.Scatter(
        x=df_overview["month_name"],
        y=df_overview["liquidity_fee_growth"],
        name="Liquidity Fee Growth (%)",
        mode="lines+markers",
        marker=dict(color="#CD5C5C"),
        yaxis="y2"
    ))
    fig4.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Liquidity Fees (USD)", side="left", showgrid=True, tickformat="~s", zeroline=True, rangemode="tozero"),
        yaxis2=dict(title="Growth (%)", side="right", overlaying="y", showgrid=False, tickformat=".1f", zeroline=True, rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### 🧑🏻‍💻 Monthly New Users & Growth Rate")
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=df_overview["month_name"],
        y=df_overview["n_new_user"],
        name="New Users",
        marker=dict(color="#FFDAB9", line=dict(width=0)),
        yaxis="y1"
    ))
    fig5.add_trace(go.Scatter(
        x=df_overview["month_name"],
        y=df_overview["new_user_growth"],
        name="New User Growth (%)",
        mode="lines+markers",
        marker=dict(color="#FF8C00"),
        yaxis="y2"
    ))
    fig5.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="New Users", side="left", showgrid=True, tickformat="~s", zeroline=True, rangemode="tozero"),
        yaxis2=dict(title="Growth (%)", side="right", overlaying="y", showgrid=False, tickformat=".1f", zeroline=True, rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    st.plotly_chart(fig5, use_container_width=True)
    
     # --- Old vs New Users ---

    st.markdown("### 🧩 Daily Share of Swap Volume by User Type")

    df_users = load_data("thorchain-data/thorchain_users.csv")
    df_users["date"] = pd.to_datetime(df_users["date"])
    df_daily = df_users.groupby(["date", "type"])["amount"].sum().reset_index()

    df_pivot = df_daily.pivot(index="date", columns="type", values="amount").fillna(0)
    df_pct = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100
    df_pct = df_pct.reset_index()
    df_melted = df_pct.melt(id_vars="date", var_name="User Type", value_name="Percent")

    fig = px.area(
        df_melted,
        x="date",
        y="Percent",
        color="User Type",
        line_shape="spline",
        color_discrete_map={
            "new": "#FFA500",  # light orange
            "old": "#4682B4"   # light blue
        },
        labels={"date": "Date", "Percent": "Swap Volume Share (%)"},
    )
    fig.update_layout(
        yaxis=dict(range=[0, 100], ticksuffix="%", title="Share (%)"),
        xaxis=dict(title="Date"),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

def show_affiliate_view():
    # --- Load Data ---

    df_fee = load_data("thorchain-data/thorchain_affiliate_fee.csv")
    df_fee = df_fee[["affiliates", "affiliate_fee"]]
    df_fee = df_fee.sort_values(by="affiliate_fee", ascending=False)

    df_vol = load_data("thorchain-data/thorchain_affiliate_volume.csv")
    df_vol = df_vol[["affiliates", "volume", "volume_growth"]]
    df_vol = df_vol.sort_values(by="volume", ascending=False)

    # --- Dashboard Title ---
    st.title("⚡️ Thorchain Affiliates Dashboard")
    st.caption("Unified view of affiliate earnings and volume activity")

    # --- KPI Metrics ---
    st.markdown("### 💰 Key Metrics")
    aff_kpi1, aff_kpi2 = st.columns(2)
    aff_kpi1.metric("Total Affiliate Fee (Apr 2025)", f"${df_fee['affiliate_fee'].sum():,.0f}")
    aff_kpi2.metric("Total Trading Volume (Apr 2025)", f"${df_vol['volume'].sum():,.0f}")

    st.markdown("---")

    # --- Page Config ---
    st.markdown("### 📈 Affiliate Trading Volume Breakdown")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Affiliate Volume *(Apr 2025)***")
        fig_vol_bar = px.bar(
            df_vol,
            x="volume",
            y="affiliates",
            orientation="h",
            text_auto=".2s",
            color="volume",
            color_continuous_scale="viridis",
            labels={"volume": "Volume (USD)", "affiliates": "Affiliate"}
        )
        fig_vol_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_vol_bar, use_container_width=True)

    with col2:
        st.markdown("**Affiliate Share of Total Volume *(Apr 2025)***")
        fig_vol_pie = px.pie(
            df_vol,
            values="volume",
            names="affiliates",
            hole=0.6
        )
        st.plotly_chart(fig_vol_pie, use_container_width=True)

    st.markdown("### 💸 Affiliate Fees Breakdown")
    col3, col4 = st.columns(2)

    # --- Bar Chart ---
    with col3:
        st.markdown("**Total Affiliate Fees *(Apr 2025)***")
        fig_bar = px.bar(df_fee, x="affiliate_fee", y="affiliates", orientation="h",
                        labels={"affiliate_fee": "Affiliate Fee (USD) ", "affiliates": "Affiliate "},
                        text_auto=".2s", color="affiliate_fee",
                        color_continuous_scale="blues")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Pie Chart ---
    with col4:
        st.markdown("**Affiliate Share of Total Fees *(Apr 2025)***")
        fig_pie = px.pie(df_fee, values="affiliate_fee", names="affiliates",
                        hole=0.6)
        st.plotly_chart(fig_pie, use_container_width=True)

def show_new_view():
    st.title("🚧 Under Construction")
    st.info("This space is reserved for future activity analytics. Coming soon!")

if view == "Overview Analysis":
    show_overview()
elif view == "Affiliate Analysis":
    show_affiliate_view()
elif view == "New View (Coming Soon)":
    show_new_view()