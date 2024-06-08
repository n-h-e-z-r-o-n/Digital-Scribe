import json, datetime
now_date = datetime.datetime.now()
with open('./Data_Raw/CUR_user.json', 'r') as openfile:  # Reading from json file
    cur_detail = json.load(openfile)
print(cur_detail)

cridentials_age = cur_detail["_CERT_DT_"]

cridentials_age = cridentials_age.split(',')
cur_date = now_date.strftime("%Y,%m,%d")
cur_date = cur_date.split(',')

y = int(cur_date[0]) - int(cridentials_age[0])
m = int(cur_date[1]) - int(cridentials_age[1])
d = iint(cur_date[2]) - int(cridentials_age[2])
print("y", y)
print("y", m)
print("y", d)

if y == 0:
    m = m * 30
    aged = m + d
    if aged < 30:
        print("aged: ", aged)
        User_Email = cur_detail['_E_token_']
        User_Pass = cur_detail['_P_token_']
