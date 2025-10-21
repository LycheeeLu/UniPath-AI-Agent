# ---------- build frontend ----------
FROM node:20-alpine AS build
WORKDIR /app/frontend
COPY unipath-frontend/ .
RUN npm ci && npm run build

# ---------- run backend ----------
FROM python:3.11-slim
WORKDIR /app
COPY backend/ ./backend
COPY --from=build /app/frontend/dist ./backend/static/dist
RUN pip install --no-cache-dir -r backend/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
