FROM node:18-slim AS build
WORKDIR /app
COPY package.json package.json
COPY src src
COPY public public
RUN npm install && npm run build

FROM node:18-slim
WORKDIR /app
COPY --from=build /app/dist /app/dist
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
