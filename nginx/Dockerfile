# שלב א': בניית ה-Frontend
FROM node:20-alpine AS builder
WORKDIR /app
COPY ./frontend/package*.json ./
RUN npm ci
COPY ./frontend/ ./
RUN npm run build

# שלב ב': שרת ה-Nginx
FROM nginx:1.25-alpine
# העתקת קונפיגורציית ה-Nginx שלך
COPY ./nginx/nginx.prod.conf /etc/nginx/conf.d/default.conf
# העתקת הקבצים המוכנים ישירות לשרת
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]