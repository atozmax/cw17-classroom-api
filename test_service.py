from fastapi.testclient import TestClient

from main import app
client = TestClient(app)

def main():
    health = client.get("/healthz")
    ready = client.get("/readyz")
    ok = client.post(
        "/predict",
        json={
            "text": "This service is fast and helpful.", "language": "en"
        }
    )

    test = client.get('/test')

    invalid = client.post("/predict", json={})
    down = client.post("/predict", json={"text": "please use [MODEL_DOWN] now"})
    assert health.status_code == 200
    assert ready.status_code == 200
    assert ok.status_code == 200
    assert ok.json()["label"] == "positive"
    assert "language" not in ok.json()
    assert invalid.status_code == 422
    assert down.status_code == 503
    assert "simulated local model outage" not in down.text
    assert health.headers["X-Service-Version"] == "0.1.0"
    assert test.status_code == 200
    assert test.json()["status"] == "ok"
    assert test.json()["message"] == "Hello, World!"
    print("all checks passed")

if __name__ == "__main__":
    main()
