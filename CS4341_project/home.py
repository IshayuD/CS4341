import webbrowser
import os

def main():
    file_path = '4341_project/pages/home.html'

    webbrowser.open_new_tab('file://' + os.path.realpath(file_path))  # Opens HTML file in new tab
    
if __name__ == '__main__':
    main()