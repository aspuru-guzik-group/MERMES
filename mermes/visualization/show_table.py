import os
import webbrowser
from json2html import json2html


def show_json_table(json_list):
    """
    Show a json data as a table in browser
    :param json_list: The json data to show
    :return:
    """
    table_html = json2html.convert(json=json_list)
    # write the html to a file
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Table</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}

        th, td {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }}

        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    {table_html}
</body> 
</html>
"""
    with open("table.html", "w") as file:
        file.write(html)
    filename = 'file:///' + os.getcwd() + '/' + 'table.html'
    webbrowser.open_new_tab(filename)


if __name__ == '__main__':
    data = {
        "John": {
            "age": 30,
            "city": "New York"
        },
        "Alice": {
            "age": 25,
            "city": "Los Angeles"
        }
    }
    show_json_table(data)
