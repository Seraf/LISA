#!/bin/sh
xgettext --package-name lisa --package-version 1.0 --default-domain lisa --output lisa.pot ../*.py ../libs/*.py ../libs/txscheduler/*.py ../plugins/*.py
xgettext --package-name intents --package-version 1.0 --default-domain intents --output intents.pot ../core/*.py