# Using the Python base image
FROM python:2.7

# Python modules
RUN pip install flask==0.10.1
RUN pip install requests_oauthlib

# add the app and settings file
COPY github_flask_oauth2.py /github_flask_oauth2.py

COPY reflect.py /reflect.py

# expose port
EXPOSE 5000

# to run in insecure mode
ENV OAUTHLIB_INSECURE_TRANSPORT 1

# run the webserver
WORKDIR /
CMD python github_flask_oauth2.py
#CMD python reflect.py
