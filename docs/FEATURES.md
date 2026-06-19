# Feature Documentation

## 1. Weak Topic Detection

**Algorithm:** For each problem tag, aggregate all submissions. Compute:
- Attempts and solves
- Success rate (solves / attempts)
- Average problem rating
- Relative performance score = `ac_rate × 50 + min(difficulty/rating, 2) × 25`

**Filters:** Topics with ≥3 attempts and <60% success rate are flagged as weak. Strongest/weakest ranked by relative performance score.

**UI:** Stats cards, bar chart, radar chart, heatmap, strongest/weakest topic lists.

## 2. Personalized Problem Recommendations

**Algorithm:**
1. Identify top 5 weakest tags
2. Load CF problemset (cached)
3. Exclude solved and recently attempted problems
4. Score: `tag_overlap × 150 - |rating - (user_rating - 100)| + rating/10`
5. Return top N with reason strings and difficulty progression labels

**Progression labels:** foundation, comfortable, growth, challenge (based on rating delta).

## 3. Contest Performance Analytics

**Metrics:**
- Rating timeline and per-contest changes
- Rank trends (reversed Y-axis — lower rank = better)
- Consistency score from rating change variance
- Contest frequency (avg days between contests)
- Upsolve count/rate (problems solved outside rated contest IDs)

## 4. Handle Comparison

Compare two users on rating, max rating, contests, solves, growth, consistency. Auto-generated insights highlight significant differences. Bar chart compares key metrics side-by-side.

## 5. Rating Growth Predictor

**Method:** Linear regression on contest-index vs rating. Predicts 3 contests ahead.

**Confidence:** Blend of R² fit and data volume (`min(0.95, r²×0.6 + volume×0.4)`).

**Output:** Low/mid/high range, trend label, monthly growth estimate, actionable suggestions.

No ML framework required — pure statistics, explainable in interviews.
