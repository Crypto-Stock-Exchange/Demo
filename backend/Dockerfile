FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
  openssl \
  gcc \
  g++ \
  libffi-dev \
  libssl-dev \
  libpq-dev \
  libtool \
  libpqxx-dev \
  pkg-config \
  make \
  cmake \
  rapidjson-dev \
  libcurl4-openssl-dev \
  cron \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#C++
RUN g++ -std=c++17 -O2 /app/offcain/cpp/*.cpp -o /usr/local/bin/cpp_worker -lpqxx -lpq -lcurl -pthread
COPY .env /usr/local/bin/.env

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY offcain/scheduled_populate.py /app/offcain/scheduled_populate.py

COPY crontab.txt /etc/cron.d/stock-cron

RUN chmod 0644 /etc/cron.d/stock-cron && \
  crontab /etc/cron.d/stock-cron

RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]
