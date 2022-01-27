from flask import Flask, render_template, request, session, redirect, url_for
import json
import time
from datetime import datetime


def open_customer_details():
    fr = open(
        r".\json\customer_details.json", 'r')
    js = json.loads(fr.read())
    fr.close()
    return js


app = Flask(__name__)
app.secret_key = "hello"
app.static_folder = 'static'


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/home1', methods=['POST', 'GET'])
def home1():
    if request.method == 'POST':
        f = open(r".\json\users.json", 'r')
        jf = json.loads(f.read())
        f.close()

        result = request.form

        session["lid"] = result["lid"]
        if result['lid'] in jf.keys() and result['pwd'] == jf[result['lid']]:
            return render_template("home.html")
        else:
            return "<html><body><h1>Invalid Login</h1><a href='/'>click to login</a></body></html>"


@app.route('/create_customer', methods=['POST', 'GET'])
def create_customer():
    return render_template("create_customer.html")


@app.route('/store_customer_details', methods=['POST', 'GET'])
def store_customer_details():
    if request.method == 'POST':
        r = request.form
        jr = open_customer_details()
        if r['cssnid'] in jr.keys():
            return '<html><body><h1>Customer Already Exists</h1><a href="http://127.0.0.1:5000/create_customer">Click to go back</a></body></html>'
        else:
            fw = open(
                r".\json\customer_details.json", 'w')
            jr[r['cssnid']] = {"customername": r['customername'], "age": r['age'], 'address1': r['address1'], 'address2': r['address2'], 'city': r['city'], 'state': r['state'],
                               'phno': r['phno'], 'status': 'Active', 'lastupdated': time.strftime("%D  %H:%M:%S"), 'account': {'accountid': "", 'amount': 0, 'accounttype': "", "statement": {}}}
            json.dump(jr, fw, indent=2)
            fw.close()
            return '<html><body><h1>Customer Created Successfully</h1><a href="http://127.0.0.1:5000/create_customer">Click to go back</a></body></html>'


@app.route('/update_customer', methods=['POST', 'GET'])
def update_customer():
    return render_template("update_customer.html")


@app.route('/store_update_customer', methods=["POST", "GET"])
def store_update_customer():
    if request.method == "POST":
        r = request.form
        jr = open_customer_details()
        if r['cssnid'] in jr.keys():
            d = jr[r['cssnid']]
            d['lastupdated'] = time.strftime("%D  %H:%M:%S")
            fw = open(
                r".\json\customer_details.json", 'w')
            for k, v in r.items():
                if len(v) != 0 and k != 'cssnid':
                    d[k] = v

            jr[r['cssnid']] = d
            json.dump(jr, fw, indent=2)
            fw.close()
            return '<html><body><h1>Customer Details Updated</h1><a href="http://127.0.0.1:5000/update_customer">Click to go back</a></body></html>'
        else:
            return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/update_customer">Click to go back</a></body></html>'


@app.route('/delete_customer', methods=['POST', 'GET'])
def delete_customer():
    return render_template("delete_customer.html")


@app.route('/store_delete_customer', methods=['POST', 'GET'])
def store_delete_customer():
    if request.method == 'POST':
        r = request.form
        jr = open_customer_details()
        if r['cssnid'] in jr.keys():
            fw = open(
                r".\json\customer_details.json", 'w')
            d = jr[r['cssnid']]
            d['status'] = "DeActive"
            d['lastupdated'] = time.strftime("%D  %H:%M:%S")
            jr[r['cssnid']] = d
            json.dump(jr, fw, indent=2)
            fw.close()
            return '<html><body><h1>Customer Deleted Succesfully</h1><a href="http://127.0.0.1:5000/delete_customer">Click to go back</a></body></html>'
        else:
            return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/delete_customer">Click to go back</a></body></html>'


@app.route('/search_customer', methods=['POST', 'GET'])
def search_customer():
    return render_template('search_customer.html')


@app.route('/customer_search_result', methods=['POST', 'GET'])
def customer_search_result():
    r = request.form
    cid = r['cssnid']
    cname = r['customername']
    jr = open_customer_details()
    if len(cid) != 0:
        if cid in jr.keys():
            return render_template('customer_search_result.html', result={cid: jr[cid]})
        else:
            return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/search_customer">Click to go back</a></body></html>'
    else:
        names = [i['customername'] for i in jr.values()]
        if cname in names:
            d = {}
            for i, j in jr.items():
                if cname == j['customername']:
                    d[i] = j
            return render_template('customer_search_result.html', result=d)
        else:
            return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/search_customer">Click to go back</a></body></html>'


@app.route('/cutomer/<cid>')
def customer(cid):
    jr = open_customer_details()
    return render_template('customer.html', result=jr[cid], custid=cid)


@app.route('/customer_status', methods=['POST', 'GET'])
def customer_status():
    jr = open_customer_details()
    return render_template('customer_status.html', result=jr)


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    return render_template('create_account.html')


