# Node.js alapú image
FROM node:20-alpine

# Munkakönyvtár beállítása
WORKDIR /app

# Csomagok telepítése
COPY package*.json ./
RUN npm install

# Frontend kód másolása
COPY . .

# Fejlesztői környezet indítása
CMD ["npm", "run", "serve"]

# Az alkalmazás elérhetővé tétele a hoston
EXPOSE 8080
