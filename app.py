import streamlit as st
import pandas as pd
import dataframe_image as dfi
from datetime import date, timedelta
import os

st.set_page_config(page_title="Daily Report Maker", layout="centered")

st.title("📝 Daily Work Report")

# Date field defaulting to yesterday
yesterday = date.today() - timedelta(days=1)
report_date = st.date_input("Report Date", value=yesterday)

# Name field
name = st.text_input("Name", value="Muskan Nanva")
assigned_work = st.text_area("Assigned Work", height=100)
completed_work = st.text_area("Work Completed", height=100)

if st.button("Make Report Image"):
    if assigned_work and completed_work:
        with st.spinner("Generating image..."):
            
            # Format the date for the table
            formatted_date = report_date.strftime("%d-%m-%Y")
            
            # Construct the DataFrame with a MultiIndex to center and merge the top header
            df = pd.DataFrame({
                "Col1": ["Date", "Name", "Assigned", "Work Completed"],
                "Col2": [formatted_date, name, assigned_work, completed_work]
            })
            
            # This creates the merged "Daily work Report" header over the two columns
            df.columns = pd.MultiIndex.from_tuples([("Daily work Report", "Col1"), ("Daily work Report", "Col2")])

            def style_table(styler):
                styler.set_properties(**{
                    'text-align': 'center',
                    'border': '1px solid black',
                    'padding': '15px',
                    'font-family': 'sans-serif'
                })
                styler.set_table_styles([{
                    'selector': 'th',
                    'props': [('background-color', '#FFD966'), ('color', 'black'), ('border', '1px solid black'), ('text-align', 'center')]
                }])
                return styler

            # Hide the index on the left, and hide the sub-headers ("Col1", "Col2")
            styled_df = df.style.pipe(style_table).hide(axis="index").hide(level=1, axis="columns")

            # Save and display the image using the chrome converter
            image_path = 'daily_report.png'
            dfi.export(styled_df, image_path, max_rows=-1, table_conversion="chrome")
            
            st.success("Report generated!")
            st.image(image_path)
            
            # Add the Download Button
            with open(image_path, "rb") as file:
                st.download_button(
                    label="📥 Download Report Image",
                    data=file,
                    file_name=f"Daily_Report_{formatted_date}.png",
                    mime="image/png"
                )
                
    else:
        st.error("Please fill in both the Assigned and Completed work fields.")
