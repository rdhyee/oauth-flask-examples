set -e
docker build -t rdhyee/github-oauth .

# create server.key, server.crt
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=XX/ST=XX/L=XX/O=dockergenerated/CN=dockergenerated"

# copy the certs
docker cp server.crt certs:/etc/nginx/certs/github-oauth.ydns.eu.crt
docker cp server.key certs:/etc/nginx/certs/github-oauth.ydns.eu.key

# jupyter stack images (don't map local drive)
docker run -d --name github  \
   -e VIRTUAL_HOST=github-oauth.ydns.eu \
   -e VIRTUAL_PORT=5000 \
   -e GITHUB_CONSUMER_KEY=$GITHUB_CONSUMER_KEY \
   -e GITHUB_CONSUMER_SECRET=$GITHUB_CONSUMER_SECRET \
   -e GITHUB_REDIRECT_URI=$GITHUB_REDIRECT_URI \
   -e OAUTHLIB_INSECURE_TRANSPORT=1 \
     rdhyee/github-oauth
