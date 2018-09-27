FROM node
COPY app /app
WORKDIR app
RUN npm install > /dev/null
EXPOSE 3000
CMD ["npm","start"]
