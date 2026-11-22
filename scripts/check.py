import random
import subprocess
import json
import os

env_example_file = os.path.abspath(__file__) + "/../../.env.example"

def increment():
    subprocess.call(["curl", "--max-time", "5", "-X", "POST", "http://localhost:8000/increment"])

def get_count():
    res = subprocess.check_output(["curl", "--max-time", "5", "http://localhost:8000/"])
    return json.loads(res)["count"]

subprocess.run(["docker", "compose", "-p", "checking_docker", "--env-file", env_example_file, "down", "-v"], check=True)

subprocess.run(["docker", "compose", "-p", "checking_docker", "--env-file", env_example_file, "up", "-d", "--build", "--wait"], check=True)


assert get_count() == 0, "Count is not equal to 0 at the start"

N = random.randint(1, 100)

for i in range(N):
    increment()

assert get_count() == N, "Error while incrementing"


subprocess.run(["docker", "compose", "-p", "checking_docker", "--env-file", env_example_file, "down"], check=True)

subprocess.run(["docker", "compose", "-p", "checking_docker", "--env-file", env_example_file, "up", "-d", "--wait"], check=True)

assert get_count() == N, "Count is not equal to one before shutting the docker down"

subprocess.run(["docker", "compose", "-p", "checking_docker", "stop", "redis"], check=True)

result = subprocess.check_output(["curl", "--max-time", "5", "-i", "http://localhost:8000/healthz"]).decode()
assert result.startswith("HTTP/1.0 200 OK"), "Health check failed"

result = subprocess.check_output(["curl", "--max-time", "5", "-i", "http://localhost:8000/readyz"]).decode()
assert result.startswith("HTTP/1.0 503 Service Unavailable"), "Ready check failed"

result = subprocess.check_output(["curl", "--max-time", "5", "-i", "-X", "POST", "http://localhost:8000/increment"]).decode()
assert result.startswith("HTTP/1.0 503 Service Unavailable"), "Increment check failed"

subprocess.run(["docker", "compose", "-p", "checking_docker", "--env-file", env_example_file, "stop"], check=True)

subprocess.run([
    "docker", "run", "--rm",
    "-v", "checking_docker_redis-data:/data:ro",
    "-v", f"{os.getcwd()}:/backup",
    "alpine",
    "tar", "czpf", f"/backup.rdb", "-C", "/data", "."
], check=True)

subprocess.run(["docker", "compose", "-p", "checking_docker", "start", "redis", "--wait"], check=True)

subprocess.run(["docker", "compose", "-p", "checking_docker", "--env-file", env_example_file, "down", "-v"], check=True)

print("All tests passed!")








