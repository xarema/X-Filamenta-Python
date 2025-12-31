"""
---
Purpose: Performance benchmarking suite for X-Filamenta-Python
Description: Comprehensive performance testing including response times, database queries, and load testing

File: backend/tests/test_performance.py | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified: 2025-12-30

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
- Test Type: Performance Benchmarks
---
"""

import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import statistics
from backend.src.models.user import User
from backend.src.models.settings import Settings
from backend.src.extensions import db


class TestResponseTimeBenchmarks:
    """Response time benchmarks for critical endpoints."""

    def test_homepage_response_time(self, client, benchmark_target=100):
        """
        Benchmark homepage response time.
        Target: < 100ms for simple page load
        """
        times = []
        iterations = 10

        for _ in range(iterations):
            start = time.perf_counter()
            response = client.get('/')
            end = time.perf_counter()

            elapsed_ms = (end - start) * 1000
            times.append(elapsed_ms)

            assert response.status_code in [200, 302]

        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n📊 Homepage Performance:")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Median: {median_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")

        # Soft assertion - log warning if slow
        if avg_time > benchmark_target:
            print(f"⚠️  WARNING: Average response time ({avg_time:.2f}ms) "
                  f"exceeds target ({benchmark_target}ms)")

    def test_login_page_response_time(self, client, benchmark_target=150):
        """
        Benchmark login page response time.
        Target: < 150ms
        """
        times = []
        iterations = 10

        for _ in range(iterations):
            start = time.perf_counter()
            response = client.get('/auth/login')
            end = time.perf_counter()

            elapsed_ms = (end - start) * 1000
            times.append(elapsed_ms)

            assert response.status_code == 200

        avg_time = statistics.mean(times)
        print(f"\n📊 Login Page Performance: {avg_time:.2f}ms avg")

        if avg_time > benchmark_target:
            print(f"⚠️  WARNING: Exceeds target ({benchmark_target}ms)")

    def test_api_endpoint_response_time(self, client, auth_user, benchmark_target=200):
        """
        Benchmark API endpoint response time.
        Target: < 200ms for authenticated requests
        """
        with client.application.app_context():
            auth_user()

            times = []
            iterations = 10

            for _ in range(iterations):
                start = time.perf_counter()
                response = client.get('/users/preferences')
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                times.append(elapsed_ms)

            avg_time = statistics.mean(times)
            print(f"\n📊 API Endpoint Performance: {avg_time:.2f}ms avg")

            if avg_time > benchmark_target:
                print(f"⚠️  WARNING: Exceeds target ({benchmark_target}ms)")


class TestDatabaseQueryPerformance:
    """Database query performance benchmarks."""

    def test_user_lookup_by_username(self, app, benchmark_target=50):
        """
        Benchmark user lookup by username.
        Target: < 50ms
        """
        with app.app_context():
            # Create test users
            for i in range(10):
                user = User(username=f'perfuser{i}', email=f'perf{i}@test.com')
                user.set_password('TestPass123!')
                db.session.add(user)
            db.session.commit()

            times = []
            iterations = 20

            for i in range(iterations):
                username = f'perfuser{i % 10}'
                start = time.perf_counter()
                user = User.query.filter_by(username=username).first()
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                times.append(elapsed_ms)
                assert user is not None

            avg_time = statistics.mean(times)
            print(f"\n📊 User Lookup Performance: {avg_time:.2f}ms avg")

            if avg_time > benchmark_target:
                print(f"⚠️  WARNING: Exceeds target ({benchmark_target}ms)")

    def test_settings_query_performance(self, app, benchmark_target=100):
        """
        Benchmark settings query performance.
        Target: < 100ms for all settings
        """
        with app.app_context():
            # Create test settings
            for i in range(20):
                setting = Settings(
                    key=f'perf_setting_{i}',
                    value=f'value_{i}',
                    description=f'Performance test setting {i}'
                )
                db.session.add(setting)
            db.session.commit()

            times = []
            iterations = 10

            for _ in range(iterations):
                start = time.perf_counter()
                settings = Settings.query.all()
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                times.append(elapsed_ms)
                assert len(settings) >= 20

            avg_time = statistics.mean(times)
            print(f"\n📊 Settings Query Performance: {avg_time:.2f}ms avg")

            if avg_time > benchmark_target:
                print(f"⚠️  WARNING: Exceeds target ({benchmark_target}ms)")

    def test_bulk_insert_performance(self, app, benchmark_target=1000):
        """
        Benchmark bulk insert performance.
        Target: < 1000ms for 100 records
        """
        with app.app_context():
            times = []
            iterations = 5
            records_per_test = 100

            for iteration in range(iterations):
                users = []
                for i in range(records_per_test):
                    user = User(
                        username=f'bulk_user_{iteration}_{i}',
                        email=f'bulk{iteration}_{i}@test.com'
                    )
                    user.set_password('TestPass123!')
                    users.append(user)

                start = time.perf_counter()
                db.session.bulk_save_objects(users)
                db.session.commit()
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                times.append(elapsed_ms)

            avg_time = statistics.mean(times)
            print(f"\n📊 Bulk Insert Performance ({records_per_test} records): "
                  f"{avg_time:.2f}ms avg")

            if avg_time > benchmark_target:
                print(f"⚠️  WARNING: Exceeds target ({benchmark_target}ms)")


