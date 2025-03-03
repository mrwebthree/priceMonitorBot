#!/bin/bash
docker build -t price-monitor .
docker run --env-file .env price-monitor
