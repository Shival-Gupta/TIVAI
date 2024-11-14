# Use Node.js image with version 18 (or other version that supports Next.js 14)
FROM node:18-slim

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose port 3000 for Next.js app
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "run", "dev"]
