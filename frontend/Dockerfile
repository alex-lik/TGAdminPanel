FROM node:20 AS build
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
WORKDIR /app
WORKDIR /app

# Копируем package.json из app
COPY app/package*.json ./
RUN npm install

# Копируем весь frontend/app внутрь контейнера
COPY app/ .

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY app/default.conf /etc/nginx/conf.d/default.conf
