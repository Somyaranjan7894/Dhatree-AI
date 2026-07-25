# ==============================================================================
# Dhatree AI Frontend Multi-Stage Dockerfile (React + TypeScript + Vite)
# ==============================================================================

# Stage 1: Dev / Base
FROM node:20-alpine as dev
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stage 2: Production Build
FROM node:20-alpine as builder
WORKDIR /app/frontend
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Minimal Nginx serving static files (if run standalone outside main docker-compose.prod.yml)
FROM nginx:1.25-alpine as prod
COPY --from=builder /app/frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
