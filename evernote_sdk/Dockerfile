# Using the Python base image
FROM python:2.7

# Python modules
RUN pip install flask==0.10.1
#RUN pip install requests_oauthlib
RUN pip install evernote

# add the app and settings file
COPY evernote_oauth1a.py /evernote_oauth1a.py

# expose port
EXPOSE 5000

# run the webserver
WORKDIR /
CMD python evernote_oauth1a.py
