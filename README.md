# מערכת שיבוץ קבוצות (Class Assignment System)

שלד הפרויקט. ראו את קובץ ההתקנה לפרטי הקמה והרצה.

## מבנה הפרויקט

```
class-assignment-system/
├── backend/
│   ├── main.py                  # FastAPI app, כל ה-endpoints
│   ├── models.py                # Pydantic models: Person, RunConfig, Assignment
│   ├── config.py                # טעינת .env בלבד
│   ├── defaults.py              # ערכי ברירת מחדל לטופס ההגדרות
│   ├── agents/
│   │   ├── data_agent.py        # קריאת Excel → List[Person]
│   │   ├── scoring_agent.py     # חישוב ציונים + Claude לטקסט בלבד
│   │   ├── constraint_agent.py  # אימות תוצאות לאחר שיבוץ
│   │   └── assignment_agent.py  # מריץ OR-Tools, מחזיר שיבוץ
│   └── services/
│       ├── claude_service.py    # עטיפה על Anthropic SDK (טקסט בלבד)
│       ├── assignment_solver.py # לוגיקת OR-Tools CP-SAT
│       ├── excel_service.py     # קריאה וכתיבת xlsx
│       └── validation_service.py # אימות נתוני קלט
├── frontend/
│   ├── setup.html               # שלב 0: טופס הגדרות
│   ├── index.html               # שלב 1-2: העלאת Excel
│   ├── review.html              # שלב 5: אימות ציונים
│   ├── dashboard.html           # שלבים 7-8: לוח שיבוץ
│   └── static/
│       ├── styles.css
│       ├── setup.js
│       └── dashboard.js
├── templates/
│   └── input_template.xlsx      # תבנית Excel (תיווצר בהמשך)
├── output/                      # קבצי פלט (נוצר אוטומטית)
├── .env                         # מפתח API (לא ב-git)
├── .env.example
├── requirements.txt
└── README.md
```

## הרצה

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```
