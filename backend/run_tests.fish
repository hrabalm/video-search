#!/usr/bin/env fish
cd (dirname (status --current-filename))
withenv .env poetry run pytest
