#!/bin/sh

mongod --dbpath ~/opt/mongodb/data &
paster serve production.ini &
