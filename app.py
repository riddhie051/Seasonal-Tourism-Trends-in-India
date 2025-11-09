# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- Config ----------
DATA_PATH = "seasonal_tourism_data_full.csv"  # keep CSV in same folder

# ---------- Helpers ----------
month_order = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def init_session():
    defaults = {
        "logged_in": False, "user_name": None, "email": None,
        "month": None, "state": None, "place": None,
        "show_places_graph": False, "show_states_graph": False, "show_monthly_trends": False,
        "show_places_explore": False
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def best_season_for_place(df_all, place):
    df_place = df_all[df_all["Place"] == place]
    if df_place.empty:
        return None, []
    month_vis = df_place.groupby("Month")["AvgVisitors"].mean().reindex(month_order).fillna(0)
    top_months = month_vis.sort_values(ascending=False).head(3).index.tolist()
    season_map = {
        "December": "Winter", "January": "Winter", "February": "Winter",
        "March": "Spring", "April": "Spring", "May": "Summer",
        "June": "Monsoon", "July": "Monsoon", "August": "Monsoon",
        "September": "Autumn", "October": "Autumn", "November": "Autumn"
    }
    seasons = [season_map.get(m, "") for m in top_months]
    season = max(set(seasons), key=seasons.count) if seasons else None
    return season, top_months

def weather_tip_for_season(season):
    tips = {
        "Winter": "Pleasant and cool — carry light woolens for mornings/evenings.",
        "Spring": "Mild weather — great for sightseeing and outdoor walks.",
        "Summer": "Warm/hot — stay hydrated, prefer early-morning outings.",
        "Monsoon": "Expect rain — carry a raincoat/umbrella and check local advisories.",
        "Autumn": "Clear skies and good visibility — ideal for outdoor photography."
    }
    return tips.get(season, "")

def suggest_alternatives(df_state_place, selected_place, top_n=2):
    df = df_state_place.copy()
    df_mean = df.groupby("Place").agg({"AvgCostPerDay":"mean","AvgVisitors":"mean"}).reset_index()
    if df_mean.empty:
        return []
    sel = df_mean[df_mean["Place"] == selected_place]
    if sel.empty:
        return df_mean.sort_values("AvgCostPerDay").head(top_n)["Place"].tolist()
    sel_cost = float(sel["AvgCostPerDay"].iloc[0])
    sel_vis = float(sel["AvgVisitors"].iloc[0])
    cheaper = df_mean[df_mean["AvgCostPerDay"] < sel_cost].sort_values("AvgCostPerDay").head(top_n)["Place"].tolist()
    if len(cheaper) < top_n:
        less_crowd = df_mean[df_mean["AvgVisitors"] < sel_vis].sort_values("AvgVisitors").head(top_n)["Place"].tolist()
        combined = list(dict.fromkeys(cheaper + less_crowd))[:top_n]
        return combined
    return cheaper[:top_n]

# ---------- Page setup ----------
st.set_page_config(page_title="Seasonal Tourism Trends", page_icon="🌌", layout="wide")
init_session()

# ---------- Dark Theme CSS + animations ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Poppins', sans-serif; background: #0b0f14; color: #E6EEF3; }
    .main > div { max-width: 1200px; margin: 0 auto; }
    .glass {
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
      border: 1px solid rgba(255,255,255,0.04);
      border-radius: 14px;
      padding: 18px;
      box-shadow: 0 6px 18px rgba(2,6,23,0.6);
      transition: transform 0.35s ease, box-shadow 0.35s ease;
    }
    .glass:hover { transform: translateY(-6px); box-shadow: 0 14px 28px rgba(2,6,23,0.7); }
    .title {
      font-size: 28px; font-weight:700; color: #A7F3D0;
      background: linear-gradient(90deg,#9AE6B4,#60A5FA,#C084FC);
      -webkit-background-clip: text; background-clip: text; color: transparent;
    }
    .subtitle { color: #9FB4C8; margin-bottom: 8px; }
    .accent { color: #60A5FA; font-weight:600; }
    .small-muted { color: #8b9db0; font-size:13px; }
    .btn {
      background: linear-gradient(90deg,#1f6feb,#6dd3ff); color: #071027; border-radius:10px; padding:8px 16px;
      font-weight:700; border:none;
    }
    .btn:hover { transform: scale(1.03); }
    /* Animate reveal */
    .reveal { animation: fadeInUp 0.55s ease both; }
    @keyframes fadeInUp {
      0% { opacity: 0; transform: translateY(10px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    /* make plotly background consistent */
    .plotly-graph-div .main-svg { background: transparent !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Load dataset ----------
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found at `{DATA_PATH}`. Place the CSV there.")
    st.stop()

# ---------- Login (centered) ----------
if not st.session_state["logged_in"]:
    st.markdown("<div style='display:flex;align-items:center;justify-content:center;margin-top:20px;'>"
                "<div class='glass' style='width:700px;text-align:center;'>"
                "<div class='title'>🌌 Seasonal Tourism Trends in India</div>"
                "<div class='subtitle'>Data-driven travel suggestions</div>"
                "<hr style='border-color:rgba(255,255,255,0.04)'/>"
                "</div></div>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown("<div class='glass reveal'>", unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="Your full name")
        email = st.text_input("Email", placeholder="you@example.com")
        st.markdown("</div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Sign in", help="Sign in to continue", use_container_width=True)
    if submitted:
        if name.strip() and email.strip():
            st.session_state["logged_in"] = True
            st.session_state["user_name"] = name.strip()
            st.session_state["email"] = email.strip()
            st.success(f"Welcome, {st.session_state['user_name']}! ✨")
        else:
            st.warning("Please provide both name and email to continue.")
    st.stop()

# ---------- Main App Layout ----------
# Header
st.markdown("<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>"
            f"<div><div class='title'>🌌 Seasonal Tourism Trends</div>"
            f"<div class='small-muted'>Welcome back, <span class='accent'>{st.session_state['user_name']}</span></div></div>"
            "<div style='text-align:right'><div class='small-muted'></div></div></div>",
            unsafe_allow_html=True)

# Two-column main area
left_col, right_col = st.columns([2,1])

with left_col:
    st.markdown("<div class='glass reveal'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0;color:#BEE3F8'>📅 Select month</h4>", unsafe_allow_html=True)
    st.session_state["month"] = st.selectbox("Choose travel month", month_order, index=month_order.index(st.session_state["month"]) if st.session_state["month"] in month_order else 0)
    st.markdown("</div>", unsafe_allow_html=True)

    # Top 5 States
    st.markdown("<div class='glass reveal' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#A7F3D0'>🌟 Top 5 States — {st.session_state['month']}</h3>", unsafe_allow_html=True)
    df_month = df[df["Month"] == st.session_state["month"]]
    if df_month.empty:
        st.warning("No data for this month. Please pick another month.")
        st.stop()
    top_states_series = df_month.groupby("State")["AvgVisitors"].mean().sort_values(ascending=False).head(5)
    st.dataframe(top_states_series.rename("AvgVisitors").reset_index(), height=200)
    st.markdown("</div>", unsafe_allow_html=True)

    # MONTHLY VISITOR TRENDS for TOP 5 STATES - placed immediately after Top 5 States
    st.markdown("<div class='glass reveal' style='margin-top:14px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#9AE6B4'>📆 Monthly Visitor Trends for Top 5 States</h3>", unsafe_allow_html=True)
    # Prepare data for top 5 states across months
    top_states = top_states_series.index.tolist()
    df_top_states = df[df["State"].isin(top_states)].copy()
    monthly = df_top_states.groupby(["State","Month"])["AvgVisitors"].mean().reset_index()
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values(["State","Month"])
    pivot = monthly.pivot(index="Month", columns="State", values="AvgVisitors").fillna(0).reindex(month_order)
    # Line chart (Plotly) with glow-like styling
    fig_lines = go.Figure()
    colors = ["#00E5FF","#7C4DFF","#FF6B6B","#FFD166","#9AE6B4"]
    for i, state in enumerate(pivot.columns):
        fig_lines.add_trace(go.Scatter(
            x=pivot.index, y=pivot[state],
            mode="lines+markers",
            name=state,
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=6),
            hovertemplate="%{x}<br>%{y:.0f} visitors<br><extra>"+state+"</extra>"
        ))
    fig_lines.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(10,14,20,0.6)',
        xaxis=dict(showgrid=False, tickangle=-45, tickmode="array", tickvals=month_order),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)'),
        margin=dict(t=40, b=40, l=40, r=20),
        height=360,
        legend=dict(title="States", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_lines, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Choose state and places
    st.markdown("<div class='glass reveal' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#C7F9E8'>🏞 Choose state & place</h3>", unsafe_allow_html=True)
    st.session_state["state"] = st.selectbox("Pick a state (top 5)", top_states, index=top_states.index(st.session_state["state"]) if st.session_state["state"] in top_states else 0)
    df_state_month = df_month[df_month["State"] == st.session_state["state"]]
    places = df_state_month["Place"].unique().tolist()
    st.session_state["place"] = st.selectbox("Pick a place", places, index=places.index(st.session_state["place"]) if st.session_state["place"] in places else 0)
    st.markdown("</div>", unsafe_allow_html=True)

    # Donut (Top 5 Places) - button toggles
    st.markdown("<div class='glass reveal' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#BDE8F2'>🍩 Top 5 Places (visitor distribution)</h3>", unsafe_allow_html=True)
    colA, colB = st.columns([1,1])
    with colA:
        if st.button("Show Visitor Trends (Top 5 Places)"):
            st.session_state["show_places_graph"] = True
    with colB:
        if st.button("Explore places (alternate viz)"):
            st.session_state["show_places_explore"] = not st.session_state["show_places_explore"]

    if st.session_state["show_places_graph"]:
        top_places = df_state_month.groupby("Place")["AvgVisitors"].mean().sort_values(ascending=False).head(5)
        if not top_places.empty:
            fig_pie = px.pie(names=top_places.index, values=top_places.values, hole=0.45)
            fig_pie.update_traces(textinfo='percent+label', textposition='inside', marker=dict(line=dict(color='#0b0f14', width=2)))
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(t=10))
            st.plotly_chart(fig_pie, use_container_width=True)
    if st.session_state["show_places_explore"]:
        # Alternate attractive viz - scatter sized by AvgVisitors, colored by AvgCostPerDay
        agg = df_state_month.groupby("Place").agg({"AvgVisitors":"mean","AvgCostPerDay":"mean"}).reset_index()
        if not agg.empty:
            fig_scatter = px.scatter(agg, x="AvgCostPerDay", y="AvgVisitors", size="AvgVisitors", hover_name="Place",
                                     color="AvgCostPerDay", color_continuous_scale=px.colors.sequential.Viridis, height=380)
            fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10))
            st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Best season, tips, suggestions, budget
    st.markdown("<div class='glass reveal' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#D6F6FF'>🌤 Best season & Tips</h3>", unsafe_allow_html=True)
    season, top_months = best_season_for_place(df, st.session_state["place"])
    if season:
        st.markdown(f"**Best season:** {season}")
        st.markdown(f"**Top months historically:** {', '.join(top_months)}")
        tip = weather_tip_for_season(season)
        if tip:
            st.info(tip)
    else:
        st.write("No season info available.")

    # Suggestions
    suggestions = suggest_alternatives(df_state_month, st.session_state["place"], top_n=2)
    if suggestions:
        st.markdown("**You may also like:** " + ", ".join(suggestions))
    st.markdown("</div>", unsafe_allow_html=True)

    # Budget estimator (kept exactly same logic)
    st.markdown("<div class='glass reveal' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FFD7A8'>💰 Trip Budget Estimator</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        num_people = st.number_input("Number of travelers", min_value=1, value=2, key="num_people")
    with col2:
        num_days = st.number_input("Number of days", min_value=1, value=3, key="num_days")
    if st.button("Calculate Budget"):
        place_row = df_state_month[df_state_month["Place"] == st.session_state["place"]].iloc[0]
        total = (place_row["AvgCostPerDay"] * num_days * num_people) + (place_row["TravelCostPerPerson"] * num_people)
        breakdown = f"Accommodation+food: ₹{place_row['AvgCostPerDay']:,}/day per person\nTravel per person: ₹{place_row['TravelCostPerPerson']:,}"
        st.success(f"Estimated total budget: ₹{total:,.0f}")
        st.write(breakdown)
    st.markdown("</div>", unsafe_allow_html=True)

    # Save trip plan (unchanged functionality)
    st.markdown("<div class='glass reveal' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#C9F7E9'>💾 Save Your Trip Plan</h3>", unsafe_allow_html=True)
    if st.button("Prepare trip summary for download"):
        place_row = df_state_month[df_state_month["Place"] == st.session_state["place"]].iloc[0]
        total = (place_row["AvgCostPerDay"] * num_days * num_people) + (place_row["TravelCostPerPerson"] * num_people)
        summary = {
            "User": st.session_state["user_name"],
            "Email": st.session_state["email"],
            "Month": st.session_state["month"],
            "State": st.session_state["state"],
            "Place": st.session_state["place"],
            "Travelers": int(num_people),
            "Days": int(num_days),
            "EstimatedBudgetINR": int(total)
        }
        df_summary = pd.DataFrame([summary])
        csv = df_summary.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download trip plan (CSV)", data=csv, file_name="trip_plan.csv", mime="text/csv")
        st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Right column quick summary card
    st.markdown("<div class='glass reveal' style='position:sticky;top:20px;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#A7F3D0'>Your Selection</h4>", unsafe_allow_html=True)
    st.write(f"**Month:** {st.session_state['month']}")
    st.write(f"**State:** {st.session_state['state']}")
    st.write(f"**Place:** {st.session_state['place']}")
    st.write("---")
    st.markdown("<h4 style='color:#9AE6B4'>Quick Stats</h4>", unsafe_allow_html=True)
    try:
        pr = df_state_month[df_state_month["Place"] == st.session_state["place"]].iloc[0]
        st.write(f"Avg visitors (this month): {int(pr['AvgVisitors']):,}")
        st.write(f"Avg stay days: {int(pr['AvgStayDays'])}")
        st.write(f"Avg cost/day: ₹{int(pr['AvgCostPerDay']):,}")
        st.write(f"Avg travel cost/person: ₹{int(pr['TravelCostPerPerson']):,}")
    except Exception:
        st.write("No data to show.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div style='margin-top:18px;text-align:center;color:#7f94a6'>"
            "✨ Developed by Riddhie Sengar/div>",
            unsafe_allow_html=True)
