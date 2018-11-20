import json
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        response = self.client.post("/api/v1/login/", {"email":"ellen@gmail.com",
                                            "password":"education",
                                            })
        self.token = json.loads(response._content).get('token')

    @task(2)
    def flights(self):
        self.client.get("/api/v1/flight/", headers={
            'Authorization': 'JWT {}'.format(self.token)
        })

    @task(1)
    def reserve(self):
        self.client.post("/api/v1/flight/1/reserve/", headers={
            'Authorization': 'JWT {}'.format(self.token)
        })

    @task(3)
    def ticket_one(self):
        self.client.get("/api/v1/ticket/2", headers={
            'Authorization': 'JWT {}'.format(self.token)
        })

    @task(4)
    def ticket_two(self):
        self.client.get("/api/v1/ticket/1", headers={
            'Authorization': 'JWT {}'.format(self.token)
        })



class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
