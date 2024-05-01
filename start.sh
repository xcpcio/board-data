#! /bin/bash

# shellcheck disable=SC2068
python3 \
  -m http.server \
  -b 127.0.0.1 \
  $@ \
  8080
