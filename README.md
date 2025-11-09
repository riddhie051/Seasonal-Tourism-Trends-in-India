# 🌤️ Seasonal Tourism Trends in India

## 📘 Project Overview
**Seasonal Tourism Trends in India** is a data-driven web application that helps users plan their trips smartly based on seasonal tourism insights.  
Users can choose the **month they wish to travel**, and the system recommends the **Top 5 Indian States** based on historical tourist patterns, weather suitability, and regional trends.  
From there, users can drill down into **districts → places**, view **interactive graphs**, receive **travel tips**, **budget estimation**, and finally **download a comprehensive report** of their analysis.

---

## 🎯 Objective
To analyze seasonal tourism data across Indian states and assist users in:
- Choosing the best destinations for a selected month.
- Understanding tourism trends through interactive visualizations.
- Getting actionable travel insights such as best time, additional tips, and budget planning.
- Generating a downloadable analytical report for personal or professional use.

---
🚀 Key Features
🧍‍♀️ User Login

Simple login form using name and email.

User sessions are managed using st.session_state so user choices persist during navigation.

📅 Month Selection

User selects a month of travel (January–December).

Based on the month, the app filters the dataset to show the top 5 most visited states.

🗺️ Top 5 States Visualization

Displays the Top 5 States for the selected month.

Generates interactive line charts showing monthly visitor trends across these states using Plotly.

🏖️ State & Place Selection

After choosing a state from the top 5, users select a place within that state.

Provides detailed information for that place, such as:

Average visitors

Average cost per day

Average travel cost per person

Average stay duration

📊 Graphical Analysis

Visitor Distribution: Donut (Pie) chart of top 5 places in the selected state.

Exploration Chart: Alternate visualization (scatter plot) of cost vs. visitors to compare places within the same state.

Monthly Trends Chart: Line graph comparing visitor trends across months for the top 5 states.

🌤️ Seasonal and Weather Insights

The model analyzes historical data to determine the best season and top months to visit the selected place.

Provides weather-specific travel tips (e.g., what to pack, when to visit, etc.).

Suggests alternative destinations (cheaper or less crowded) based on similarity in features.

💰 Budget Estimator

Calculates total trip cost using:

Total = (AvgCostPerDay × Days × People) + (TravelCostPerPerson × People)


Displays a detailed cost breakdown for easy understanding.

📄 Downloadable Trip Summary

Generates a downloadable CSV report summarizing:

User details

Selected month, state, and place

Number of travelers and days

Estimated total budget

🎨 Modern UI

Built with a dark, glassmorphism-inspired interface for a premium aesthetic.

Smooth animations, hover effects, and gradient text give a modern, dashboard-like experience.

🧠 Workflow Summary

The step-by-step interaction flow of the app is as follows:

User Login

Enter name and email to start.

Month Selection

Choose travel month → App filters data for that month.

Top 5 States

Displays most visited states for that month.

Shows a monthly comparison line chart between top 5 states.

Select State → Select Place

Choose a state → See its districts/places.

Choose a place for deeper analysis.

Visual Insights

Pie chart for visitor distribution among top 5 places.

Scatter chart for cost vs. popularity among places.

Trend graphs comparing months and states.

Insights Section

Shows best travel season for the place.

Gives weather tips and alternative destinations.

Budget Estimation

User enters number of people and days.

App calculates and shows total estimated cost.

Download Report

Generates CSV report summarizing all selections and analysis.

📂 Project Structure
Tourism Trends/
│
├── app.py                         # Main Streamlit application
├── seasonal_tourism_data_full.csv  # Dataset used for analysis
├── requirements.txt                # Dependencies (you’ll create this)

📊 Dataset Description

Filename: seasonal_tourism_data_full.csv

Column Name	Description
Month	Month of travel (January–December)
State	Indian state name
District	District inside the state
Place	Tourist destination name
AvgVisitors	Average number of visitors per month
AvgStayDays	Average number of days tourists stay
AvgCostPerDay	Average cost of accommodation and food per person per day
TravelCostPerPerson	Average travel cost to reach the destination per person

🧰 Technologies Used
Component	Technology
Frontend UI	Streamlit
Data Processing	Pandas
Visualizations	Plotly Express & Graph Objects
Styling & Layout	Custom HTML/CSS (Glassmorphism theme)
Data Storage	CSV file (seasonal_tourism_data_full.csv)
Output Format	Downloadable CSV (Trip Report)

⚙️ Installation & Setup
1. Clone or Extract Project

If you have the ZIP file:

unzip Tourism\ Trends.zip
cd Tourism\ Trends


If from GitHub:

git clone https://github.com/<your-username>/Seasonal-Tourism-Trends.git
cd Seasonal-Tourism-Trends

2. Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate      # for Mac/Linux
venv\Scripts\activate         # for Windows

3. Install Dependencies

Create a requirements.txt file and add:

streamlit
pandas
plotly


Then install:

pip install -r requirements.txt

4. Run the App
streamlit run app.py

5. Open in Browser

The app will open automatically in your default browser (usually at):

http://localhost:8501

