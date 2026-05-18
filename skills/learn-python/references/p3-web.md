# P3: Web / APIs Track

Full project spec: `references/projects.md` → "Web/APIs Project: weather_app"

## L1: HTTP with requests

**Concept:** The web runs on HTTP. `requests` is Python's go-to library for making HTTP calls. APIs return JSON — Python's `json` module (or `response.json()`) turns it into a dict.

**Task:** Install `requests`. Write `weather.py` that fetches current weather for a city from `wttr.in/?format=j1` and prints temperature and description.

```bash
pip install requests
python weather.py London
```

**Acceptance criteria:** Prints city, temp in °C, and a description. Handles non-200 response with a clear error.

**Common mistakes:** Forgetting to call `response.raise_for_status()`. Accessing nested JSON keys without checking they exist.

---

## L2: REST Concepts

**Concept:** REST APIs expose *resources* via URLs. HTTP methods define the action: GET (read), POST (create), PUT/PATCH (update), DELETE (remove). Status codes signal the result: 2xx success, 4xx client error, 5xx server error.

**Task:** No code this lesson. Map out the weather app's future endpoints on paper or in a comment block in `weather.py`:

```
GET  /weather/{city}            → current weather
GET  /weather/{city}/forecast   → 3-day forecast
POST /favorites                 → add favorite city
GET  /favorites                 → list favorites
DELETE /favorites/{city}        → remove favorite
```

**Acceptance criteria:** User can explain what each endpoint does and which HTTP method maps to each CRUD operation.

---

## L3: FastAPI Basics

**Concept:** FastAPI builds web APIs in Python with almost no boilerplate. Routes are plain functions decorated with `@app.get()` etc. Uvicorn is the server that runs it. Pydantic handles input/output validation automatically.

**Task:** Create `weather_app/main.py`. Add a single `GET /weather/{city}` endpoint that calls your `weather.py` fetcher and returns a JSON response.

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

**Acceptance criteria:** `GET http://localhost:8000/weather/London` returns JSON with city, temp, description. `/docs` (auto-generated) shows the endpoint.

**Common mistakes:** Forgetting `uvicorn main:app` — `python main.py` doesn't start the server. Returning a plain string instead of a dict (FastAPI serializes dicts to JSON automatically).

---

## L4: CRUD App

**Concept:** A CRUD app covers the four fundamental data operations: Create, Read, Update, Delete. An in-memory dict is fine for learning — no database needed yet.

**Task:** Add POST, GET, DELETE endpoints for `/favorites`. Store cities in a module-level dict. Test each endpoint.

```bash
# Test with curl:
curl -X POST http://localhost:8000/favorites -H "Content-Type: application/json" -d '{"city": "Tokyo"}'
curl http://localhost:8000/favorites
curl -X DELETE http://localhost:8000/favorites/Tokyo
```

**Acceptance criteria:** All three endpoints work. Duplicate city POST returns a 400 error. Deleting a city that doesn't exist returns 404.

**Common mistakes:** Using a list instead of dict for favorites — dict lookup by city name is O(1). Returning 200 for all errors instead of correct status codes.
