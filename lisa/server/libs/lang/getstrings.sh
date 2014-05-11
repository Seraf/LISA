#!/bin/sh
xgettext --package-name lisa --package-version 1.0 --default-domain lisa --output lisa.pot ../*.py ../txscheduler/*.py ../../plugins/*.py
