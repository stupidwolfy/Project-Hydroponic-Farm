FROM node:lts-buster

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_OPTIONS=--max_old_space_size=1024

RUN npm install @vue/cli -g

COPY package.json .
COPY package-lock.json .
RUN npm install
RUN npm install vuetify


CMD ["npm", "run", "serve"]
