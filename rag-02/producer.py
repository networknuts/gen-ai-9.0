import uuid 
import redis 

# REDIS CONNECTION SETUP
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# GENERATE QUERY AND ID TO SEND TO REDIS
def push_query(query):
    job_id = str(uuid.uuid4())
    payload = {
        "job_id": job_id,
        "query": query
    }
    redis_client.rpush("rag:requests",str(payload))
    return job_id

user_query = input("Human Query: ")
job = push_query(user_query)

print("Job sent to Redis Queue")
print(job)
