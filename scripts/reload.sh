#!/bin/bash

set -e

bash ./scripts/down.sh \
    && bash ./scripts/build.sh \
    && bash ./scripts/up.sh