@app.route('/store_account', methods=["POST", "GET"])
def store_account():
    jr = open_customer_details()
    r = request.form
    if r['cssnid'] in jr.keys():
        d = jr[r['cssnid']]
        if d["account"]["accountid"] != "":
            return '<html><body><h1>Account Exists</h1><a href="http://127.0.0.1:5000/create_account">Click to go back</a></body></html>'
        else:
            d['account']['accountid'] = r['cssnid']+time.strftime("%Y")
            d['account']['amount'] = r['amount']
            d['account']['accounttype'] = r['accounttype']
            d['account']["statement"][time.strftime("%d/%m/%Y %H:%M:%S")] = {
                "operation": "Deposited", "opamount": r['amount'], 'remainingamount': r['amount']}
            jr[r['cssnid']] = d
            fw = open(
                r".\json\customer_details.json", 'w')
            json.dump(jr, fw, indent=2)
            fw.close()
            return '<html><body><h1>Account Created Successfully</h1><a href="http://127.0.0.1:5000/create_account">Click to go back</a></body></html>'
    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/create_account">Click to go back</a></body></html>'


@app.route('/delete_account', methods=['POST', 'GET'])
def delete_account():
    return render_template('delete_account.html')


@app.route('/store_delete_account', methods=['POST', 'GET'])
def store_delete_account():
    jr = open_customer_details()
    r = request.form
    if r['cssnid'] in jr.keys():
        if jr[r['cssnid']]['account']['accountid'] == r['accountid'] and jr[r['cssnid']]['account']['accounttype'] == r['accounttype']:
            jr[r['cssnid']]['account']['accountid'] = ""
            jr[r['cssnid']]['account']['amount'] = "0"
            jr[r['cssnid']]['account']['accounttype'] = ""
            jr[r['cssnid']]['account']["statement"] = {}

            fw = open(
                r".\json\customer_details.json", 'w')
            json.dump(jr, fw, indent=2)
            fw.close()
            return '<html><body><h1>Account Deleted Succesfully</h1><a href="http://127.0.0.1:5000/delete_account">Click to go back</a></body></html>'
        else:
            return '<html><body><h1>Invalid Account Details</h1><a href="http://127.0.0.1:5000/delete_account">Click to go back</a></body></html>'

    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/delete_account">Click to go back</a></body></html>'


@app.route('/search_account', methods=["POST", "GET"])
def search_account():
    return render_template('search_account.html')


@app.route("/account_search_result", methods=["POST", "GET"])
def account_search_result():
    r = request.form
    cid = r['cssnid']
    aid = r['accountid']
    jr = open_customer_details()
    if cid in jr.keys():
        if jr[cid]['account']['accountid'] == "":
            return '<html><body><h1>Account Not Yet Created</h1><a href="http://127.0.0.1:5000/search_account">Click to go back</a></body></html>'
        elif jr[cid]['account']['accountid'] != aid:
            return '<html><body><h1>Mismatch Customer SSN_ID and Account ID </h1><a href="http://127.0.0.1:5000/search_account">Click to go back</a></body></html>'
        else:
            return render_template('account_search_result.html', result={cid: jr[cid]})
    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/search_account">Click to go back</a></body></html>'


@app.route('/account/<cid>')
def account(cid):
    jr = open_customer_details()
    d = jr[cid]['account']
    return render_template('account.html', result=d, custid=cid)


@app.route('/account_status', methods=['POST', 'GET'])
def account_status():
    jr = open_customer_details()
    return render_template('account_status.html', account=jr)


@app.route('/withdraw', methods=['POST', 'GET'])
def withdraw():
    return render_template("withdraw.html")


@app.route('/store_withdraw', methods=['POST', 'GET'])
def store_withdraw():
    r = request.form
    jr = open_customer_details()
    if r['cssnid'] in jr.keys():
        if r['accountid'] == jr[r['cssnid']]['account']['accountid']:
            w = int(r['wamount'])
            rm = int(jr[r['cssnid']]['account']['amount'])
            if rm >= w and rm-w >= 0:
                jr[r['cssnid']]['account']['amount'] = str(rm-w)
                jr[r['cssnid']]['account']['statement'][time.strftime(
                    "%d/%m/%Y %H:%M:%S")] = {"operation": "Withdraw", "opamount": str(w), 'remainingamount': str(rm-w)}
                fw = open(
                    r".\json\customer_details.json", 'w')
                json.dump(jr, fw, indent=2)
                fw.close()
                return '<html><body><h1>Withdrawn Succesfully</h1><a href="http://127.0.0.1:5000/withdraw">Click to go back</a></body></html>'
            else:
                return '<html><body><h1>No Sufficient Funds</h1><a href="http://127.0.0.1:5000/withdraw">Click to go back</a></body></html>'
        else:
            return '<html><body><h1>Invalid Account Details</h1><a href="http://127.0.0.1:5000/withdraw">Click to go back</a></body></html>'
    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/withdraw">Click to go back</a></body></html>'


