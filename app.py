import streamlit as st
import pandas as pd
import dataframe_image as dfi
from datetime import date, timedelta
import urllib.parse
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
                    'padding': '20px',         # Increased padding for higher quality
                    'font-size': '18px',       # Increased font size for crispness
                    'font-family': 'sans-serif'
                })
                styler.set_table_styles([{
                    'selector': 'th',
                    'props': [
                        ('background-color', '#FFD966'), 
                        ('color', 'black'), 
                        ('border', '1px solid black'), 
                        ('text-align', 'center'),
                        ('font-size', '20px')  # Larger header font
                    ]
                }])
                return styler

            # Hide the index on the left, and hide the sub-headers ("Col1", "Col2")
            styled_df = df.style.pipe(style_table).hide(axis="index").hide(level=1, axis="columns")

            # Save and display the image using the chrome converter
            image_path = 'daily_report.png'
            dfi.export(styled_df, image_path, max_rows=-1, table_conversion="chrome")
            
            st.success("Report generated!")
            st.image(image_path)
            
            # --- ACTION BUTTONS ---
            col1, col2 = st.columns(2)
            
            # 1. Download Button
            with col1:
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Image",
                        data=file,
                        file_name=f"Daily_Report_{formatted_date}.png",
                        mime="image/png",
                        use_container_width=True
                    )
            
            # 2. WhatsApp Button
            with col2:
                whatsapp_text = urllib.parse.quote("Good morning sir")
                # Using the universal wa.me link which works on both mobile and desktop
                whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
                
                # Create a custom green button using HTML
                st.markdown(f"""
                    <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #25D366; color: white; padding: 8px 15px; text-align: center; border-radius: 8px; font-weight: bold; border: 1px solid #1ebe5d;">
                            💬 Open WhatsApp
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            
            st.caption("ℹ️ *Note: Browsers block automatic file attachments. Tap 'Download Image' (or long-press the image to copy it), then click 'Open WhatsApp' and paste the image into the chat.*")
                
    else:
        st.error("Please fill in both the Assigned and Completed work fields.")
