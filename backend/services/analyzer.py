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
def generate_recommendations(weak_topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    For each weak topic, recommend practicing more problems with that tag.
    """
    recommendations = []
    for topic in weak_topics:
        recommendations.append({
            "topic": topic["topic"],
            "action": f"Practice more problems tagged with '{topic['topic']}' on Codeforces.",
            "suggested_url": f"https://codeforces.com/problemset?tags={topic['topic']}"
        })
    return recommendations
