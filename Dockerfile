# Stage 1: Build the Vue/TypeScript client frontend
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve the static build with nginx (runnable, pullable image).
# Vite emits the web root (index.html + assets) to ./auratorrent/public.
FROM nginx:1.27-alpine AS serve
COPY --from=build /app/auratorrent/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

# Stage 3: Export-only image containing just the static files, for mounting
# into an existing qBittorrent container's alternative WebUI directory.
FROM scratch AS export
COPY --from=build /app/auratorrent/public /auratorrent
