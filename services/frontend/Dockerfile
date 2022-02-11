FROM node:lts-buster

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install @vue/cli -g

COPY package.json .
COPY package-lock.json .
RUN npm install
RUN npm install vuetify


CMD ["npm", "run", "serve"]
