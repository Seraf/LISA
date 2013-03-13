> object calendar python
    import gflags
    import httplib2
    from datetime import timedelta, datetime, date
    import dateutil.parser
    from apiclient.discovery import build
    from oauth2client.file import Storage
    from oauth2client.client import OAuth2WebServerFlow
    from oauth2client.tools import run

    FLAGS = gflags.FLAGS

    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for native
    # applications
    # The client_id and client_secret are copied from the API Access tab on
    # the Google APIs Console
    FLOW = OAuth2WebServerFlow(
        client_id='779399468423.apps.googleusercontent.com',
        client_secret='YzGpGCXABzZAO4pfD_ZV4q_d',
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='JARVIS/0.1')

    # To disable the local server feature, uncomment the following line:
    FLAGS.auth_local_webserver = False

    # If the Credentials don't exist or are invalid, run through the native client
    # flow. The Storage object will ensure that if successful the good
    # Credentials will get written back to a file.
    storage = Storage('tmp/calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage)

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Build a service object for interacting with the API. Visit
    # the Google APIs Console
    # to get a developerKey for your own application.
    service = build(serviceName='calendar', version='v3', http=http,
            developerKey='AIzaSyAOdvOzmU3VkyDKj4baRYbZ3y8HM2Alc64')

    page_token = None
    event_list = []
    today = date.today()
    tomorrow = today + timedelta(days=1)
    while True:
        events = service.events().list(calendarId='fl6f2v9te1h3gmlsm2o3lqiu68@group.calendar.google.com',pageToken=page_token).execute()
        if events['items']:
            for event in events['items']:
                if event['start']['dateTime']:
                    event_date = dateutil.parser.parse(event['start']['dateTime']).date()
                    if (args[0] == "aujourd'hui" or args[0] == "today") and (today == event_date):
                        event_list.append(event['summary'])
                    if (args[0] == "demain" or args[0] == "tomorrow") and (tomorrow == event_date):
                        event_list.append(event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            return "Voici les evenements prevus : "+ ' puis '.join(event_list)
            break
< object