import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import random

# Base URL for Chicago Open Data Portal crime API; plus adding date and location filters
base_url = "https://data.cityofchicago.org/resource/w98m-zvie.json"
date_between = "?$where=date between '2019-01-01T12:00:00' and '2022-07-16T14:00:00'"
location_filter = 'within_box(location, 41.975121, -87.791649, 41.978260, -87.763931)'

# Create the overall URL to interrogate API with our data and location filters
url = base_url + date_between + ' AND ' + location_filter

# Retrieve data from the API
response = requests.get(url)
data = response.json()

# Create a pandas DataFrame from the retrieved data
df = pd.DataFrame(data, columns=['date', 'block', 'primary_type', 'description', 'arrest', 'latitude', 'longitude'])

# Function to handle button click event
def generate_chart():
    selected_graph = graph_choice.get()
    selected_data = data_choice.get()

    # Perform data analysis and visualization based on user selections
    if selected_graph == "Bar Chart":
        if selected_data == "Top Crimes":
            generate_top_crimes_bar_chart()
        else:
            generate_bar_chart(selected_data)
    elif selected_graph == "Line Chart":
        if selected_data == "Top Crimes":
            generate_top_crimes_line_chart()
        else:
            generate_line_chart(selected_data)
    elif selected_graph == "Pie Chart":
        if selected_data == "Top Crimes":
            generate_top_crimes_pie_chart()
        else:
            generate_pie_chart(selected_data)
    elif selected_graph == "Scatter Plot":
        if selected_data == "Top Crimes":
            generate_top_crimes_scatter_plot()
        else:
            generate_scatter_plot(selected_data)
    elif selected_graph == "Histogram":
        if selected_data == "Top Crimes":
            generate_top_crimes_histogram()
        else:
            generate_histogram(selected_data)
    elif selected_graph == "Heatmap":
        if selected_data == "Top Crimes":
            generate_top_crimes_heatmap()
        else:
            generate_heatmap(selected_data)
    else:
        messagebox.showinfo("Error", "Invalid graph choice")

# Function to generate a bar chart for the top crimes
def generate_top_crimes_bar_chart():
    crime_counts = df['primary_type'].value_counts().sort_values(ascending=True)
    data = crime_counts.iloc[-10:-5]

    # Plotting the bar chart
    plt.figure(figsize=(8, 6))
    plt.barh(data.index, data.values)
    plt.xlabel("Count")
    plt.ylabel("Crime Type")
    plt.title("Top Crimes")
    plt.tight_layout()

    # Displaying the chart
    plt.show()

# Function to generate a bar chart based on the selected data
def generate_bar_chart(data):
    if data in df.columns:
        data_counts = df[data].value_counts().sort_values(ascending=True)

        # Plotting the bar chart
        plt.figure(figsize=(8, 6))
        plt.barh(data_counts.index, data_counts.values)
        plt.xlabel("Count")
        plt.ylabel(data)
        plt.title(f"{data} Count")
        plt.tight_layout()

        # Displaying the chart
        plt.show()
    else:
        messagebox.showinfo("Error", "Invalid data choice")

# Function to generate a line chart for the top crimes
def generate_top_crimes_line_chart():
    crime_counts = df['primary_type'].value_counts().sort_values(ascending=True)

    # Plotting the line chart
    plt.figure(figsize=(8, 6))
    plt.plot(crime_counts.index, crime_counts.values, marker='o')
    plt.xlabel("Crime Type")
    plt.ylabel("Count")
    plt.title("Top Crimes")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Displaying the chart
    plt.show()

# Function to generate a line chart based on the selected data
def generate_line_chart(data):
    if data in df.columns:
        data_counts = df[data].value_counts().sort_values(ascending=True)

        # Plotting the line chart
        plt.figure(figsize=(8, 6))
        plt.plot(data_counts.index, data_counts.values, marker='o')
        plt.xlabel(data)
        plt.ylabel("Count")
        plt.title(f"{data} Count")
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Displaying the chart
        plt.show()
    else:
        messagebox.showinfo("Error", "Invalid data choice")

# Function to generate a pie chart for the top crimes
def generate_top_crimes_pie_chart():
    crime_counts = df['primary_type'].value_counts().sort_values(ascending=True)
    data = crime_counts.iloc[-10:-5]

    # Plotting the pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(data.values, labels=data.index, autopct='%1.1f%%')
    plt.title("Top Crimes")

    # Displaying the chart
    plt.show()

# Function to generate a pie chart based on the selected data
def generate_pie_chart(data):
    if data in df.columns:
        data_counts = df[data].value_counts()

        # Plotting the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(data_counts.values, labels=data_counts.index, autopct='%1.1f%%')
        plt.title(f"{data} Distribution")

        # Displaying the chart
        plt.show()
    else:
        messagebox.showinfo("Error", "Invalid data choice")

