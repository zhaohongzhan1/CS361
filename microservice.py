from flask import Flask
import random
import join

app = Flask(__name__)

@app.route('/randomnum')
def num():
    num = [1,2,3,4,5,6,7,8,9]
     
    getnum = random.sample(num, 8)
    result = ''.join(map(str,getnum))
    
    return result

@app.route('/randomword')
def word(): 
    list = []
    for i in range(65,90):
        list.append(chr(i))
    for i in range(97,122):
        list.append(chr(i))
    
    getword = random.sample(list, 8)
    result = ''.join(getword)

    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="7710", debug=True)
