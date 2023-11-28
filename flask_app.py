from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def home():
    return render_template('home.html', companyName='Company Name')

@app.route('/results', methods = ['GET'])
def company_page():
    company = request.args.get('company-select')

    df_company = pd.read_csv(f'/home/ColbyKid/capstoneProject/static/{company}_info.csv', dtype=str, index_col=[0])
    dateValue = df_company.loc[0]['Values']
    actualValue = df_company.loc[1]['Values']
    predictedValue = df_company.loc[2]['Values']
    diffValue = str("%.2f" % (float(predictedValue) - float(actualValue)))
    diffPercValue = str("%.2f" % ((float(diffValue) / float(actualValue)*100)))

    return render_template(
        'results.html',
        companyName = company,
        img_data = f'static/{company}_lstm_final',
        dateString = dateValue,
        actualString = actualValue,
        predictedString = predictedValue,
        diffString = diffValue,
        diffPercString = diffPercValue
    )

@app.route('/info')
def more_info():
    return render_template('learnMore.html')

if __name__ == '__main__':
  app.run(debug=True)