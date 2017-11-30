One Signal API SDK for Python
=============================

This SDK helps to simplify the one signal api implementation ( https://documentation.onesignal.com/reference ).

This version (0.1) only supports:

- Send notifications

- Include and exlude segments for delivery

- Set filtes for delivery

- Set specifics player ids



Requirements
------------
You will need your APP ID and API KEY,
if you don't know how to get it visit this link: https://documentation.onesignal.com/docs/accounts-and-keys#section-keys-ids



Installation
------------
Run this command in your shell:


`pip install onesignalapi`

It depends if you are working with a virtual env (I recommend it) you should activate it first and then install the package.
Here more information about the packages installing https://packaging.python.org/tutorials/installing-packages/


Configuration
-------------
Once you install the package you should be able to import it:

```python
from onesignalapi import OneSignal
```

Then create an instance:

```python
APP_ID = "YOUR-APP-ID"
API_KEY = "YOUR-API-KEY"
os_sdk = OneSignal(APP_ID,API_KEY)
```


That's all! Now you are ready to send notifications


Sending Notifications
---------------------
You have to create a new notification first:

```python
push_notification = os_sdk.new_notification('TITLE','SUBTITLE','MESSAGE')
```

Now you can:

Include a segment or segments:

```python
push_notification.include_segments(["Active Users","Inactive Users"])
```

Exclude a segment or segments:
```python
push_notification.exclude_segments(["Active Users","Inactive Users"])
```

Set filters:

```python
push_notification.set_filters([{"field": "tag", "key": "isNewUser", "relation": "=", "value": "1"}])
```

Define player ids:

```python
push_notification.set_playersid(["THIS-IS-A-PLAYER-ID", "THIS-IS-ANOTHER-PLAYER-ID"])
```

And finally send the notification:

```python
push_notification.send()
```


Responses
---------
The package will always return a dictionary (dict) with the same structure:

```python
{"error": , "message": , "data": }
```

`"error"` (bool) It could be True or False.

`"message"` (String) If there is an error it explains the error or `"Ok"` if nothing fails.

`"data"` (list) It contains the response data or error data.

Example:

```python
if push_notification["error"]:

    return push_notification["message"]

else:

    NOTIFICATION SENT
```

TODO
----
A lot! XD