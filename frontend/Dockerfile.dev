FROM node:20-alpine

WORKDIR /app

RUN apk update && apk upgrade

COPY package*.json ./
# נשתמש ב-npm install בפיתוח כדי לאפשר גמישות
RUN npm install

COPY . .

# חשיפת הפורט של שרת הפיתוח של Vite
EXPOSE 5173

# הרצת שרת הפיתוח עם דגל --host (חובה כדי ש-Nginx החיצוני יוכל לגשת לקונטיינר)
CMD ["npm", "run", "dev", "--", "--host"]

# # שלב א': בנייה
# FROM node:20-alpine AS builder

# WORKDIR /app

# # הוספת שדרוג חבילות פנימיות של אלפיין
# RUN apk update && apk upgrade

# COPY package*.json ./
# RUN npm ci

# COPY . .
# RUN npm run build

# # שלב ב': הגשה
# FROM nginx:1.25-alpine

# # שדרוג חבילות פנימיות גם בשכבת הריצה של nginx
# RUN apk update && apk upgrade

# COPY --from=builder /app/dist /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]