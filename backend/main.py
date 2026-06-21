"""FastAPI app — כל ה-endpoints.

TODO: להגדיר את אפליקציית FastAPI, הגשת ה-frontend וה-endpoints
(העלאת Excel, הרצת שיבוץ, אימות, ייצוא).

כרגע: stub מינימלי לאימות שהסביבה עובדת.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}
