# PlatePoint POS — production image
FROM node:20-alpine

# wget is used by the container healthcheck (already present in alpine base)
WORKDIR /app

# Install production dependencies only (skips pg-mem / test tooling)
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# App source
COPY . .

ENV NODE_ENV=production
ENV PORT=4242
EXPOSE 4242

# Container health: the app exposes an unauthenticated /api/health endpoint
HEALTHCHECK --interval=30s --timeout=4s --start-period=15s --retries=3 \
  CMD wget -qO- http://127.0.0.1:4242/api/health || exit 1

# On boot the server runs schema migration and seeds an empty DB automatically.
CMD ["node", "src/server.js"]
