
def get_token():
    authorization = "auth_token " + USER_LOGIN_TOKEN
    headers = {"content-type": "application/json",
               "accept": "application/json, text/plain, */*",
               "authorization": authorization}
    return headers

    headers = {'content-type': "application/json",
               'authorization': "auth_token" + " " + access_token,
               }