import sys
import os

# Add the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_tag_analysis():
    response = client.get("/api/users/Tourist/tag-analysis")
    print(f"Tag Analysis Status Code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    print(f"Tag Analysis results count: {len(data)}")
    if data:
        print("Sample item:", data[0])
        assert "tag" in data[0]
        assert "total" in data[0]
        assert "solved" in data[0]
        assert "ac_rate" in data[0]
        assert "avg_difficulty" in data[0]
    print("test_tag_analysis PASSED")

def test_percentile():
    response = client.get("/api/users/Tourist/percentile")
    print(f"Percentile Status Code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    print(f"Percentile contests count: {len(data)}")
    if data:
        print("Sample item:", data[0])
        assert "contest_id" in data[0]
        assert "contest_name" in data[0]
        assert "rank" in data[0]
        assert "old_rating" in data[0]
        assert "new_rating" in data[0]
        assert "total_participants" in data[0]
        assert "percentile" in data[0]
    print("test_percentile PASSED")

def test_compare():
    response = client.get("/api/compare?handle1=Tourist&handle2=Benq")
    print(f"Compare Status Code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    print("Compare keys:", data.keys())
    assert "rival1" in data
    assert "rival2" in data
    rival1 = data["rival1"]
    print(f"Rival 1 ({rival1['handle']}): Solved={rival1['problems_solved']}, Contests={rival1['total_contests']}, Strongest={rival1['strongest_tags']}")
    print("test_compare PASSED")

if __name__ == "__main__":
    test_tag_analysis()
    test_percentile()
    test_compare()
