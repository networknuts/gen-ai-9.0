import json

ai_output = '{"zipcode":"400001"}'
new_output = json.loads(ai_output) #str to dict

function_output = {"temperature": 25}
modified_output = json.dumps(function_output) #dict to str 
print(modified_output)
print(type(modified_output))