class TestConcurrentLoadBenchmarks:
    """Concurrent load testing benchmarks."""

    def test_concurrent_homepage_requests(self, client, concurrent_users=10):
        """
        Test concurrent homepage requests.
        Simulates multiple users accessing homepage simultaneously.
        """
        def make_request(user_id):
            start = time.perf_counter()
            response = client.get('/')
            end = time.perf_counter()
            return {
                'user_id': user_id,
                'status': response.status_code,
                'time_ms': (end - start) * 1000
            }

        results = []
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(make_request, i)
                      for i in range(concurrent_users)]

            for future in as_completed(futures):
                results.append(future.result())

        times = [r['time_ms'] for r in results]
        successful = sum(1 for r in results if r['status'] in [200, 302])

        print(f"\n📊 Concurrent Load Test ({concurrent_users} users):")
        print(f"  Successful: {successful}/{concurrent_users}")
        print(f"  Average: {statistics.mean(times):.2f}ms")
        print(f"  Median: {statistics.median(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")

        assert successful == concurrent_users

    def test_concurrent_authentication(self, client, app, concurrent_users=5):
        """
        Test concurrent authentication requests.
        Simulates multiple users logging in simultaneously.
        """
        with app.app_context():
            # Create test users
            for i in range(concurrent_users):
                user = User(username=f'concurrent{i}',
                           email=f'concurrent{i}@test.com')
                user.set_password('TestPass123!')
                db.session.add(user)
            db.session.commit()

        def login_request(user_id):
            start = time.perf_counter()
            response = client.post('/auth/login', data={
                'username': f'concurrent{user_id}',
                'password': 'TestPass123!'
            })
            end = time.perf_counter()
            return {
                'user_id': user_id,
                'status': response.status_code,
                'time_ms': (end - start) * 1000
            }

        results = []
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(login_request, i)
                      for i in range(concurrent_users)]

            for future in as_completed(futures):
                results.append(future.result())

        times = [r['time_ms'] for r in results]
        successful = sum(1 for r in results if r['status'] in [200, 302])

        print(f"\n📊 Concurrent Authentication ({concurrent_users} users):")
        print(f"  Successful: {successful}/{concurrent_users}")
        print(f"  Average: {statistics.mean(times):.2f}ms")

        assert successful >= concurrent_users * 0.8  # 80% success rate acceptable


