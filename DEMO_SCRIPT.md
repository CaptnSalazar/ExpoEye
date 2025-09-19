# Demo Script

1. Demo UI: `streamlit run app.py` — show upload of badge and voice file.
2. Full stack via Docker: `docker-compose up --build`
3. Use curl to POST: `curl -F "image=@demo_images/badge_sample.jpg" http://localhost:8200/submit`
4. Run `python benchmark.py` to show latency numbers.
