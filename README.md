##Control-M Workload Automation Client in Python

This project uses the Control-M Automation API restful webservice to connect to your Control-M Environment.

The graphic component of this project uses [Kivy](https://kivy.org/#home). Each screen is a .kv file under the loaders directory.


All connections the REST API are done though the api module using the requests package: [http://docs.python-requests.org/en/master/](http://docs.python-requests.org/en/master/).
###Current Issues:

- Monitoring Screen only shows the last job in the json returned by api.list_jobs

###To Do:

- Implement Color coding in Monitoring Screen based on status
- Implement Rerun/Hold/Free actions for jobs in Monitoring Screen
- Implement Planning Screen to create new jobs