# Function to generate a scatter plot for the top crimes
def generate_top_crimes_scatter_plot():
    top_crimes = df['primary_type'].value_counts().nlargest(5).index
    data = df[df['primary_type'].isin(top_crimes)]

    plt.figure(figsize=(8, 6))
    plt.scatter(data['longitude'], data['latitude'], alpha=0.5)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Scatter Plot: Top Crimes")
    plt.tight_layout()
    plt.show()

# Function to generate a scatter plot based on the selected data
def generate_scatter_plot(data):
    if data in df.columns:
        plt.figure(figsize=(8, 6))
        plt.scatter(df[data], df['primary_type'], alpha=0.5)
        plt.xlabel(data)
        plt.ylabel("Crime Type")
        plt.title(f"Scatter Plot: Crime Type vs {data}")
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Error", "Invalid data choice")

# Function to generate a histogram for the top crimes
def generate_top_crimes_histogram():
    top_crimes = df['primary_type'].value_counts().nlargest(5).index
    data = df[df['primary_type'].isin(top_crimes)]

    plt.figure(figsize=(8, 6))
    plt.hist(data['primary_type'], bins='auto', edgecolor='black')
    plt.xlabel("Crime Type")
    plt.ylabel("Count")
    plt.title("Histogram: Top Crimes")
    plt.tight_layout()
    plt.show()

# Function to generate a histogram based on the selected data
def generate_histogram(data):
    if data in df.columns:
        if df[data].dtype == bool:
            labels = ['False', 'True']
            values = df[data].value_counts()
            plt.figure(figsize=(6, 6))
            plt.bar(labels, values)
            plt.xlabel(data)
            plt.ylabel("Count")
            plt.title(f"Histogram: {data}")
            plt.tight_layout()
            plt.show()
        else:
            plt.figure(figsize=(8, 6))
            plt.hist(df[data], bins='auto', edgecolor='black')
            plt.xlabel(data)
            plt.ylabel("Count")
            plt.title(f"Histogram: {data}")
            plt.tight_layout()
            plt.show()
    else:
        if data == "Top Crimes":
            generate_top_crimes_histogram()
        else:
            messagebox.showinfo("Error", "Invalid data choice")

# Function to generate a heatmap for the top crimes
def generate_top_crimes_heatmap():
    top_crimes = df['primary_type'].value_counts().nlargest(5).index
    data = df[df['primary_type'].isin(top_crimes)]
    data_heatmap = data.pivot_table(index='primary_type', columns='latitude', aggfunc='size')

    plt.figure(figsize=(10, 8))
    sns.heatmap(data_heatmap, cmap='YlOrRd', annot=True, fmt='g')
    plt.xlabel("Latitude")
    plt.ylabel("Crime Type")
    plt.title("Heatmap: Top Crimes")
    plt.tight_layout()
    plt.show()

# Function to generate a heatmap based on the selected data
def generate_heatmap(data):
    if data in df.columns:
        if data == "Top Crimes":
            generate_top_crimes_heatmap()
        else:
            plt.figure(figsize=(10, 8))
            data_heatmap = df.pivot_table(index='primary_type', columns=data, aggfunc='size')
            sns.heatmap(data_heatmap, cmap='YlOrRd', annot=True, fmt='g')
            plt.xlabel(data)
            plt.ylabel("Crime Type")
            plt.title(f"Heatmap: Crime Type vs {data}")
            plt.tight_layout()
            plt.show()
    else:
        messagebox.showinfo("Error", "Invalid data choice")

# Function to handle exit button click event
def exit_application():
    answer = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
    if answer:
        window.destroy()

def open_charts_window():
    global graph_choice, data_choice

    # Create the main window
    window = tk.Tk()
    window.title("Crime in Chicago Data Analysis")

    # Set the window dimensions and position
    window_width = 400
    window_height = 300
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 8
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a style for the window
    window.configure(bg="white")
    label_font = ("Arial", 12)
    button_font = ("Arial", 12, "bold")

    # Welcome message
    welcome_label = tk.Label(window, text="Welcome to Crime Analysis for Chicago", font=("Arial", 14), bg="white")
    welcome_label.pack(pady=20)

    # Graph choice dropdown
    graph_label = tk.Label(window, text="Select Graph:", font=label_font, bg="white")
    graph_label.pack(pady=10)
    graph_choice = tk.StringVar()
    graph_dropdown = tk.OptionMenu(window, graph_choice, "Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram", "Heatmap")
    graph_dropdown.pack()

    # Data choice dropdown
    data_label = tk.Label(window, text="Select Data:", font=label_font, bg="white")
    data_label.pack(pady=10)
    data_choice = tk.StringVar()
    data_dropdown = tk.OptionMenu(window, data_choice, "Top Crimes", "primary_type", "description", "arrest", "latitude", "longitude")
    data_dropdown.pack()

    # Generate chart button
    generate_button = tk.Button(window, text="Generate Chart", font=button_font, command=generate_chart)
    generate_button.pack(pady=20)

    # Exit button
    exit_button = tk.Button(window, text="Exit", font=button_font, command=exit_application)
    exit_button.pack(pady=10)

    window.mainloop()

# Call the function to open the window
open_charts_window()
