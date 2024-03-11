# Sound Meter  

## Project Objectives

The primary objective of this repository is to provide tools for measuring noise levels, inferring the type of sound detected at any given moment, storing this information in a CSV format, and visualizing it through various methods, both locally and via web browsers.

### Measurement of Noise Level
The repository offers functionality to measure noise levels using the default microphone on a device. This data is captured in chunks and processed for further analysis.

### Inference of Sound Types
Utilizing advanced algorithms, the repository performs inference to determine the type of sound detected at each moment. This allows for categorization and understanding of the environmental audio.

### Data Storage in CSV
All measurements and inferred sound types are stored in a CSV (Comma-Separated Values) format. This ensures easy access to historical data for analysis and reference.

### Visualization Methods
The repository provides multiple visualization methods for analyzing the collected data. These include box graphs for sound levels, stacked bar graphs for categorized sound types, and potentially more advanced visualization techniques.

### Accessibility
The tools provided in this repository are accessible both locally and through web browsers. This enables users to monitor and analyze noise levels and sound types conveniently from various platforms and devices.

### Files
**meter.py**  
Measures audio levels from the default microphone in chunks, performs inference using MediaPipe, and stores results every minute in a CSV. To prevent the CSV from becoming too big, it's limited to one day.

**plots.py**  
Reads the CSV file and draws a box graph with sound levels and a stacked bar graph with audio detected with MediaPipe, limited to 12 categories.

**http_server.py**  
Performs the same functionality and serves files in two endpoints, one landscape for desktops and one portrait for mobile devices.

Many improvements can be made, like using JavaScript to display and filter HTTP graphs :-)

### Requirements
Flask Mediapipe Sounddevice Pandas  

### Screenshots
![Desktop View](https://github.com/arin-apin/sound_meter/blob/main/desktop.jpeg)  

![Portrait View](https://github.com/arin-apin/sound_meter/blob/main/cell.jpeg)

### Disclaimer
This project is provided as-is, without any warranty or guarantee of its suitability for any purpose. While every effort has been made to ensure the accuracy and reliability of the information and code provided, the developers assume no responsibility for errors, omissions, or damages resulting from the use of this project. Feel free to clone, fork, and experiment with this project! Happy coding!

### Author
Pablo Pastor  
For [Arin Apin](https://arinapin.ai/)

