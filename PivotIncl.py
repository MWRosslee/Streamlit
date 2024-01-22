import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Title of the app
st.title("Dynamic Data Visualization with Pivot Table")

# File uploader widget
uploaded_file = st.sidebar.file_uploader("Upload your data file", type=["csv", "xls", "xlsm", "xlsx"])

# Function to load data based on file type
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Check if a file has been uploaded
if uploaded_file:
    df = load_data(uploaded_file)
    st.write("Dataframe Preview:")
    st.write(df.head())

    # Pivot Table Configuration
    st.sidebar.header("Pivot Table Configuration")
    index_column = st.sidebar.selectbox("Select index column for pivot table", df.columns)
    columns_column = st.sidebar.selectbox("Select columns column for pivot table", df.columns)
    values_column = st.sidebar.selectbox("Select values column for pivot table", df.columns)

    # Creating the Pivot Table
    pivot_table = pd.pivot_table(df, values=values_column, index=index_column, columns=columns_column, aggfunc=np.sum)

    # Displaying the Pivot Table
    st.write("Pivot Table:")
    st.write(pivot_table)

    # Plot Configuration
    st.sidebar.header("Plot Configuration")
    plot_type = st.sidebar.selectbox("Select plot type", ["Bar Plot", "Line Plot", "Area Plot"])

    # Creating and Displaying the Plot
    if st.sidebar.button("Create Plot"):
        if plot_type == "Bar Plot":
            fig = px.bar(pivot_table.reset_index(), x=index_column, y=pivot_table.columns)
        elif plot_type == "Line Plot":
            fig = px.line(pivot_table.reset_index(), x=index_column, y=pivot_table.columns)
        elif plot_type == "Area Plot":
            fig = px.area(pivot_table.reset_index(), x=index_column, y=pivot_table.columns)

        st.plotly_chart(fig)

else:
    st.write("Please upload a data file to begin.")
