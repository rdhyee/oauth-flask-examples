# Using the Python base image
FROM python:2.7

# Python modules
RUN pip install flask==0.10.1
RUN pip install requests_oauthlib

# add the app and settings file
COPY mendeley_flask_oauth2.py /mendeley_flask_oauth2.py

# expose port
EXPOSE 5000

# to run in insecure mode
# ENV OAUTHLIB_INSECURE_TRANSPORT 1

# run the webserver
WORKDIR /
CMD python mendeley_flask_oauth2.py
