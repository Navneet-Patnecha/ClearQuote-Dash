import streamlit as st
import pandas as pd
import plotly.express as px

from QueryLLM import query

# Set the page configuration to wide layout
st.set_page_config(page_title="ClearQuoteQuery", page_icon=":bar_chart:", layout="wide")

# Function to display the Dashboard page
def display_dashboard():
    st.title("Dashboard")
    st.subheader("Explore your CSV data with interactive visualizations")

    # Read the CSV file from the specified location
    file_path = "ClearQuote.csv"  # Replace with the actual file path
    df = pd.read_csv(file_path)

    # Display the data as a table
    st.subheader("Data Overview")
    st.write(df)

    # Plotting section
    st.subheader("Data Visualization")

    col1, col2, col3 = st.columns(3)

    # Question 1: How many vehicles were inspected by date?
    st.subheader("Vehicles Inspected by Date")
    vehicle_count_by_date = df.groupby('Inspection date')['Vehicle ID'].nunique().reset_index()
    fig1 = px.bar(vehicle_count_by_date, x='Inspection date', y='Vehicle ID')
    st.plotly_chart(fig1, use_container_width=True)

    # Create columns for the pie charts
    col1, col2 = st.columns(2)

    # Question 2: Which parts were most frequently detected?
    with col1:
        st.subheader("Most Frequently Detected Parts")
        part_counts = df['Part detected'].value_counts().reset_index()
        part_counts.columns = ['Part', 'Count']
        frequent_part_detected = part_counts.nlargest(6, 'Count')
        fig2 = px.bar(frequent_part_detected, x='Part', y='Count' , color='Part')
        st.plotly_chart(fig2, use_container_width=True)

    # Question 3: Which parts are least detected?
    with col2:
        st.subheader("Least Frequently Detected Parts")
        least_detected_parts = part_counts.nsmallest(5, 'Count')
        fig3 = px.pie(least_detected_parts, values='Count', names='Part')
        st.plotly_chart(fig3)

    # Question 4: Which vehicles have been inspected thoroughly (max number of parts detected) and which ones have poor coverage?
    # Assuming df is already defined and loaded with the relevant data
    # Group by Vehicle ID and Part detected, then count occurrences
    vehicle_part_counts = df.groupby(['Vehicle ID', 'Part detected']).size().reset_index(name='Count')

    # Sum the counts to get the total number of parts detected per vehicle
    vehicle_total_parts = vehicle_part_counts.groupby('Vehicle ID')['Count'].sum().reset_index()

    # Sort the vehicles by the total parts detected in descending order
    vehicle_total_parts = vehicle_total_parts.sort_values('Count', ascending=False)

    # Set up Streamlit layout: two columns for the table and the chart, with the chart column wider
    col1, col2 = st.columns([1, 3])  # Give more space to the second column

    # Display the sorted data in the first column
    with col1:
        st.subheader("Vehicles with Thorough Inspection (Descending Order)")
        st.write(vehicle_total_parts)

    # Plotting the data using Plotly with color grading in the second column
    with col2:
        fig = px.bar(vehicle_total_parts, x='Vehicle ID', y='Count', 
                     labels={'Vehicle ID': 'Vehicle ID', 'Count': 'Number of Parts Detected'},
                     title='Number of Parts Detected per Vehicle',
                     color='Count',  # Color by the count value
                     color_continuous_scale='Viridis',  # Use a color scale
                     width=1000, height=600)  # Set the size of the plot

        # Update the layout for better readability and make it scrollable
        fig.update_layout(xaxis_title='Vehicle ID', yaxis_title='Number of Parts Detected', 
                          xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'})

        # Display the plot in the second column
        st.plotly_chart(fig, use_container_width=True)
    
    # Question 5: Assume - if a part is detected at least 3 times in an inspection, then it has good coverage. So which parts have poor coverage? And which parts have good coverage?
    st.subheader("Part Inspection Coverage")
    part_inspection_counts = df.groupby(['Vehicle ID', 'Part detected'])['Inspection ID'].nunique().reset_index()
    part_inspection_counts.columns = ['Vehicle ID', 'Part', 'Inspection Count']
    poor_coverage_parts = part_inspection_counts[part_inspection_counts['Inspection Count'] < 3]

    st.write("Vehicles with Poor Coverage Parts:")
    st.write(poor_coverage_parts[['Vehicle ID', 'Part']])

    selected_vehicle = st.selectbox("Select a Vehicle ID", df['Vehicle ID'].unique())

    vehicle_parts = part_inspection_counts[part_inspection_counts['Vehicle ID'] == selected_vehicle]
    vehicle_parts['Coverage'] = vehicle_parts['Inspection Count'].apply(lambda x: 'Good Coverage' if x >= 3 else 'Poor Coverage')

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Part Inspection Details for Vehicle: {selected_vehicle}")
        st.write(vehicle_parts[['Part', 'Inspection Count', 'Coverage']])

    with col2:
        part_distribution = vehicle_parts.groupby('Part')['Inspection Count'].sum().reset_index()
        fig = px.bar(part_distribution, x='Part', y='Inspection Count', color='Inspection Count', color_continuous_scale='Viridis')
        st.subheader("Part Detected Distribution")
        st.plotly_chart(fig)



    #Q6

    part_inspection_counts = df.groupby(['Vehicle ID', 'Part detected'])['Inspection ID'].nunique().reset_index()
    part_inspection_counts.columns = ['Vehicle ID', 'Part', 'Inspection Count']

    # Dropdown for selecting a vehicle
    selected_vehicle = st.selectbox("Select a Vehicle ID", df['Vehicle ID'].unique(), key='vehicle_select')

    # Filter parts for the selected vehicle and determine coverage
    vehicle_parts = part_inspection_counts[part_inspection_counts['Vehicle ID'] == selected_vehicle]
    vehicle_parts['Coverage'] = vehicle_parts['Inspection Count'].apply(lambda x: 'Good Coverage' if x >= 3 else 'Poor Coverage')

    # Create a pivot table for the heatmap
    heatmap_data = vehicle_parts.pivot(index='Vehicle ID', columns='Part', values='Inspection Count').fillna(0)

    # Generate the heatmap
    heatmap_fig = px.imshow(heatmap_data, 
                            labels=dict(x="Part", y="Vehicle ID", color="Inspection Count"),
                            x=heatmap_data.columns,
                            y=heatmap_data.index,
                            color_continuous_scale='Viridis')

    # Display the heatmap
    st.subheader(f"Inspection Coverage Heatmap for Vehicle: {selected_vehicle}")
    st.plotly_chart(heatmap_fig, use_container_width=True)




    st.markdown("---")

    # Display the message with a bold header and a colorful background
    st.markdown(
        """
        <div style='background-color: #f63366; padding: 20px;'>
            <h2 style='color: white; text-align: center;'>Now that you've scrolled so far...</h2>
            <p style='color: white; text-align: center; font-size: 18px;'>
                When can we schedule an interview? I'm eager to join your organization!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

        