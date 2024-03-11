# sound_meter

**meter.py** measures audio levels from the default microphone in chunks, performs inference using MediaPipe, and stores results every minute in a CSV. To prevent the CSV from becoming too big, it's limited to one day.

**plots.py** reads the CSV file and draws a box graph with sound levels and a stacked bar graph with audio detected with MediaPipe, limited to 12 categories.

**http_server.py** performs the same functionality and serves files in two endpoints, one landscape for desktops and one portrait for mobile devices.

Many improvements can be made, like using JavaScript to display and filter HTTP graphs :-)

