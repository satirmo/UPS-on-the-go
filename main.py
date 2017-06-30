from flask import Flask, render_template, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from imageProcessing import *

app= Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def handle_data():
    imgs= [base64ToMat(request.form['ImageSide'], 0), base64ToMat(request.form['ImageTop'], 0)]
    size=  findSmallestBox(imgs)
    print size
    
    db_connect = create_engine('sqlite:///RATES.db')
    conn = db_connect.connect()
    dest= request.form['z2']
    origin=request.form['z1']

    print "origin: "+ origin + " dest: "+ dest
    query = conn.execute("SELECT * FROM PRICETABLE WHERE ZONENUMBER IN (SELECT ZONENUMBER FROM ZONETABLE WHERE DESTINATION ="+ dest +" AND ORIGIN ="+ origin+" ) AND PACKAGETYPE = '"+size+"'")
    result= query.cursor.fetchall()
    result= result[0]
    actual=""
    for i in result[0:len(result)-1]:
        actual=actual+ str(i)+" "
    return actual


if __name__ == '__main__':
    app.debug= True
    app.run('0.0.0.0', 8080)
    app.run(debug= True)
