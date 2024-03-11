import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from ast import literal_eval
from collections import Counter
import numpy as np
from flask import Flask, send_file

# Import Flask and create an instance of the application
app = Flask(__name__)

# Apply dark theme
plt.style.use('dark_background')

def sound_levels_graph(data, ax_boxplot):
    ax_boxplot.clear()  # Clear the axis for the new plot
    
    # Transform data if necessary, as described earlier
    data['Data'] = data['Data'].apply(literal_eval)
    data_for_boxplot = [d for d in data['Data']]
    
    # Generate a color scale for the boxplot boxes
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_for_boxplot)))
    
    # Plot the boxplot with the generated colors
    box = ax_boxplot.boxplot(data_for_boxplot, patch_artist=True)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    
    # Configure labels and title
    x_labels = [f"{hour:02d}:{minute:02d}" for hour, minute in zip(data['Hour'], data['Minute'])]
    ax_boxplot.set_xticks(ticks=range(1, len(data) + 1))
    ax_boxplot.set_xticklabels(labels=x_labels, rotation=90)  # Rotate labels by 90 degrees
    ax_boxplot.set_xlabel('Hour-Minute')
    ax_boxplot.set_ylabel('dB')  # Update y-axis label
    ax_boxplot.set_title('Sound Level')
    ax_boxplot.grid(True)

def audio_classification_graph(data, ax_bar):
    ax_bar.clear()  # Clear the axis for the new plot
    sounds = {}
    # Iterate over each row of the DataFrame
    for index, row in data.iterrows():
        # Combine all sound lists into one list
        all_sounds = [sound for sound in literal_eval(row['Sounds'])]
        
        # Count occurrences of each sound
        counter_sounds = Counter(all_sounds)
        
        # Calculate occurrence percentages of each sound
        total_occurrences = sum(counter_sounds.values())
        percentages = {sound: (count / total_occurrences) * 100 for sound, count in counter_sounds.items()}
        sounds[f"{row['Hour']:02d}:{row['Minute']:02d}"] = percentages
    
    # Collect all unique categories and calculate total percentage sums for each
    category_totals = {}
    for time, categories_data in sounds.items():
        for category, percentage in categories_data.items():
            category_totals[category] = category_totals.get(category, 0) + percentage

    # Sort categories by their total percentage sums
    sorted_categories = sorted(category_totals.keys(), key=lambda x: category_totals[x], reverse=True)[:12]  # Limit to top 12 categories

    # Create a matrix to store percentages of each category at each moment
    bars = np.zeros((len(sounds), len(sorted_categories)))

    # Fill the matrix with percentages
    for i, time in enumerate(sorted(sounds)):
        for j, category in enumerate(sorted_categories):
            if category in sounds[time]:
                bars[i, j] = sounds[time][category]

    # Create the stacked bar chart
    bottom = np.zeros(len(sounds))
    for i, category in enumerate(sorted_categories):
        ax_bar.bar(sorted(sounds), bars[:, i], bottom=bottom, label=category)
        bottom += bars[:, i]       
    
    # Configure labels and title
    ax_bar.set_xlabel('Hour-Minute')
    ax_bar.set_xticks(range(len(sounds)))  # Set tick locations
    ax_bar.set_xticklabels(sorted(sounds.keys()), rotation=90)  # Set labels and rotate them 90 degrees
    ax_bar.set_ylabel('Percentage')
    ax_bar.set_title('Sound Percentage')
    ax_bar.legend()  # Show legend
    ax_bar.grid(True)

@app.route('/horizontal-chart')
def serve_horizontal_chart():
    date_time = datetime.now()
    file_name = f"{date_time.year}-{date_time.month:02d}-{date_time.day:02d}.csv"
    if os.path.isfile(file_name):
        # Read data and take only the last 100 records
        data = pd.read_csv(file_name).iloc[-120:]
        # Initialize figure and axes
        fig, (ax_boxplot, ax_bar) = plt.subplots(nrows=2, ncols=1, figsize=(20, 12))
        sound_levels_graph(data, ax_boxplot)  # Pass the axis as an argument
        audio_classification_graph(data, ax_bar)  # Pass the axis as an argument
        plt.tight_layout()  # Adjust subplots layout
        temp_name = f"temp_{date_time.strftime('%Y%m%d%H%M%S')}.png"
        plt.savefig(temp_name)  # Save figure as image
        plt.close(fig)  # Close figure to release memory
        return send_file(temp_name, mimetype='image/png')  # Send image to client
    else:
        return "Waiting for data..."
    
@app.route('/vertical-chart')
def serve_vertical_chart():
    date_time = datetime.now()
    file_name = f"{date_time.year}-{date_time.month:02d}-{date_time.day:02d}.csv"
    if os.path.isfile(file_name):
        # Read data and take only the last 100 records
        data = pd.read_csv(file_name).iloc[-45:]
        # Initialize figure and axes
        fig, (ax_boxplot, ax_bar) = plt.subplots(nrows=2, ncols=1, figsize=(6, 10))
        sound_levels_graph(data, ax_boxplot)  # Pass the axis as an argument
        audio_classification_graph(data, ax_bar)  # Pass the axis as an argument
        plt.tight_layout()  # Adjust subplots layout
        temp_name = f"temp_{date_time.strftime('%Y%m%d%H%M%S')}.png"
        plt.savefig(temp_name)  # Save figure as image
        plt.close(fig)  # Close figure to release memory
        return send_file(temp_name, mimetype='image/png')  # Send image to client
    else:
        return "Waiting for data..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
