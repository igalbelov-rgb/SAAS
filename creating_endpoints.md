כאשר מוסיפים נתיבים (Endpoints) חדשים או כפתורים שמדברים עם ה-Backend, העבודה תמיד מתחלקת ל-3 שכבות: הגדרת הנתיב ב-Backend, רישום הראוטר ב-main.py, וחשיפת הקריאה בפרונטאנד.

שלב 1: יצירת/עדכון קובץ הראוטר הפנימי ב-Backend
אם מדובר בישות חדשה לגמרי, ניצור קובץ חדש תחת התיקייה backend/app/api/.

כלל ברזל: לא כותבים /api או את שם הישות בתוך ה-APIRouter הפנימי – משאירים את הקידומת נקייה לטובת גמישות ב-main.py.

📄 קובץ לדוגמה: backend/app/api/campaigns.py

Python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 1. מגדירים את הראוטר ללא תחילית גלובלית (prefix)
router = APIRouter(tags=["Campaigns Management"])

# 2. הגדרת המודל (Schema) של הבקשה מהפרונטאנד
class CampaignRequest(BaseModel):
    name: str
    budget: float

# 3. יצירת ה-Endpoint עצמו
@router.post("/create") # הכתובת הפנימית בלבד!
async def create_campaign(payload: CampaignRequest):
    try:
        # לוגיקה עסקית (למשל שמירה בבסיס הנתונים)
        return {"success": True, "campaign_name": payload.name}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
שלב 2: רישום הראוטר בקובץ המרכזי
זהו שלב המפתח שמקשר את הראוטר הפנימי אל העולם החיצון, ומבטיח ש-Nginx והדפדפן ידעו לאן לגשת בלי כפילויות.

📄 קובץ לשינוי: backend/app/main.py

Python
# 1. מייבאים את הראוטר החדש שיצרנו
from api.campaigns import router as campaigns_router

# 2. מחברים אותו תחת הקידומת המלאה והמדויקת שלו (מתחת לראוטרים הקיימים)
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products_router, prefix="/api/products", tags=["Products & Automation"])

# 🔥 הוספת הראוטר החדש:
app.include_router(campaigns_router, prefix="/api/campaigns", tags=["Campaigns Management"])
איך הנתיב ייראה בפועל? השילוב של ה-prefix מ-main.py והנתיב מהראוטר הפנימי ירכיבו בדיוק את הכתובת הבאה: POST http://localhost/api/campaigns/create.

שלב 3: חשיפת הקריאה ב-Axios (Frontend)
כדי שהפרונטאנד יוכל לבצע את קריאת ה-HTTP בצורה מסודרת, אנחנו מוסיפים מתודה לשירות ה-API הקיים.

📄 קובץ לשינוי: frontend/src/services/api.js

JavaScript
// בתוך אובייקט ה-API הקיים (או יצירת שירות חדש באותו קובץ):
export const campaignService = {
  createCampaign: async (campaignData) => {
    // קריאה לנתיב המדויק שהגדרנו ב-Backend
    const response = await api.post('/campaigns/create', campaignData);
    return response.data;
  }
};
שלב 4: חיבור לכפתור/רכיב ב-UI (React)
עכשיו נשאר רק לקרוא לשירות בזמן לחיצה על כפתור בדשבורד או ברכיב הרלוונטי.

📄 קובץ לשינוי: קובץ הקומפוננטה שלך (למשל Dashboard.jsx)

JavaScript
import { campaignService } from '../services/api';

export default function Dashboard() {
  const [loading, setLoading] = useState(false);

  const handleCreateCampaign = async () => {
    setLoading(true);
    try {
      const data = await campaignService.createCampaign({
        name: "Summer Sale 2026",
        budget: 500.0
      });
      if (data.success) {
        alert(`Campaign ${data.campaign_name} created successfully!`);
      }
    } catch (err) {
      console.error("Failed to create campaign", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button 
      onClick={handleCreateCampaign}
      disabled={loading}
      className="bg-amber-400 hover:bg-amber-500 cursor-pointer text-slate-900 font-bold p-4 rounded-xl"
    >
      {loading ? 'Creating...' : 'Launch New Campaign'}
    </button>
  );
}
📋 צ'קליסט מהיר לכל נתיב עתידי:
[ ] בתוך קובץ ה-API הפנימי: הראוטר מוגדר נקי (router = APIRouter()), ה-Decorator מכיל רק את תת-הנתיב (@router.post("/action")).

[ ] בתוך main.py: הראוטר מיובא ומחובר עם הכתובת המלאה שכוללת /api/ בתחילתה.

[ ] בתוך api.js: יש פונקציית Axios מתאימה שמצביעה על היעד (ללא התחילית /api הכללית אם ה-BaseURL של Axios כבר כולל אותה).