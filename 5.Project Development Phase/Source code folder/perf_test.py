import requests
import time

url = "http://127.0.0.1:5000/"  # Ensure your app is running
num_requests = 50

print(f"Starting performance test: {num_requests} requests...")
start_time = time.time()

for i in range(num_requests):
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Request {i+1} failed: {e}")

end_time = time.time()
total_time = end_time - start_time

print("-" * 30)
print(f"Total time for {num_requests} requests: {total_time:.2f} seconds")
print(f"Average time per request: {total_time/num_requests:.4f} seconds")
print(f"Requests per second: {num_requests/total_time:.2f}")