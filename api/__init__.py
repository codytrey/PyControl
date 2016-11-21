import json
import requests


try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except:
    from urllib3.exceptions import InsecureRequestWarning
    import urllib3

verify_certs = False


def login(args):
    baseurl = "https://" + args.host + ":8443/automation-api/"
    loginurl = baseurl + "session/login"
    body = json.loads(
        '{ "password": "' + args.password + '", "username": "' + args.username + '"}')  # create a json object to use as the body of the post to the login url
    try:
        r = requests.post(loginurl, json=body, verify=verify_certs)
    except requests.exceptions.ConnectTimeout as err:
        print("Connecting to Automation API REST Server failed with error: " + str(err))
        quit(1)
    except requests.exceptions.ConnectionError as err:
        print("Connecting to Automation API REST Server failed with error: " + str(err))
        if 'CERTIFICATE_VERIFY_FAILED' in str(err.message):
            print(
                'INFO: If using a args.Signed Certificate use the -i flag to disable cert verification or add the certificate to this systems trusted CA store')
        quit(1)
    except requests.exceptions.HTTPError as err:
        print("Connecting to Automation API REST Server failed with error: " + str(err))
        quit(1)
    except:
        print("Connecting to Automation API REST Server failed with error unknown error")
        quit(1)

    loginresponce = json.loads(r.text)
    if 'errors' in loginresponce:
        print(json.dumps(loginresponce['errors'][0]['message']))
        quit(1)

    if 'token' in loginresponce:  # If token exists in the json response set the value to the variable token
        token = json.loads(r.text)['token']
        return token
        #args.is_loggedin = True
    else:
        print("Failed to get token for unknown reason, exiting...")
        quit(2)


def logout(args):
    baseurl = "https://" + args.host + ":8443/automation-api/"
    logouturl = baseurl + 'session/logout'
    body = json.loads(
        '{ "token": "' + args.token + '", "username": "' + args.username + '"}')  # logout url needs json with the token and username

    r4 = requests.post(logouturl, data=body,
                       verify=verify_certs)
    #args.is_loggedin = False
    #args.token = None
    return


def list_jobs(args):
    baseurl = "https://" + args.host + ":8443/automation-api/"
    jobstatusurl = baseurl + 'run/jobs/status'  # url to list statuses of all the jobs in the AJF

    data = json.loads(
        '{"Authorization": "Bearer ' + args.token + '"}')  # the jobs statues call should have the token in the header as JSON

    r2 = requests.get(jobstatusurl, headers=data,
                      verify=verify_certs)  # do a get on the job status url returns json with all of the job status

    if 'statuses' in json.loads(r2.text):  # if statuses exsits in json response store the statuses to variable statuses
        statuses = json.loads(r2.text)['statuses']
        return  statuses
    else:
        print(
        'No job statuses were loaded.')  # if statuses does not exist, report it. this can happen if no jobs are in the AJF
        return json.loads('{"status": []}')  # or if you've added a filter to the job statues url that has no results