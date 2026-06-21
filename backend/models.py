"""מודלי Pydantic: Person, RunConfig, Assignment.

מודל הנתונים המרכזי של המערכת (ראי spec.md §4).
המערכת מיועדת לקבוצה אחידה — אין שדה gender ואין איזון לפי מגדר.
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

# סבילות לבדיקת סכום משקלים (סכום ≈ 1.0)
_WEIGHT_SUM_TOLERANCE = 0.01


class Person(BaseModel):
    """אדם בודד לשיבוץ — קלט + ציונים מחושבים + שיבוץ סופי."""

    id: int
    full_name: str
    # אין שדה gender — המערכת מיועדת לקבוצה אחידה

    # ציוני קלט מספריים
    gpa: float = Field(ge=0, le=100)                      # 0-100
    math_score: float = Field(ge=0, le=100)              # 0-100
    science_score: float = Field(ge=0, le=100)           # 0-100
    behavior_score: float = Field(ge=1, le=10)           # 1-10
    participation_score: float = Field(ge=1, le=10)      # 1-10
    teacher_social_rating: float = Field(ge=1, le=10)    # 1-10

    # שדות טקסט (מנותחים ע"י Claude)
    special_needs_notes: str = ""
    teacher_notes: str = ""
    parent_request: str = ""

    # בקשות חברתיות — PersonID מספרי, לא שם
    friend_requests: list[int] = Field(default_factory=list)      # [3, 7, 12]
    separation_requests: list[int] = Field(default_factory=list)  # [5]

    # ציונים מחושבים (ממולאים על-ידי ScoringAgent)
    academic_score: float = 0.0
    social_score: float = 0.0
    special_needs_score: float = 0.0

    # שיבוץ סופי
    assigned_group: str = ""


class ScoringWeights(BaseModel):
    """משקלי ניקוד — כל קבוצת משקלים חייבת להסתכם ל-1.0."""

    # משקלי ציון אקדמי (חייבים להסתכם ל-1.0)
    gpa: float = 0.40
    math_score: float = 0.35
    science_score: float = 0.25

    # משקלי ציון חברתי (חייבים להסתכם ל-1.0)
    behavior_score: float = 0.30
    participation_score: float = 0.40
    teacher_social_rating: float = 0.30

    @model_validator(mode="after")
    def _validate_sums(self) -> "ScoringWeights":
        academic = self.gpa + self.math_score + self.science_score
        social = self.behavior_score + self.participation_score + self.teacher_social_rating
        if abs(academic - 1.0) > _WEIGHT_SUM_TOLERANCE:
            raise ValueError(f"משקלי הציון האקדמי חייבים להסתכם ל-1.0 (התקבל {academic:.3f})")
        if abs(social - 1.0) > _WEIGHT_SUM_TOLERANCE:
            raise ValueError(f"משקלי הציון החברתי חייבים להסתכם ל-1.0 (התקבל {social:.3f})")
        return self


class BalanceTarget(BaseModel):
    """יעד איזון לקבוצה: טווח אחוזים + סף שמעליו אדם נחשב ל'קבוצה זו'."""

    min_ratio: float    # אחוז מינימום
    max_ratio: float    # אחוז מקסימום
    threshold: float    # ציון מעל X נחשב ל"קבוצה זו"

    @model_validator(mode="after")
    def _validate_range(self) -> "BalanceTarget":
        if self.min_ratio > self.max_ratio:
            raise ValueError(
                f"min_ratio ({self.min_ratio}) חייב להיות קטן או שווה ל-max_ratio ({self.max_ratio})"
            )
        return self


class HardRule(BaseModel):
    """כלל קשה (מובטח ע"י ה-solver): הפרדה או חיבור בין שני אנשים."""

    type: Literal["separate", "together"]   # "separate" | "together"
    person_id_1: int
    person_id_2: int
    reason: str = ""    # הסבר אופציונלי


class RunConfig(BaseModel):
    """כל ההגדרות של הרצת שיבוץ אחת."""

    # הגדרות קבוצות
    group_names: list[str]      # ["A", "B", "C"]
    target_size: int            # אנשים לקבוצה

    # משקלי ניקוד (מהטופס)
    scoring_weights: ScoringWeights

    # יעדי איזון (אין מגדר — קבוצה אחידה)
    high_achiever_balance: BalanceTarget    # % מצטיינים + סף אקדמי
    high_needs_balance: BalanceTarget       # % צרכי תמיכה + סף מיוחד

    # עדיפות קונפליקטים (סדר יורד = מה גובר)
    priority_order: list[str] = Field(
        default_factory=lambda: [
            "hard_rules",        # כלל קשה תמיד ראשון
            "academic_balance",
            "needs_balance",
            "friend_requests",
            "parent_requests",
        ]
    )

    # כללים קשים (נוספים דינמית מהטופס)
    hard_rules: list[HardRule] = Field(default_factory=list)
