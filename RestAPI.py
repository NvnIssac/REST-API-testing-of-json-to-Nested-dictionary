from flask import Flask,request,jsonify
from flask_restful import Api,reqparse,Resource
from collections import OrderedDict
import json

#Reordering of the Dictionary based on Nesting Order provided
def reorder(jsn_lst,nest_indexlst):
    reordered_dic=OrderedDict()
    nest_leaf=[key for key,value in jsn_lst.items() if key not in nest_indexlst]
    nest_indexlst.extend(nest_leaf)
    for index,key in enumerate(nest_indexlst):
        reordered_dic[key]=jsn_lst[key]
    return reordered_dic

#Recursive Function to Create Nested Dictionary
def dict_factory(lst):
    if len(lst) == 2:
        return {lst[0][1]: [{lst[1][0]:lst[1][1]}]}
    else:
        return {lst[0][1]: dict_factory(lst[1:])}

#Function to traverse the dictionary and create nested dictionary
def nest_creation(dict,nest):
    nested_dicts={}
    for item in dict:
        reordered_json = (reorder(item, nest))
        json_values = list(reordered_json.items())
        nested_dict = dict_factory(json_values)
        nested_dicts.update(nested_dict)
    return nested_dicts

#Implement FLask API to test POST
app=Flask(__name__)
@app.route('/signup.html')
def signup():
    return render_template('signup.html')

api=Api(app)

#Class Rest_Data for performing post operation
class Rest_Data(Resource):

    @app.route('/')
    def index():
        headers = request.headers
        auth = headers.get("Secret-Key")
        if auth == 'Revolut':
            return jsonify({"message": "OK: Authorized"}), 200
        else:
            return jsonify({"message": "ERROR: Unauthorized"}), 401


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nest_order1")
        parser.add_argument("nest_order2")
        parser.add_argument("nest_order3")
        args=parser.parse_args()
        print("Enter json to be tested on Rest")
        Input_Data = '[{    "country": "US",    "city": "Boston",    "currency": "USD",    "amount": 100  }, {"country": "US",    "city": "NewYork",    "currency": "USD",    "amount": 200  }, {    "country": "FR",    "city": "Paris",    "currency": "EUR","amount": 20  }]'
        try:
            Input_Data = json.loads(Input_Data)
            output = nest_creation(Input_Data, list(args.values()))
        except (NameError, IOError, TypeError, SyntaxError):
            return jsonify({"Error: Parsing of Json has failed"}),400
        except (KeyError):
            return jsonify({"Error: Parsing of Json has failed"}),500
        return output,201

#Executes from REST API (Currently Tested on Postman GUI)
api.add_resource(Rest_Data,'/Rev')
app.run(debug=True)