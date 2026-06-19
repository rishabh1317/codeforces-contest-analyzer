import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Competitive Programming Analyzer API"}
    print("Root endpoint test PASSED")

def test_analysis():
    # Tourist is a valid codeforces user
    response = client.get("/analysis/codeforces/Tourist")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Analysis response keys:", data.keys())
        print("Recommendations sample:", data["recommendations"][:2] if data["recommendations"] else [])
        assert "handle" in data
        assert "total_submissions" in data
        assert "weak_topics" in data
        assert "recommendations" in data
        if data["recommendations"]:
            rec = data["recommendations"][0]
            assert "tag" in rec
            assert "ac_rate" in rec
            assert "suggested_difficulty" in rec
            assert "action" in rec
            assert "suggested_url" in rec
        print("Analysis endpoint test PASSED")
    else:
        print(f"Analysis endpoint returned error: {response.text}")

if __name__ == "__main__":
    test_root()
    test_analysis()