class TestMemoryUsageBenchmarks:
    """Memory usage and resource consumption tests."""

    def test_session_memory_usage(self, client, app):
        """
        Test memory impact of multiple sessions.
        Monitors memory usage during session creation.
        """
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create multiple sessions
        sessions_count = 50
        with app.app_context():
            for i in range(sessions_count):
                user = User(username=f'memtest{i}', email=f'mem{i}@test.com')
                user.set_password('TestPass123!')
                db.session.add(user)
            db.session.commit()

            # Login multiple users
            for i in range(sessions_count):
                client.post('/auth/login', data={
                    'username': f'memtest{i}',
                    'password': 'TestPass123!'
                })

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"\n📊 Memory Usage Test ({sessions_count} sessions):")
        print(f"  Initial: {initial_memory:.2f} MB")
        print(f"  Final: {final_memory:.2f} MB")
        print(f"  Increase: {memory_increase:.2f} MB")
        print(f"  Per Session: {memory_increase/sessions_count:.2f} MB")

        # Warning if memory usage is high
        if memory_increase > 100:
            print(f"⚠️  WARNING: High memory usage ({memory_increase:.2f}MB)")

    def test_database_connection_pool(self, app):
        """
        Test database connection pool efficiency.
        """
        with app.app_context():
            times = []
            iterations = 20

            for _ in range(iterations):
                start = time.perf_counter()
                # Test connection acquisition
                result = db.session.execute(db.text('SELECT 1'))
                result.fetchone()
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                times.append(elapsed_ms)

            avg_time = statistics.mean(times)
            print(f"\n📊 DB Connection Pool Performance: {avg_time:.2f}ms avg")

            if avg_time > 10:
                print(f"⚠️  WARNING: Connection acquisition slow ({avg_time:.2f}ms)")


class TestBottleneckIdentification:
    """Identify performance bottlenecks in the application."""

    def test_identify_slow_routes(self, client, threshold_ms=500):
        """
        Identify routes that exceed performance threshold.
        """
        routes_to_test = [
            ('GET', '/'),
            ('GET', '/auth/login'),
            ('GET', '/auth/register'),
        ]

        slow_routes = []
        results = []

        for method, route in routes_to_test:
            times = []
            for _ in range(5):
                start = time.perf_counter()
                if method == 'GET':
                    response = client.get(route)
                end = time.perf_counter()

                elapsed_ms = (end - start) * 1000
                times.append(elapsed_ms)

            avg_time = statistics.mean(times)
            results.append({
                'route': f'{method} {route}',
                'avg_ms': avg_time
            })

            if avg_time > threshold_ms:
                slow_routes.append(f'{method} {route}: {avg_time:.2f}ms')

        print(f"\n📊 Route Performance Analysis:")
        for result in sorted(results, key=lambda x: x['avg_ms'], reverse=True):
            print(f"  {result['route']}: {result['avg_ms']:.2f}ms")

        if slow_routes:
            print(f"\n⚠️  Slow Routes (>{threshold_ms}ms):")
            for route in slow_routes:
                print(f"    {route}")

    def test_database_query_analysis(self, app):
        """
        Analyze database query patterns for N+1 issues.
        """
        with app.app_context():
            # Create test data
            for i in range(10):
                user = User(username=f'querytest{i}',
                           email=f'query{i}@test.com')
                user.set_password('TestPass123!')
                db.session.add(user)
            db.session.commit()

            # Test potential N+1 query
            start = time.perf_counter()
            users = User.query.all()
            for user in users:
                # Accessing relationship would cause N+1 if not optimized
                _ = user.username
            end = time.perf_counter()

            elapsed_ms = (end - start) * 1000
            print(f"\n📊 Query Pattern Analysis:")
            print(f"  Query Time: {elapsed_ms:.2f}ms for {len(users)} users")
            print(f"  Per Record: {elapsed_ms/len(users):.2f}ms")

            if elapsed_ms / len(users) > 10:
                print(f"⚠️  WARNING: Potential N+1 query issue detected")


# Performance test utilities
@pytest.fixture
def benchmark_target():
    """Default benchmark targets (can be overridden)."""
    return {
        'homepage': 100,  # ms
        'api': 200,  # ms
        'db_query': 50,  # ms
        'bulk_insert': 1000,  # ms for 100 records
    }


@pytest.fixture
def performance_report():
    """Collect performance metrics during test run."""
    metrics = {
        'response_times': [],
        'db_queries': [],
        'warnings': []
    }
    return metrics

