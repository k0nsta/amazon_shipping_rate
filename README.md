# Amazon Shipping Rate Scraper by Scrapy & Splash

A shipping rate spider tool based on Scrapy framework and Splash for interacting with UI.

## Problem Description

I've had a task to scrape shipping rate for the specific products for different geolocation (different countries). Amazon has shown correct rate if client IP address and provided shipping address in UI have one origin (country).

## Resolution

I've created a spider based on `Scrapy` Framework, which was deployed on VPS. Scrapyd was a service for running the spider.

## Built With

- [Scrapy](https://scrapy.org) - An open source and collaborative framework for extracting the data you need from websites
- [Splash](https://github.com/scrapinghub/splash) - Lightweight, scriptable browser as a service with an HTTP API

