import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Configuration 
st.set_page_config(page_title="Data Sweeper", page_icon=":shark:", layout="wide")

# Improved Custom CSS for Background and Button Styling
st.markdown(
    """
    <style>
    /* Background Color */
    .main {
        background-color: #f4f6f9;
    }
    /* Header and Text Color */
    h1, h2, h3, h4, h5, h6 {
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    /* Button Styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        font-size: 14px;
        margin: 4px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Configuration
st.title("🧹 Data Sweeper")
st.markdown("""
Transform files between **CSV** and **Excel** formats with built-in data cleaning and visualization!
""")

# File Uploader
uploaded_files = st.file_uploader("📁 Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

# Process Files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File Info and Preview
        st.markdown(f"### 📊 File: {file.name}")
        st.markdown(f"**File Size:** {file.size/1024:.2f} KB")
        st.subheader("🔍 Preview Data:")
        st.dataframe(df.head(), use_container_width=True)

        # Data Cleaning Options
        st.subheader("🧼 Data Cleaning:")
        with st.expander(f"🔧 Cleaning Options for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates", key=f"dup_{file.name}"):
                    df = df.drop_duplicates()
                    st.success("✅ Duplicate Rows Removed")
            with col2:
                if st.button(f"Fill Missing Values", key=f"fill_{file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled")

        # Choose Columns to Keep or Convert
        st.subheader("📂 Column Selection:")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization:")
        if st.checkbox(f"Show Summary Statistics for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        # Conversion Options
        st.subheader("🔄 Conversion Options:")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert and Download", key=f"convert_{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download the converted file
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            # Show success message after download
            st.success(f"🎉 {file.name} has been converted and downloaded successfully!")
