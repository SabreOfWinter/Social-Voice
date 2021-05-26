from locust import HttpUser, TaskSet, task


class UserActions(HttpUser):
    def on_start(self):
        self.login()

    def login(self):
        # login to the application
        response = self.client.get('/accounts/login/')
        csrftoken = response.cookies['csrftoken']
        #self.client.post('/accounts/login/',
                        #  {'username': 'ivanivan', 'password': 'ivan123A'},
                        #  headers={'X-CSRFToken': csrftoken})
        self.client.post(
        '/accounts/login/',
        {
            'username': 'ivanivan',
            'password': 'ivan123A',
            'csrfmiddlewaretoken': csrftoken
        },
        headers={
            'X-CSRFToken': csrftoken,
            'Referer': self.host + '/accounts/login/'
        })
    @task(1)
    def index(self):
        self.client.get('/')
