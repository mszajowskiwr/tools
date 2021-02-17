#!/bin/bash

set -euo pipefail

[ $# -ne 1 ] && echo "Usage: $(basename $0) <CONSUMER_NAME>" >&2 && exit 1 
CONSUMER="$1"

for dependency in jq curl; do
    ! command -v "${dependency}" &> /dev/null && echo "'${dependency}' missing, please install it" && exit 1
done

echo "Fetching data for: ${CONSUMER}"

ALL_VERSIONS=$(curl "https://pact-broker.wremitdev.com/pacticipants/${CONSUMER}/versions" 2>/dev/null)

ERROR_MSG=$(echo ${ALL_VERSIONS} | jq '.error')

[[ "${ERROR_MSG}" != null ]] && echo "ERROR: ${ERROR_MSG}" >&2 && exit 1

ALL_PROVIDERS=$(echo "${ALL_VERSIONS}" | jq .'_embedded.versions[]._links."pb:pact-versions"[].href' | sed 's#.*/provider/##' | sed 's#/.*##' | sort -u)

echo "${CONSUMER} has pacts with following backend services:" ${ALL_PROVIDERS}

echo -- "--------------"

for provider in ${ALL_PROVIDERS}; do
    echo "${CONSUMER} has pact with ${provider} on paths:"
    # TODO: what if some pact existed before, but in the current 'latest' it's not there?
    PACT_URL="https://pact-broker.wremitdev.com/pacts/provider/${provider}/consumer/${CONSUMER}/latest"
    curl "${PACT_URL}"  2>/dev/null | jq ".interactions[].request.path"
done