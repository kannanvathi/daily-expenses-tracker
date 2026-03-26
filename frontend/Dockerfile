FROM node:18-alpine as build

WORKDIR /app

# install dependencies
COPY frontend/package*.json ./
RUN npm ci

# build
COPY frontend/ .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
