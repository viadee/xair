########### FRONTEND ###########

# 2 stages

# temp image for build
# FROM node:alpine as build
FROM node:12.18.0-alpine as build
WORKDIR /webapp

RUN apk update && apk add bash


COPY ./xai-recommender-frontend/package.json .
COPY ./xai-recommender-frontend/package-lock.json .


# Install the dependencies and make the folder
RUN npm install 
# --legacy-peer-deps
COPY ./xai-recommender-frontend/ .

# please build the Docker container from the directory above to ensure the copy of the frontend_input_config
COPY ./xai_xps/src/resources/config/frontend_input_config.json ./static/config/frontend_input_config.json


# clean public and .cache folder
RUN npm run clean

# Build the project and copy the files
RUN npm run build




# production environment
FROM nginx:stable-alpine

COPY ./xai-recommender-frontend/nginx/nginx.conf /etc/nginx/nginx.conf


## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /webapp/public /usr/share/nginx/html

# copy fonts
RUN mkdir /usr/share/nginx/html/static/fonts
ADD ./xai-recommender-frontend/static/fonts /usr/share/nginx/html/static/fonts

EXPOSE 3000 80
CMD ["nginx", "-g", "daemon off;"]
