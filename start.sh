#!/bin/bash

cp .env.example .env
make upgrade-version
make up
