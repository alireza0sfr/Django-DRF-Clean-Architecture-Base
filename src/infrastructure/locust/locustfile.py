from locust import HttpUser, task

class QuickStartUser(HttpUser):

    def on_start(self):
        pass

    @task
    def sample_task(self):
        pass