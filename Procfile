web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
worker: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0