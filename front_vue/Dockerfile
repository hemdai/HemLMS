FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
EXPOSE 8080

# Staging
FROM build-stage as hemlms-frontend-staging-stage
RUN npm install -g http-server
COPY --from=build-stage /app .
RUN npm run build_staging

# Staging
FROM build-stage as hemlms-frontend-production-stage
RUN npm install -g http-server
COPY --from=build-stage /app .
RUN npm run build_production