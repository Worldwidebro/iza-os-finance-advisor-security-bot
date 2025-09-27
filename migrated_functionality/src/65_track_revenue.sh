#!/bin/bash
gemini "Read Stripe logs → sum payments → output JSON { date, revenue }" | jq . >> finance/revenue.json
