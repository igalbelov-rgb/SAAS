import bcrypt

def hash_password(password: str) -> str:
    """
    מצפין סיסמה גולמית באמצעות bcrypt ומחזיר מחרוזת (str) מוצפנת
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    בודק האם הסיסמה הגולמית תואמת לסיסמה המוצפנת בבסיס הנתונים
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False
    
import jwt
from datetime import datetime, timedelta

# מפתח זמני לפיתוח (בפרודקשן זה יימשך מ-config.py שמביא מה-.env)
SECRET_KEY = "SUPER_SECRET_KEY_FOR_JWT_SIGNING_DONT_USE_IN_PROD"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    מייצרת טוקן JWT חתום ומאובטח המכיל את נתוני המשתמש
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30) # תוקף ברירת מחדל של 30 דקות
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict | None:
    """
    מפענחת ומאמתת טוקן JWT.
    אם הטוקן תקין ובתוקף - מחזירה את ה-dict של הדאטא.
    אם פג תוקף או פגום - מחזירה None.
    """
    try:
        # מפענח את הטוקן באמצעות המפתח והאלגוריתם של המערכת
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # הטוקן פג תוקף (עברו יותר מ-30 דקות)
        return None
    except jwt.PyJWTError:
        # הטוקן פגום, שונה או מזויף
        return None