@app.route('/deposit', methods=['POST', 'GET'])
def deposit():
    return render_template('deposit.html')


@app.route('/store_deposit', methods=['POST', 'GET'])
def store_deposit():
    r = request.form
    jr = open_customer_details()
    cid = r['cssnid']
    aid = r['accountid']
    dm = int(r['damount'])
    rm = int(jr[r['cssnid']]['account']['amount'])

    if cid in jr.keys():
        if aid == jr[r['cssnid']]['account']['accountid']:
            jr[r['cssnid']]['account']['amount'] = str(rm+dm)
            jr[r['cssnid']]['account']['statement'][time.strftime("%d/%m/%Y %H:%M:%S")] = {
                "operation": "Deposit", "opamount": str(dm), 'remainingamount': str(rm+dm)}
            fw = open(
                r".\json\customer_details.json", 'w')
            json.dump(jr, fw, indent=2)
            fw.close()
            return '<html><body><h1>Deposited Succesfully</h1><a href="http://127.0.0.1:5000/deposit">Click to go back</a></body></html>'
        else:
            return '<html><body><h1>Invalid Account Details</h1><a href="http://127.0.0.1:5000/deposit">Click to go back</a></body></html>'
    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/deposit">Click to go back</a></body></html>'


@app.route('/transfer', methods=['POST', 'GET'])
def transfer():
    return render_template('transfer.html')


@app.route('/store_transfer', methods=['POST', 'GET'])
def store_transfer():
    r = request.form
    jr = open_customer_details()
    fcid = r['fcssnid']
    faid = r['faccountid']
    tm = int(r['tamount'])
    rm = int(jr[fcid]['account']['amount'])
    tcid = r['tcssnid']
    taid = r['taccountid']

    if fcid in jr.keys():
        if faid == jr[fcid]['account']['accountid']:
            if rm >= tm:
                jr[fcid]['account']['amount'] = str(rm-tm)
                jr[fcid]['account']['statement'][time.strftime("%d/%m/%Y %H:%M:%S")] = {
                    "operation": "Tranfer"+tcid+taid, "opamount": str(tm), 'remainingamount': str(rm-tm)}
                fw = open(
                    r".\json\customer_details.json", 'w')
                json.dump(jr, fw, indent=2)
                fw.close()
                return '<html><body><h1>Tranfered Succesfully</h1><a href="http://127.0.0.1:5000/transfer">Click to go back</a></body></html>'
            else:
                return '<html><body><h1>No Sufficient Funds</h1><a href="http://127.0.0.1:5000/transfer">Click to go back</a></body></html>'

        else:
            return '<html><body><h1>Invalid Account Details</h1><a href="http://127.0.0.1:5000/transfer">Click to go back</a></body></html>'
    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/transfer">Click to go back</a></body></html>'


@app.route('/viewstatement', methods=['POST', 'GET'])
def viewstatement():
    return render_template('viewstatement.html')


@app.route('/statement', methods=['POST', 'GET'])
def statement():
    r = request.form
    jr = open_customer_details()
    cid = r['cssnid']
    aid = r['accountid']
    if cid in jr.keys():
        if aid == jr[cid]['account']['accountid']:
            selector = r['selector']
            if selector == "num":
                try:
                    n = int(r["numtext"])
                    li = [[i, j]
                          for i, j in jr[cid]['account']['statement'].items()]
                    if n > len(li):
                        n = len(li)
                    return render_template('statement.html', result=li[-n:], custid=cid, accid=aid)
                except:
                    return '<html><body><h1>Enter Correct Number of Transactions</h1><a href="http://127.0.0.1:5000/viewstatement">Click to go back</a></body></html>'

            else:
                fdate = datetime.strptime(r['dateftext'], '%d/%m/%Y').date()
                tdate = datetime.strptime(r['datettext'], '%d/%m/%Y').date()
                li = []
                for i, j in jr[cid]['account']['statement'].items():
                    curr_date = datetime.strptime(i[:10], '%d/%m/%Y').date()
                    if fdate <= curr_date and curr_date <= tdate:
                        li.append([i, j])
                if len(li) != 0:
                    return render_template('statement.html', result=li, custid=cid, accid=aid)
                else:
                    return '<html><body><h1>No Results </h1><a href="http://127.0.0.1:5000/viewstatement">Click to go back</a></body></html>'
        else:
            return '<html><body><h1>Invalid Account Details</h1><a href="http://127.0.0.1:5000/viewstatement">Click to go back</a></body></html>'
    else:
        return '<html><body><h1>Customer Doesnt Exists</h1><a href="http://127.0.0.1:5000/viewstatement">Click to go back</a></body></html>'


@app.route('/logout')
def logout():
    session.pop('lid', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
