import requests, time, statistics, os
ORCH = os.getenv('ORCH_URL','http://localhost:8200/submit')
IMG = os.getenv('BENCH_IMG','demo_images/badge_sample.jpg')

def run(n=5):
    times=[]
    for i in range(n):
        with open(IMG,'rb') as f:
            files={'image': f}
            start=time.time()
            r=requests.post(ORCH, files=files, timeout=60)
            elapsed=time.time()-start
            times.append(elapsed)
            print(f'iter {i+1}/{n} status {r.status_code} {elapsed:.3f}s')
    print('mean',statistics.mean(times),'median',statistics.median(times))

if __name__=='__main__':
    run(5)
