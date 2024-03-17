import os
import webbrowser
from json2html import json2html

def show_json_table(json_data):
    """
    Show a json data as a table in browser
    :param json_data: The json data to show
    :return:
    """
    html = json2html.convert(json=json_data)
    # write the html to a file

    with open("table.html", "w") as file:
        file.write(html)
    filename = 'file:///' + os.getcwd() + '/' + 'table.html'
    webbrowser.open_new_tab(filename)

if __name__ == '__main__':
    data = [
        {
            "name": "John",
            "age": 30,
            "city": "New York"
        },
        {
            "name": "Alice",
            "age": 25,
            "city": "Los Angeles"
        }
    ]
    show_json_table(data)