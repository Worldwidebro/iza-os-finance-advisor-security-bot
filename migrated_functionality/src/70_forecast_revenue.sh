#!/bin/bash
gemini "Use NuminaMath: fit ARIMA model → predict → output JSON { forecast }" | jq . > finance/forecast.json
