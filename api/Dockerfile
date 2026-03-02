
# Use the official Node.js 20 image as the base
FROM node:20-slim

# Create and change to the app directory
WORKDIR /usr/src/app

# Install system dependencies for Prisma
RUN apt-get update -y && apt-get install -y openssl

# Copy application dependency manifests to the container image.
# A wildcard is used to ensure both package.json and package-lock.json are copied.
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy local code to the container image.
COPY . .

# Generate Prisma client
RUN npm run db:generate

# Bind the app to port 8080 by default (Cloud Run requirement)
ENV PORT=8080

# Run the web service on container startup.
CMD [ "npm", "start" ]
