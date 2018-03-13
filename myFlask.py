from flask import Flask
from flask import render_template
from flask import jsonify,request
import alias_enterprise
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("test.html")
@app.route('/test')
def test():
    return render_template("testhtml.html")

@app.route('/present_alias_enterprise_by_name')
def present_alias_enterprise():
    name = request.args.get('name')
    id = alias_enterprise.get_enterprise_id_by_name(name)
    if id == None:return "该企业不存在"
    aliasname_list = alias_enterprise.present_all_aliasname(id)
    if len(aliasname_list) == 0:return "该企业不存在别名"
    responseStr = ""
    for aliasname in aliasname_list:
        responseStr = responseStr + aliasname + '</br>'
    return responseStr

@app.route('/match_enterprise')
def machine_match_enterprise():
    alias_enterprise.machine_match_enterprise()
    return "match successfully"

@app.route('/insert_into_manmade')
def insert_into_manmade():
    names = request.args.get('names')
    print(names)
    alias_enterprise.insert_into_manmade_table(names)
    return "success"

if __name__ == '__main__':
    app.run()#ta
