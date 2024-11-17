#!/bin/bash

websites=(
    "https://google.com"
    "https://facebook.com"
    "https://twitter.com"
)

log_file="website_status.log"

echo "Processing availability ..."
echo "Results will be saved in $log_file"

# Clearing old log file.
> $log_file

for site in "${websites[@]}"; do
    status_code=$(curl -o /dev/null -s -w "%{http_code}" "$site")

    if [[ "$status_code" -eq 200 ]]; then
        result="$site is UP"
    else
        result="$site is DOWN"
    fi

    # Write result into log file.
    echo "$result" >> "$log_file"

    # Output the result to console
    echo "$result"
done

echo "Website check completed. Results saved in '$log_file'."