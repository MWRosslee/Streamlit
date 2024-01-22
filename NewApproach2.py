import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Function to create plots based on user input
def create_plot(df, plot_type, x_col, y_cols=None, category_col=None):
    if plot_type == "Line Plot":
        return px.line(df, x=x_col, y=y_cols)
    elif plot_type == "Bar Plot":
        return px.bar(df, x=x_col, y=y_cols)
    elif plot_type == "Scatter Plot":
        return px.scatter(df, x=x_col, y=y_cols)
    elif plot_type == "Pie Chart":
        return px.pie(df, names=category_col, values=x_col)
    # Additional plot types can be added here

# Initialize session state for storing plots and configurations
if 'plots' not in st.session_state:
    st.session_state['plots'] = []

# Title of the app
st.title("Dynamic Data Visualization App")

# File uploader widget
uploaded_file = st.sidebar.file_uploader("Upload your data file", type=["csv", "xls", "xlsm", "xlsx"])

# Function to load data based on file type
def load_data(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

# Check if a file has been uploaded
if uploaded_file:
    df = load_data(uploaded_file)
    st.write("Dataframe Preview:")
    st.write(df.head())

    # Add new plot configuration
    if st.sidebar.button("Add New Plot Configuration"):
        st.session_state['plots'].append({})

    # Iterate over each plot configuration
    for index, plot_config in enumerate(st.session_state['plots']):
        with st.sidebar.container():
            unique_key = f"plot_{index}"
            plot_type = st.selectbox("Choose the type of plot", ["Line Plot", "Bar Plot", "Scatter Plot", "Pie Chart"], key=unique_key+"_type")
            x_column = st.selectbox("Choose the X-axis column", df.columns, key=unique_key+"_x")
            if plot_type != "Pie Chart":
                y_columns = st.multiselect("Choose the Y-axis column(s)", df.columns, key=unique_key+"_y")
                category_column = None
            else:
                category_column = st.selectbox("Choose the category column for Pie Chart", df.columns, key=unique_key+"_cat")
                y_columns = None

            # Update plot configuration
            plot_config.update({"type": plot_type, "x": x_column, "y": y_columns, "cat": category_column})

    # Display all configured plots
    for plot_config in st.session_state['plots']:
        if plot_config.get("type") and plot_config.get("x"):
            if plot_config["type"] != "Pie Chart":
                plot = create_plot(df, plot_config["type"], plot_config["x"], plot_config["y"])
            else:
                plot = create_plot(df, plot_config["type"], plot_config["x"], category_col=plot_config["cat"])
            st.plotly_chart(plot)


# def sideBar():
#     with st.sidebar:
#         selected = option_menu(
#             menu_title="Menu",
#             # menu_title=None,
#             options=["Home", "Progress"],
#             icons=["house", "eye"],
#             menu_icon="cast",  # option
#             default_index=0,  # option
#         )
#     if selected == "Home":
#         try:
#             HomePage()
#             Graphs()
#         except:
#             st.warning("one or more options are mandatory ! ")
#
#     if selected == "Progress":
#         try:
#             ProgressBar()
#             Graphs()
#         except:
#             st.warning("one or more options are mandatory ! ")
#
#
# # print side bar
# sideBar()

footer = """<style>


a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
height:5%;
bottom: 0;
width: 100%;
background-color: #243946;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with  ❤ by <a style='display: block; text-align: center;' href="https://www.heflin.dev/" target="_blank">Samir.s.s</a></p>
</div>
"""

st.write("Please upload a data file to begin.")
