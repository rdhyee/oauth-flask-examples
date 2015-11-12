set -e
docker build -t rdhyee/evernotesdk-oauth .

# create server.key, server.crt
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=XX/ST=XX/L=XX/O=dockergenerated/CN=dockergenerated"

# copy the certs
docker cp server.crt certs:/etc/nginx/certs/evernotesdk-oauth.ydns.eu.crt
docker cp server.key certs:/etc/nginx/certs/evernotesdk-oauth.ydns.eu.key

# setup the environment
source setenv.sh

# jupyter stack images (don't map local drive)
docker run -d --name evernotesdk  \
   -e VIRTUAL_HOST=evernotesdk-oauth.ydns.eu \
   -e VIRTUAL_PORT=5000 \
   -e EVERNOTE_CONSUMER_KEY=$EVERNOTE_CONSUMER_KEY \
   -e EVERNOTE_CONSUMER_SECRET=$EVERNOTE_CONSUMER_SECRET \
   -e EVERNOTE_PRODUCTION=$EVERNOTE_PRODUCTION \
   -e EVERNOTE_DEV_AUTH_TOKEN=$EVERNOTE_DEV_AUTH_TOKEN \
   -e EVERNOTE_CALLBACK_URI=$EVERNOTE_CALLBACK_URI \
   -e OAUTHLIB_INSECURE_TRANSPORT=1 \
     rdhyee/evernotesdk-oauth
