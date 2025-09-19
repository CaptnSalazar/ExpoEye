"""benchmark.py
Measure end-to-end latency of the orchestrator pipeline using demo image.
"""
import requests, time, statistics, os
ORCH = os.getenv('ORCH_URL','http://localhost:8200/submit')
IMG = 'demo_images/badge_sample.jpg'

def run_rounds(n=5):
    times = []
    for i in range(n):
        with open(IMG,'rb') as f:
            files = {'image': f}
            start = time.time()
            resp = requests.post(ORCH, files=files)
            elapsed = time.time()-start
            times.append(elapsed)
            print(f'iter {i+1}/{n} -> status {resp.status_code}, {elapsed:.3f}s')
    print('mean:', statistics.mean(times))
    print('median:', statistics.median(times))
    print('p99:', sorted(times)[int(0.99*len(times))-1 if len(times)>1 else -1])

if __name__=='__main__':
    run_rounds(5)
