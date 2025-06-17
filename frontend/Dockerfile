# ./frontend/Dockerfile
FROM node:18

WORKDIR /app

# Copy only package files first for caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start dev server
CMD ["npm", "run", "dev"]
