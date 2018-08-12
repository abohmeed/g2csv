FROM node
RUN git clone -q https://github.com/abohmeed/g2csv.git
WORKDIR g2csv
RUN npm install > /dev/null
EXPOSE 3000
CMD ["npm","start"]