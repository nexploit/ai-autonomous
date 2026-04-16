# Multi-stage build für Frontend
FROM node:22-alpine AS builder

WORKDIR /app

# Cache dependencies layer separately
COPY package*.json ./
RUN npm ci --prefer-offline --no-audit 2>/dev/null || npm install --prefer-offline --no-audit

COPY . .
RUN npm run build

# Production stage - minimal runtime
FROM node:22-alpine

WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm ci --prefer-offline --no-audit --omit=dev 2>/dev/null || npm install --prefer-offline --no-audit --omit=dev && npm cache clean --force

# Copy assets and server code
COPY --from=builder /app/dist ./dist
COPY server.js .

EXPOSE 3000

CMD ["node", "--disable-warning=ExperimentalWarning", "server.js"]
