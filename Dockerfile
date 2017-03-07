# Dockerfile for my django application

# Use onbuild - this will copy current directory to /usr/src/app and run pip install -r requirements.txt
FROM python:3.6-onbuild

#
# RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

RUN python manage.py collectstatic --noinput
RUN chmod -R -x+X *
RUN chmod +x start.sh
RUN chmod +x init.sh
CMD ["./start.sh"]
