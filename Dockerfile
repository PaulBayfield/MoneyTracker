FROM sanicframework/sanic:lts-py3.11

RUN apk add --no-cache git

COPY . ./MoneyTracker

WORKDIR /MoneyTracker

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "__main__.py"]
