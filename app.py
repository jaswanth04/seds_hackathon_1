

# col_names = ["status", "duration", "credit_history", "purpose", "credit_amount",
#             "savings_account", "employed_since", "installment_rate", "maritial_status_sex",
#             "other_debtors", "resident_since", "property", "age", "other_installments",
#             "housing", "existing_credits", "job", "no_of_dependents", "telephone", "foreign_worker", "credit"]

# ['status', 'credit_history', 'purpose', 'savings_account',
#        'employed_since', 'maritial_status_sex', 'other_debtors', 'property',
#        'other_installments', 'housing', 'job', 'telephone', 'foreign_worker'],


from flask import Flask, jsonify, request, session, redirect, url_for, g, Response
from flask.templating import render_template
from ml_utils import predict_credit, retrain, explain_model
import sys
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


print('Hello World')


app = Flask(__name__)
app.secret_key = 'jumpjacks'

query = {}

@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html', message = "Click on the links to go the respective pages")


@app.route('/about', methods = ["GET"])
def about():
    return render_template('about.html')

    
@app.route('/predict', methods =['GET', 'POST'])
def predict():
    if request.method == 'GET':
        message = "Let us predict"
        return render_template('predict.html', message = message)
    else:
        col_names = ["status", "duration", "credit_history", "purpose", "credit_amount",
            "savings_account", "employed_since", "installment_rate", "maritial_status_sex",
            "other_debtors", "resident_since", "property", "age", "other_installments",
            "housing", "existing_credits", "job", "no_of_dependents", "telephone", "foreign_worker"]
        query_dict = {}
        for name in col_names:
            if name == "duration":
                query_dict[name] = int(request.form[name])
            elif name == "credit_amount":
                query_dict[name] = int(request.form[name])
            elif name == "installment_rate":
                query_dict[name] = int(request.form[name])
            elif name == "resident_since":
                query_dict[name] = int(request.form[name])
            elif name == "age":
                query_dict[name] = int(request.form[name])
            elif name == "existing_credits":
                query_dict[name] = int(request.form[name])
            elif name == "no_of_dependents":
                query_dict[name] = int(request.form[name])
            else:
                query_dict[name] = request.form[name]

        print(query_dict)
        
        global query 
        query = query_dict

        prediction = predict_credit(query_dict)
        message = f'This customer is {prediction} to give loan'

        feedback_template = """
            <p> Please provide feedback about the above prediction </p>
            <form action="/feedback" method="post">
                <input type="radio" name="feedback" value="good"> Good Loan
                <input type="radio" name="feedback" value="bad"> Bad Loan
                <input type = "submit" value="Submit">
            </form>

        """

        return render_template('predict.html', message=message, feedback=feedback_template)


@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_value = request.form["feedback"]
    print(f'query: {query}')
    retrain_message = retrain(query, feedback_value)

    return render_template('index.html', message=f'Thanks for providing the feedback: {feedback_value}; {retrain_message}')

@app.route('/plot.png')
def plot_png():
    fig = explain_model()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')    

@app.route('/explain')
def explain():
    return render_template("explain.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)