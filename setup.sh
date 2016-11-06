#!/bin/sh

PYTHONPATH='./:./data_preparation_pipeline' luigi --module run_all_data_tasks AllDataTasks --local-scheduler
