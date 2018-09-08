FROM zenika/alpine-node:9

COPY package.json yarn.lock /usr/src/app/
RUN yarn
COPY . /usr/src/app

CMD [ "yarn", "start" ]