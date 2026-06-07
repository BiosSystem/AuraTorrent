# Stage 1: Build the Vue/TypeScript client frontend
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Create a minimal image containing just the built static files
FROM scratch
COPY --from=build /app/dist /auratorrent

