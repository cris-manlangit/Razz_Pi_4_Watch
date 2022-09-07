#!/bin/bash

curl -A 'random' https://old.reddit.com/r/mechmarket/new.json > r-mm-test.json
python rmm-email.py
mutt -s "smooth operator" cris.manlangit@gmail.com < mutt_test_rmm.html
