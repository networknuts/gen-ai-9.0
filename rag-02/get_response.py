import redis
import time 

# SETUP THE REDIS CONNECTION
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

job_id = input("Enter your Job ID: ")

while True:
    result = redis_client.get(f"rag:response:{job_id}")
    if result:
        print("AI OUTPUT\n")
        print(result)
        break
    else:
        print("Waiting for 5 seconds and trying again.")
        time.sleep(5)