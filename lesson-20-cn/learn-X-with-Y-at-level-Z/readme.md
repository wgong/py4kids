X = [Chinese, Math, Physics, Python, ...]

Y = [AI, Anna, Bob, KhanAcademy, OpenU, ...]

Z = [Novice, Beginner, Intermediate, Advanced, Expert]
     kindgarten, primary, mid/high school, college, phd-graduate

A concept-based learning platform:
- Multi-Lingual
- Multi-Modal
- Multi-Media
- Multi-Level
- AI powered
- Human mentored/supported


asked Claude for learning resources and combine them into CSV

```
# convert each json to flat csv
ls data/*-v2.json | xargs -t -I {} python json_to_csv_converter-v2.py {}

# concat flat csv files into one
(head -n 1 "$(ls data/*-v2.csv | head -n 1)"; for f in data/*-v2.csv; do tail -n +2 "$f"; done) > stem-learning-resources-per-claude-pro.csv
```

