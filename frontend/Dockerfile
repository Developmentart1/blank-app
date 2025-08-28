FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* /app/
RUN npm install --loglevel=error || (npm init -y && npm install --loglevel=error)
COPY . /app
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
