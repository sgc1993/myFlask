from flask import Flask
from flask import render_template
from flask import jsonify,request
import match_enterprise
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("test.html")
@app.route('/test')
def test():
    return jsonify("test success")

@app.route('/present_alias_enterprise')
def present_alias_enterprise():
    name = request.args.get('name')
    id = match_enterprise.get_enterprise_id_by_name(name)
    if id == None:return "该企业不存在"
    aliasname_list = match_enterprise.present_all_aliasname(id)
    if len(aliasname_list) == 0:return "该企业不存在别名"
    responseStr = ""
    for aliasname in aliasname_list:
        responseStr = responseStr + aliasname + '</br>'
    return responseStr

if __name__ == '__main__':
    app.run()#ta
