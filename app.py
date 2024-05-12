from flask import Flask, request, render_template_string, send_file
import requests
import zipfile
import csv
import os

app = Flask(__name__, template_folder='templates')

# HTML template
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>BUAD 625 Milestone 6 - Akshay Soni</title>
</head>
<body>
    <h1>BUAD 625 Milestone 6</h1>
    <h2>Akshay Soni</h2>
    <h3>Step 1: Please enter URL</h3>
    <form method="post" action="/analyze">
        <input type="text" name="url" placeholder="Enter URL" required>
        <button type="submit">Analyze</button>
    </form>
    <h3>Step 2: Result</h3>
    {% if result %}
    <form method="get" action="/download">
        <button type="submit">Download Result</button>
    </form>
    <p>{{ result }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template, result=None)

def extract_zip(zip_file_path, output_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    try:
        response = requests.get(url)
        with open('temp.zip', 'wb') as f:
            f.write(response.content)
        # Extract zip file
        extract_zip('temp.zip', 'temp')
        # Read file names and save to CSV
        files = os.listdir('temp')
        with open('result.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['File Name'])
            for file in files:
                csvwriter.writerow([file])
        result = "Analysis completed. CSV file generated."
    except Exception as e:
        result = f"Error analyzing URL: {e}"
    return render_template_string(html_template, result=result)

@app.route('/download')
def download():
    return send_file('result.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
