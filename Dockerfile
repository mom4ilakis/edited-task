FROM python:3.13

LABEL author="mvmarinov@pm.me"

VOLUME /screenshots
VOLUME /db

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps

ENV DB_FILE_FOLDER="/db"
ENV SCREENSHOTS_FOLDER="/screenshots"

RUN python db.py

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["main.py"]