import webbrowser
import os

file_path = 'pages/home.html'






webbrowser.open_new_tab(f'file://{os.path.realpath(file_path)}')  # Opens HTML file in new window