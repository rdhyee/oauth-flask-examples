set -e
docker build -t rdhyee/github-oauth .
PORT=${1:-80}

# jupyter stack images (don't map local drive)
docker run -d --name github -p $PORT:5000 \
   -e GITHUB_CONSUMER_KEY=$GITHUB_CONSUMER_KEY \
   -e GITHUB_CONSUMER_SECRET=$GITHUB_CONSUMER_SECRET \
   -e GITHUB_REDIRECT_URI=$GITHUB_REDIRECT_URI \
     rdhyee/github-oauth
