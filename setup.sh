#!/bin/sh

PYTHONPATH='./:./data_preparation_pipeline' luigi --module clean_data DataSinkTask --local-scheduler
