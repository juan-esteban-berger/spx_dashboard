FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 8081

# Start development server with host networking
CMD ["npm", "run", "dev", "--", "--port", "8081", "--host"]
