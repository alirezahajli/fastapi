from locust import TaskSet, constant, task, HttpUser, SequentialTaskSet


class GetQueries(TaskSet):
    @task
    def get_status(self):
        self.client.get("/search_queries/")
        print("Get Status of queries")
        self.interrupt(reschedule=False)


# class GetUrls(TaskSet):
#     @task
#     def get_500_status(self):
#         self.client.get("/urls/")
#         print("Get Status of urls")
#         self.interrupt(reschedule=False)


class Home(TaskSet):
    @task
    def get_home_status(self):
        self.client.get("/")
        print("Get Status of /")
        self.interrupt(reschedule=False)


# class MySeqTask(TaskSet):
#    @task
#    def post_query(self):
#        res = self.client.post("/search_queries/", json={"query": "foo"})
#        self.client.delete("/delete_queries/foo")
#        print(res)
#        print("Post Status of query", ":            ", res.text)
#       self.interrupt(reschedule=False)

# @task(1)
# class MustDelete(TaskSet):
#     wait_time = constant(1)

#     @task
#     def delete_query(self):
#         delete = self.client.delete("/delete_queries/foo")
#         print("Status of delete", ":                  ", delete)
#         if (
#             delete.text == '{"deleted":true}'
#             or delete.text == '{"detail":"Query not found"}'
#         ):
#             self.interrupt(reschedule=False)


class MyLoadTest(HttpUser):
    host = "http://web:8000"
    # tasks = [MySeqTask]
    tasks = [GetQueries, Home]
    #wait_time = constant(0.5)
    
    
    
