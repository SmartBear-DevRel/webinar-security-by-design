#!/bin/bash

## ACC
# ENDPOINT=https://sbdevrel-fua-smartbearcoin-acc.azurewebsites.net/api/payees
## PROD
# ENDPOINT=https://sbdevrel-fua-smartbearcoin-prd.azurewebsites.net/api/payees

ENDPOINT=${ENDPOINT:-'http://0.0.0.0:8000'}
PROJECT_FOLDER=${PROJECT_FOLDER:-'ReadyAPI-Tests'}
PROJECT_FILE=${PROJECT_FILE:-'secure-by-design-readyapi-project.xml'}

MISSING=()
[ ! "$PROJECT_FOLDER" ] && MISSING+=("PROJECT_FOLDER")
[ ! "$PROJECT_FILE" ] && MISSING+=("PROJECT_FILE")
[ ! "$ENDPOINT" ] && MISSING+=("ENDPOINT")
[ ! "$SLM_API_KEY" ] && MISSING+=("SLM_API_KEY")

case $(uname -sm) in
'Darwin x86' | 'Darwin x86_64' | 'Darwin arm64' | 'Windows')
    ENDPOINT=${ENDPOINT/localhost/host.docker.internal}
    ;;
esac
if [ ${#MISSING[@]} -gt 0 ]; then
    echo "ERROR: The following environment variables are not set:"
    printf '\t%s\n' "${MISSING[@]}"
    exit 1
fi

echo "executing security tests for ${PROJECT_FILE}"
docker run --rm --network="host" \
    -v=${PWD}/${PROJECT_FOLDER}:/project \
    -e SLM_LICENSE_SERVER="https://api.slm.manage.smartbear.com:443" \
    -e API_KEY=${SLM_API_KEY} \
    -e ENDPOINT=${ENDPOINT} \
    -e PROJECT_FILE=${PROJECT_FILE} \
    -e COMMAND_LINE="'-f/project' '-RSecurity Issues Report' -FPDF '-Elocal' /project/${PROJECT_FILE}" \
    smartbear/readyapi-security-testrunner:latest
