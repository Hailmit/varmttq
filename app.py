from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

# Load JSON data from file
with open('data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# HTML form and results template
form_html = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Sao Kê </title>
    <style>
      table {
        width: 100%;
        border-collapse: collapse;
      }
      table, th, td {
        border: 1px solid black;
      }
      th, td {
        padding: 8px;
        text-align: left;
      }
      th {
        background-color: #f2f2f2;
      }
    </style>
  </head>
  <body>
    <h1>Check Var Sao Kê</h1>
    <p>Dữ liệu từ ngày 1/9 đến 10/9</p>
    <form method="post" action="/search">
      <label for="search">Nhập thông tin chuyển khoảng:</label><br>
      <input type="text" id="search" name="search" maxlength="20" required><br><br>
      <input type="submit" value="Search">
    </form>
    {% if results %}
      <h2>Kết Quả:</h2>
      <table>
        <thead>
          <tr>
            <th>Ngày</th>
            <th>Số Tiền</th>
            <th>Chi Tiết</th>
          </tr>
        </thead>
        <tbody>
          {% for item in results %}
            <tr>
              <td>{{ item['\ufeffdate'] }}</td>
              <td>{{ item[' credit '] }}</td>
              <td>{{ item['detail'] }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% elif no_result %}
      <h2>Không tìm thấy thông tin</h2>
    {% endif %}
  </body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(form_html)

@app.route('/search', methods=['POST'])
def search():
    search_string = request.form['search']
    matching_items = [item for item in json_data if search_string in item['detail']]
    
    if matching_items:
        return render_template_string(form_html, results=matching_items)
    else:
        return render_template_string(form_html, no_result=True)

if __name__ == '__main__':
    app.run(debug=True)
