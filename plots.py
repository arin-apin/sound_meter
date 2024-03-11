import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time
from ast import literal_eval
from collections import Counter
import numpy as np

# Apply dark theme
plt.style.use('dark_background')

def sound_levels_graph(data, ax_boxplot):
    ax_boxplot.clear()  # Clear the axis for the new plot
    
    # Transform the data if necessary, as described earlier
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
    sounds={}
    # Iterate over each row of the DataFrame
    for index, row in data.iterrows():
        # Combine all sound lists into one list
        all_sounds = [sound for sound in literal_eval(row['Sounds'])]
        
        # Count the occurrences of each sound
        counter_sounds = Counter(all_sounds)
        
        # Calculate the percentage occurrence of each sound
        total_occurrences = sum(counter_sounds.values())
        percentages = {sound: (count / total_occurrences) * 100 for sound, count in counter_sounds.items()}
        sounds[f"{row['Hour']:02d}:{row['Minute']:02d}"] = percentages
    
    # Collect all unique categories
    data=sounds

    # Collect all unique categories and calculate the total percentage sum for each one
    category_totals = {}
    for time, categories_data in data.items():
        for category, percentage in categories_data.items():
            category_totals[category] = category_totals.get(category, 0) + percentage

    # Sort categories by their total percentage sum
    sorted_categories = sorted(category_totals.keys(), key=lambda x: category_totals[x], reverse=True)[:12]  # Limit to the top 12 categories

    # Create a matrix to store the percentages of each category at each moment
    bars = np.zeros((len(data), len(sorted_categories)))

    # Fill the matrix with percentages
    for i, time in enumerate(sorted(data)):
        for j, category in enumerate(sorted_categories):
            if category in data[time]:
                bars[i, j] = data[time][category]

    # Create the stacked bar chart
    bottom = np.zeros(len(data))
    for i, category in enumerate(sorted_categories):
        ax_bar.bar(sorted(data), bars[:, i], bottom=bottom, label=category)
        bottom += bars[:, i]       
    
    # Configure labels and title
    ax_bar.set_xlabel('Hour-Minute')
    ax_bar.set_xticks(range(len(data)))  # Set tick locations
    ax_bar.set_xticklabels(sorted(data.keys()), rotation=90)  # Set labels and rotate them by 90 degrees
    ax_bar.set_ylabel('Percentage')
    ax_bar.set_title('Detected Sound Percentage')
    ax_bar.legend()  # Show legend
    ax_bar.grid(True)

current_datetime = datetime.now()
     
# Initialize the figure and axes outside the loop
fig, (ax_boxplot, ax_bar) = plt.subplots(nrows=2, ncols=1, figsize=(20, 12))

while True:
    filename = f"{current_datetime.year}-{current_datetime.month:02d}-{current_datetime.day:02d}.csv"
    if os.path.isfile(filename):
        # Read the data and take only the last 100 records
        data = pd.read_csv(filename).iloc[-120:]
        sound_levels_graph(data, ax_boxplot)  # Pass the axis as an argument
        audio_classification_graph(data, ax_bar)  # Pass the axis as an argument
        plt.tight_layout()  # Adjust subplots layout
        plt.draw()
        plt.pause(0.5)  # Brief pause to update the UI
    else:
        print("Waiting for data...")
    time.sleep(10)  # Wait before the next update
