FROM node:21-bullseye-slim as base

ARG PORT=3000

ENV NODE_ENV=production

WORKDIR /src

# Build
FROM base as build

COPY --link ./passman-frontend/package.json ./passman-frontend/package-lock.json ./
RUN npm install --production=false

COPY --link ./passman-frontend .

RUN npm run build
RUN npm prune

# Run
FROM base

ENV PORT=$PORT

COPY --from=build /src/.output /src/.output

CMD [ "node", ".output/server/index.mjs" ]