#!/bin/sh

PYTHONPATH='.' luigi --module prepare_data ExtractSchoolData --local-scheduler
