#!/bin/bash

# shellcheck disable=SC2068
python3 \
  -m http.server \
  $@ \
  8080
