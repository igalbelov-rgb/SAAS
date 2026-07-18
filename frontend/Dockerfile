# שלב א': בניית האפליקציה (Compiling)
FROM node:20-alpine AS builder

WORKDIR /app

# עדכון חבילות אבטחה של אלפיין
RUN apk update && apk upgrade

COPY package*.json ./
# התקנה נקייה ומדויקת לפרודקשן
RUN npm ci

COPY . .
RUN npm run build

# שלב ב': השארת הקבצים המוכנים בתיקיית העבודה
# משתמשים באימג' קטן של Alpine כדי לא להריץ שרת נוסף ברקע
FROM alpine:latest

WORKDIR /app

# מעתיקים את תיקיית ה-dist המוכנת
COPY --from=builder /app/dist ./dist

# הפקודה הזו שומרת על הקונטיינר חי או פשוט מעתיקה את הקבצים ל-Volume
CMD ["sh", "-c", "echo 'Frontend build files are ready in volume!' && sleep infinity"]