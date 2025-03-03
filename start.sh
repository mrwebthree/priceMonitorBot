#!/bin/bash
docker build -t price-monitor .
docker run -d --env-file .env price-monitor
