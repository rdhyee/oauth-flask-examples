set -e
docker build -t rdhyee/mendeley-oauth .

# create server.key, server.crt
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=XX/ST=XX/L=XX/O=dockergenerated/CN=dockergenerated"

# copy the certs
docker cp server.crt certs:/etc/nginx/certs/mendeley-oauth.ydns.eu.crt
docker cp server.key certs:/etc/nginx/certs/mendeley-oauth.ydns.eu.key

source setenv.sh

# jupyter stack images (don't map local drive)
docker run -d --name mendeley  \
   -e VIRTUAL_HOST=mendeley-oauth.ydns.eu \
   -e VIRTUAL_PORT=5000 \
   -e MENDELEY_CONSUMER_KEY=$MENDELEY_CONSUMER_KEY \
   -e MENDELEY_CONSUMER_SECRET=$MENDELEY_CONSUMER_SECRET \
   -e MENDELEY_REDIRECT_URI=$MENDELEY_REDIRECT_URI \
   -e OAUTHLIB_INSECURE_TRANSPORT=1 \
     rdhyee/mendeley-oauth
