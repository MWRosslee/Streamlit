import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title of the app
st.title("Dynamic Data Visualization App")

# File uploader widget
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write("Dataframe:")
    st.write(df)

    # Select Plot Type
    plot_types = ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", "Pie Chart", "Two Y-Axes Plot"]
    plot_type = st.sidebar.selectbox("Select the type of plot", plot_types)

    # Plot configuration based on selected plot type
    if plot_type in ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram", "Two Y-Axes Plot"]:
        x_column = st.sidebar.selectbox("Select the X-axis column", df.columns, index=0)
        y_columns = st.sidebar.multiselect("Select one or more Y-axis columns (numeric only)",
                                           df.select_dtypes(['number']).columns,
                                           default=df.select_dtypes(['number']).columns[0] if df.select_dtypes(['number']).columns.any() else None)

        if plot_type == "Line Plot":
            fig = px.line(df, x=x_column, y=y_columns, markers=True)
        elif plot_type == "Bar Plot":
            fig = px.bar(df, x=x_column, y=y_columns)
        elif plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_columns)
        elif plot_type == "Histogram":
            fig = px.histogram(df, x=x_column, y=y_columns)
        elif plot_type == "Two Y-Axes Plot":
            if len(y_columns) == 2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df[x_column], y=df[y_columns[0]], name=y_columns[0]))
                fig.add_trace(go.Scatter(x=df[x_column], y=df[y_columns[1]], name=y_columns[1], yaxis="y2"))
                fig.update_layout(yaxis2=dict(overlaying="y", side="right"))
            else:
                st.write("Please select exactly two Y-axis columns for this plot.")

    elif plot_type == "Pie Chart":
        cat_column = st.sidebar.selectbox("Select the category column", df.select_dtypes(exclude=['number']).columns)
        num_column = st.sidebar.selectbox("Select the numeric column", df.select_dtypes(include=['number']).columns)
        fig = px.pie(df, names=cat_column, values=num_column)

    # Display the plot
    if 'fig' in locals():
        st.plotly_chart(fig)
    else:
        st.write("Please select appropriate columns for the plot.")

else:
    st.write("Please upload a CSV file.")
