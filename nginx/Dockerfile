FROM nginx:1.25-alpine
# מחיקת קונפיגורציית ברירת המחדל והחלפתה בקובץ החכם שלנו
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/