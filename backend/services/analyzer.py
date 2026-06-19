import pandas as pd
from typing import List, Dict, Any

def analyze_submissions(submissions: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not submissions:
        return {"weak_topics": [], "total_submissions": 0}
        
    df = pd.DataFrame(submissions)
    
    # Extract tags and verdicts
    records = []
    for _, row in df.iterrows():
        problem = row.get("problem", {})
        tags = problem.get("tags", [])
        verdict = row.get("verdict", "")
        
        for tag in tags:
            records.append({
                "tag": tag,
                "is_solved": 1 if verdict == "OK" else 0
            })
            
    if not records:
        return {"weak_topics": [], "total_submissions": len(submissions)}
        
    tag_df = pd.DataFrame(records)
    
    # Calculate stats per tag
    stats = tag_df.groupby("tag").agg(
        attempted=("is_solved", "count"),
        solved=("is_solved", "sum")
    ).reset_index()
    
    stats["success_rate"] = stats["solved"] / stats["attempted"]
    
    # Filter for topics with significant attempts and low success rate
    weak_topics_df = stats[(stats["attempted"] >= 3) & (stats["success_rate"] < 0.6)].sort_values("success_rate")
    
    weak_topics = []
    for _, row in weak_topics_df.iterrows():
        weak_topics.append({
            "topic": row["tag"],
            "attempted": int(row["attempted"]),
            "solved": int(row["solved"]),
            "success_rate": float(row["success_rate"])
        })
        
    return {
        "weak_topics": weak_topics[:10], # Return top 10 weakest topics
        "total_submissions": len(submissions)
    }

# New: Generate recommendations based on weak topics
from typing import Optional

def generate_recommendations(submissions: List[Dict[str, Any]], user_rating: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    After fetching user contest history, analyze weak tags (tags with low AC rate).
    Return top 5 problem tags the user should practice, sorted by weakness score.
    Schema: [{ tag: string, ac_rate: float, suggested_difficulty: int }]
    """
    if not submissions:
        return []

    # Map from tag name to a list of dicts/ratings
    tag_data = {}
    
    for sub in submissions:
        verdict = sub.get("verdict", "")
        problem = sub.get("problem", {})
        tags = problem.get("tags", [])
        rating = problem.get("rating")
        
        is_solved = 1 if verdict == "OK" else 0
        
        for tag in tags:
            if tag not in tag_data:
                tag_data[tag] = {
                    "solved": 0,
                    "attempted": 0,
                    "ratings": []
                }
            tag_data[tag]["attempted"] += 1
            if is_solved:
                tag_data[tag]["solved"] += 1
            if rating is not None:
                tag_data[tag]["ratings"].append(rating)

    stats = []
    for tag, data in tag_data.items():
        ac_rate = data["solved"] / data["attempted"]
        
        # Calculate base difficulty from ratings
        avg_rating = None
        if data["ratings"]:
            avg_rating = sum(data["ratings"]) / len(data["ratings"])
            
        stats.append({
            "tag": tag,
            "ac_rate": ac_rate,
            "attempted": data["attempted"],
            "avg_rating": avg_rating
        })

    # Sort: lowest ac_rate first, then highest attempted count to break ties
    stats.sort(key=lambda x: (x["ac_rate"], -x["attempted"]))
    
    recommendations = []
    # Take top 5
    for item in stats[:5]:
        tag = item["tag"]
        ac_rate = item["ac_rate"]
        
        # Calculate suggested difficulty
        if user_rating is not None:
            base = user_rating
        elif item["avg_rating"] is not None:
            base = item["avg_rating"]
        else:
            base = 1200
            
        # Adjust difficulty based on success rate
        if ac_rate < 0.2:
            suggested = base - 200
        elif ac_rate < 0.4:
            suggested = base - 100
        elif ac_rate < 0.6:
            suggested = base
        else:
            suggested = base + 100
            
        # Round to nearest 100
        suggested = int(round(suggested / 100.0) * 100)
        # Clamp between 800 and 3500
        suggested = max(800, min(3500, suggested))
        
        recommendations.append({
            "tag": tag,
            "ac_rate": round(ac_rate, 4),
            "suggested_difficulty": suggested,
            # Backward compatibility fields for the frontend Dashboard.jsx
            "action": f"Practice {tag} (Suggested Diff: {suggested})",
            "suggested_url": f"https://codeforces.com/problemset?tags={tag}"
        })
        
    return recommendations
