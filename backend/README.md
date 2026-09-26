# Trinity Core backend
1. `python -m venv .venv`
2. Activate it and `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your API keys/model IDs.
4. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Test: GET `http://localhost:8000/health`

Never commit `.env` or put provider keys in the Android app.
