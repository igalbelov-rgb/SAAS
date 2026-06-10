from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

# יצירת המנוע שמדבר עם פוסטגרס. 
# משתמשים בכתובת ה-URL שמשכנו מקובץ ה-.env.production
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True # מדפיס את שאילתות ה-SQL לטרמינל - מעולה לפיתוח ודיבאג!
)

# פונקציה ליצירת הטבלאות במידה והן לא קיימות
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency (מזרק) עבור הטרנזקציות ב-API
# בכל פעם שנרצה לדבר עם הדאטאבייס בתוך נתיב, נקרא לזה
def get_session():
    with Session(engine) as session:
        yield session