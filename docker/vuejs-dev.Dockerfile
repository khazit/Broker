FROM node:lts-alpine

# Create working directory
RUN mkdir app
WORKDIR /app
COPY web/package*.json ./

# Install project dependencies
RUN npm install

# Copy files to work directory
COPY web/. .

# Run app in dev mode
ENTRYPOINT ["npm", "run", "dev"]

# Network config
EXPOSE 8080
