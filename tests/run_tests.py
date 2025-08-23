#!/usr/bin/env python3
"""
Test Runner for Ethereum Fraud Detection System

This script runs all tests in the project and provides a comprehensive report.
It can be used for continuous integration and local development testing.
"""

import unittest
import sys
import os
import time
import argparse
from io import StringIO

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests(verbose=False, coverage=False):
    """
    Run all tests in the project
    
    Args:
        verbose (bool): Enable verbose output
        coverage (bool): Enable coverage reporting
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Configure test runner
    if verbose:
        verbosity = 2
    else:
        verbosity = 1
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=verbosity, stream=sys.stdout)
    
    # Run tests
    print("=" * 60)
    print("ETHEREUM FRAUD DETECTION SYSTEM - TEST SUITE")
    print("=" * 60)
    print(f"Running tests with verbosity level: {verbosity}")
    print(f"Test discovery directory: {start_dir}")
    print("-" * 60)
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("-" * 60)
    print("TEST SUMMARY")
    print("-" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    
    # Print detailed results if there are failures or errors
    if result.failures:
        print("\nFAILURES:")
        print("-" * 20)
        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print(traceback)
            print()
    
    if result.errors:
        print("\nERRORS:")
        print("-" * 20)
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(traceback)
            print()
    
    # Print success message if all tests passed
    if result.wasSuccessful():
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ SOME TESTS FAILED! ❌")
        print("=" * 60)
        return False

def run_specific_test(test_name, verbose=False):
    """
    Run a specific test module or test case
    
    Args:
        test_name (str): Name of the test module or test case
        verbose (bool): Enable verbose output
    
    Returns:
        bool: True if test passed, False otherwise
    """
    loader = unittest.TestLoader()
    
    # Try to load the specific test
    try:
        if '.' in test_name:
            # Specific test case
            suite = loader.loadTestsFromName(test_name)
        else:
            # Test module
            suite = loader.loadTestsFromName(f'tests.{test_name}')
    except Exception as e:
        print(f"Error loading test '{test_name}': {e}")
        return False
    
    # Configure test runner
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity, stream=sys.stdout)
    
    # Run test
    print(f"Running specific test: {test_name}")
    print("-" * 40)
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    print(f"\nTest completed in {end_time - start_time:.2f} seconds")
    return result.wasSuccessful()

def list_available_tests():
    """List all available test modules"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]
    
    print("Available test modules:")
    print("-" * 30)
    for test_file in sorted(test_files):
        module_name = test_file[:-3]  # Remove .py extension
        print(f"  {module_name}")
    
    print(f"\nTotal: {len(test_files)} test modules")

def main():
    """Main function to handle command line arguments and run tests"""
    parser = argparse.ArgumentParser(
        description='Run tests for Ethereum Fraud Detection System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py -v                 # Run all tests with verbose output
  python run_tests.py --list             # List available test modules
  python run_tests.py test_api           # Run only API tests
  python run_tests.py test_data_cleaning # Run only data cleaning tests
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available test modules'
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Enable coverage reporting (requires coverage package)'
    )
    
    parser.add_argument(
        'test_name',
        nargs='?',
        help='Specific test module or test case to run'
    )
    
    args = parser.parse_args()
    
    # Handle list command
    if args.list:
        list_available_tests()
        return
    
    # Run specific test if provided
    if args.test_name:
        success = run_specific_test(args.test_name, args.verbose)
        sys.exit(0 if success else 1)
    
    # Run all tests
    success = run_all_tests(args.verbose, args.coverage)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
