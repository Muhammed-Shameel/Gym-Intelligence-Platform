# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Accept the URL as a build argument
ARG VITE_API_BASE_URL
# Bake it into the build
RUN VITE_API_BASE_URL=$VITE_API_BASE_URL npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
