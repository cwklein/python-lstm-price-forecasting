from flask import Flask, render_template, request

app = Flask(__name__, template_folder = "templates")


@app.route("/")
def home():
    return render_template('home.html', companyName="Company Name")

@app.route("/results", methods = ["POST"])
def company_page():
    company = request.form.get("company-select")
    return render_template('home.html', companyName=company)

@app.route("/info")
def more_info():
    return render_template('home.html', companyName="More INFO")

if __name__ == '__main__':
  app.run()