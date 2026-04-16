#!/bin/bash
timestamp=$(date +"%Y%m%d_%H%M%S")
mkdir -p backups
cp -r reports "backups/reports_$timestamp"
echo "Reports backed up to backups/reports_$timestamp"
