from locust import HttpUser, task, constant_throughput

class DescuentoUser(HttpUser):
    wait_time = constant_throughput(1)

    @task
    def comprar(self):
        self.client.post("/comprar-ticket")

# from locust import HttpUser, task, between

# class Navegador(HttpUser):
#     wait_time = between(1, 2)

#     @task(4)
#     def index(self):
#         self.client.get("/navegador")

# class Comprador(HttpUser):
#     wait_time = between(1, 2)

#     @task(3)
#     def comprar(self):
#         self.client.post("/comprar")

# class Cliente( HttpUser):

#     @task(1)
#     def revisar_version (self):
#         self.client.get("/version")