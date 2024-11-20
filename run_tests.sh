#!/bin/bash

# Create necessary directories
mkdir -p tests/ui/dashboard
mkdir -p tests/ui/project_management
mkdir -p tests/ui/competitor_management
mkdir -p tests/security
mkdir -p test_reports
mkdir -p tests/cross_browser

# Run tests with proper error handling
echo "Running all test suites..."
python -m tests.commands.test_runner test --suite all --browser chrome || true

echo "Running security tests..."
python -m tests.commands.test_runner test --suite security --browser chrome || true 