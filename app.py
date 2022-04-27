from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/bewakoof',methods=['POST','GET']) # route to show the result in a web UI
@cross_origin()
def index():
    global custComment
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = 'https://www.bewakoof.com/search/'+searchString+'?ga_q='+searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.find_all('div',{'class':'plp-product-card'})


            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Rate ,Price, Diff \n"
            fw.write(headers)
            data = []
            for bigbox in bigboxes:
                try:
                    #Product Name
                    name = bigbox.a.div.find_all('div',{'class':'productCardDetail'})[0].div.text

                except:
                    name = 'No Name'

                try:
                    #Discounted Price
                    rate = bigbox.a.div.find_all('div',{'class':'productCardDetail'})[0].find_all('div',{'class':'productPriceBox clearfix'})[0].span.b.text


                except:
                    rate = 'No Discounted Rate Available'

                try:
                    #Actual Price
                    price = bigbox.a.div.find_all('div',{'class':'productCardDetail'})[0].find_all('div',{'class':'productPriceBox clearfix'})[0].find_all('span',{'class':'actualPriceText'})[0].text

                except:
                    price = 'No Pricing Available'

                try:
                    #Price Difference between Actual and Discounted Price
                    actual = bigbox.a.div.find_all('div', {'class': 'productCardDetail'})[0].find_all('div', {
                        'class': 'productPriceBox clearfix'})[0].find_all('span', {'class': 'actualPriceText'})[0].text
                    disc = bigbox.a.div.find_all('div', {'class': 'productCardDetail'})[0].find_all('div', {
                        'class': 'productPriceBox clearfix'})[0].span.b.text
                    res = int(actual) - int(disc)

                except:
                    price = 'No Pricing Available'


                mydict = {"Product": searchString, "Name": name, "Rate": rate, "Price": price, "Diff": res}
                data.append(mydict)
            return render_template('results.html', data=data[0:(len(data)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001, debug=True)
