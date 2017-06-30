from flask import Flask, render_template, request
app= Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def handle_data():
    print request.values
    return "hello world"

'''
@app.route('/result', methods =['GET', 'POST'])
def result():
    if request.method== 'POST':
        result= request.form['textData']
        result=result[::-1]
        return render_template("result.html", result=result)
'''
if __name__ == '__main__':
    app.debug= True
    app.run('0.0.0.0', 8080)
    app.run(debug= True)
