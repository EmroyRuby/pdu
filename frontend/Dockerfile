# Use an official Node.js runtime as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Install Angular CLI globally (if not already installed)
RUN npm install -g @angular/cli

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the Angular project files to the container
COPY . .

# Build the Angular app for production
RUN ng build --configuration=production

# Expose the port that the Angular app will run on
EXPOSE 4200

# Start the Angular app
CMD ["ng", "serve", "--host", "0.0.0.0"]
