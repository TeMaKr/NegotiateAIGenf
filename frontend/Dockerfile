# ==============================================================================
# Stage 1: Build stage
# Downloads and installs all dependencies needed for building
# ==============================================================================
FROM node:lts AS base

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source files
COPY . .

# Build the application
RUN npm run build


# ==============================================================================
# Stage 2: Deploy stage
# Uses nginx to serve the built application
# ==============================================================================
FROM nginx:stable-alpine@sha256:aed99734248e851764f1f2146835ecad42b5f994081fa6631cc5d79240891ec9 AS deploy

# Fix vulnerabilities in alpine.
# Note: The specific versions of libxml2 may vary based on the latest available images. This can 
# possibly be removed or updated in the future.
RUN apk update && \
    apk add --no-cache libxml2=2.13.4-r6 && \
    rm -rf /var/cache/apk/*

# Copy built files from the base stage to the nginx html directory
COPY --from=base /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]