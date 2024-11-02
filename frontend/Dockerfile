FROM node:18.20-alpine

ENV NODE_OPTIONS="--max-old-space-size=4096"

WORKDIR /frontend

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build