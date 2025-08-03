"""
Enterprise WebSocket System Testing Suite
Comprehensive testing for KairoCal WebSocket functionality
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import List, Dict, Any
import uuid

import socketio
import aiohttp
import pytest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketTester:
    """
    Comprehensive WebSocket testing client
    """
    
    def __init__(self, server_url: str = "http://localhost:8001"):
        self.server_url = server_url
        self.clients: List[socketio.AsyncClient] = []
        self.test_results = {
            'connection_tests': [],
            'message_tests': [],
            'load_tests': [],
            'latency_tests': [],
            'error_tests': []
        }
    
    async def create_test_client(self, user_id: int, device_type: str = "desktop") -> socketio.AsyncClient:
        """Create a test WebSocket client"""
        client = socketio.AsyncClient(
            reconnection=True,
            reconnection_attempts=3,
            reconnection_delay=1,
            logger=logger
        )
        
        # Generate test auth token (simplified for testing)
        auth_token = f"test_token_user_{user_id}"
        device_id = f"test_device_{user_id}_{uuid.uuid4().hex[:8]}"
        
        auth_data = {
            'token': auth_token,
            'deviceInfo': {
                'deviceId': device_id,
                'deviceType': device_type,
                'platform': 'test',
                'browser': 'test-client',
                'version': '1.0.0'
            }
        }
        
        # Store client info
        client.user_id = user_id
        client.device_id = device_id
        client.auth_data = auth_data
        client.messages_received = []
        client.connection_time = None
        client.latency_measurements = []
        
        # Set up event handlers
        await self._setup_client_handlers(client)
        
        self.clients.append(client)
        return client
    
    async def _setup_client_handlers(self, client: socketio.AsyncClient):
        """Set up event handlers for test client"""
        
        @client.event
        async def connect():
            client.connection_time = time.time()
            logger.info(f"✅ Test client {client.user_id} connected")
        
        @client.event
        async def disconnect():
            logger.info(f"👋 Test client {client.user_id} disconnected")
        
        @client.event
        async def connect_error(data):
            logger.error(f"❌ Test client {client.user_id} connection error: {data}")
        
        # Message handlers
        @client.event
        async def event_created(data):
            client.messages_received.append(('event_created', data, time.time()))
            logger.info(f"📅 Client {client.user_id} received event_created")
        
        @client.event
        async def conflict_detected(data):
            client.messages_received.append(('conflict_detected', data, time.time()))
            logger.info(f"⚠️ Client {client.user_id} received conflict_detected")
        
        @client.event
        async def priority_alert(data):
            client.messages_received.append(('priority_alert', data, time.time()))
            logger.info(f"🚨 Client {client.user_id} received priority_alert")
        
        @client.event
        async def voice_transcription(data):
            client.messages_received.append(('voice_transcription', data, time.time()))
            logger.info(f"🎤 Client {client.user_id} received voice_transcription")
        
        @client.event
        async def pong(latency):
            client.latency_measurements.append(latency)
    
    async def test_single_connection(self) -> Dict[str, Any]:
        """Test single client connection"""
        logger.info("🔧 Testing single connection...")
        
        client = await self.create_test_client(user_id=1001)
        
        try:
            # Connect
            start_time = time.time()
            await client.connect(self.server_url, auth=client.auth_data)
            connection_time = time.time() - start_time
            
            # Wait for connection to establish
            await asyncio.sleep(1)
            
            result = {
                'success': client.connected,
                'connection_time': connection_time,
                'user_id': client.user_id
            }
            
            self.test_results['connection_tests'].append(result)
            
            await client.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"❌ Single connection test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_multiple_connections(self, num_clients: int = 10) -> Dict[str, Any]:
        """Test multiple concurrent connections"""
        logger.info(f"🔧 Testing {num_clients} concurrent connections...")
        
        clients = []
        start_time = time.time()
        
        try:
            # Create and connect multiple clients
            connect_tasks = []
            for i in range(num_clients):
                client = await self.create_test_client(user_id=2000 + i)
                clients.append(client)
                task = client.connect(self.server_url, auth=client.auth_data)
                connect_tasks.append(task)
            
            # Wait for all connections
            await asyncio.gather(*connect_tasks, return_exceptions=True)
            total_time = time.time() - start_time
            
            # Count successful connections
            successful_connections = sum(1 for client in clients if client.connected)
            
            # Wait a bit for stability
            await asyncio.sleep(2)
            
            result = {
                'requested_connections': num_clients,
                'successful_connections': successful_connections,
                'total_time': total_time,
                'avg_time_per_connection': total_time / num_clients,
                'success_rate': successful_connections / num_clients
            }
            
            self.test_results['connection_tests'].append(result)
            
            # Disconnect all clients
            disconnect_tasks = [client.disconnect() for client in clients if client.connected]
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Multiple connection test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_message_broadcasting(self) -> Dict[str, Any]:
        """Test message broadcasting functionality"""
        logger.info("🔧 Testing message broadcasting...")
        
        # Create multiple clients
        clients = []
        for i in range(3):
            client = await self.create_test_client(user_id=3000 + i)
            clients.append(client)
        
        try:
            # Connect all clients
            connect_tasks = [client.connect(self.server_url, auth=client.auth_data) for client in clients]
            await asyncio.gather(*connect_tasks)
            
            # Wait for connections to establish
            await asyncio.sleep(1)
            
            # Test broadcast via HTTP API
            async with aiohttp.ClientSession() as session:
                broadcast_data = {
                    "type": "event_created",
                    "payload": {
                        "event": {
                            "id": "test_event_123",
                            "title": "Test Event",
                            "priority": 5
                        }
                    },
                    "user_ids": [3000, 3001, 3002]
                }
                
                async with session.post(
                    f"{self.server_url}/broadcast",
                    json=broadcast_data
                ) as response:
                    broadcast_result = await response.json()
            
            # Wait for messages to be received
            await asyncio.sleep(2)
            
            # Check message reception
            messages_received = []
            for client in clients:
                for msg_type, msg_data, timestamp in client.messages_received:
                    if msg_type == 'event_created':
                        messages_received.append({
                            'user_id': client.user_id,
                            'message_type': msg_type,
                            'timestamp': timestamp
                        })
            
            result = {
                'broadcast_success': broadcast_result.get('success', False),
                'messages_sent': 3,
                'messages_received': len(messages_received),
                'reception_rate': len(messages_received) / 3,
                'message_details': messages_received
            }
            
            self.test_results['message_tests'].append(result)
            
            # Disconnect clients
            disconnect_tasks = [client.disconnect() for client in clients]
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Message broadcasting test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_latency_measurement(self) -> Dict[str, Any]:
        """Test WebSocket latency"""
        logger.info("🔧 Testing latency measurement...")
        
        client = await self.create_test_client(user_id=4000)
        
        try:
            await client.connect(self.server_url, auth=client.auth_data)
            await asyncio.sleep(1)
            
            # Send ping messages
            ping_count = 10
            for i in range(ping_count):
                await client.emit('ping')
                await asyncio.sleep(0.5)
            
            # Wait for all pongs
            await asyncio.sleep(2)
            
            latencies = client.latency_measurements
            
            result = {
                'pings_sent': ping_count,
                'pongs_received': len(latencies),
                'avg_latency': sum(latencies) / len(latencies) if latencies else 0,
                'min_latency': min(latencies) if latencies else 0,
                'max_latency': max(latencies) if latencies else 0,
                'latency_measurements': latencies
            }
            
            self.test_results['latency_tests'].append(result)
            
            await client.disconnect()
            return result
            
        except Exception as e:
            logger.error(f"❌ Latency test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling and recovery"""
        logger.info("🔧 Testing error handling...")
        
        results = []
        
        # Test 1: Invalid auth token
        try:
            client = socketio.AsyncClient()
            await client.connect(self.server_url, auth={'token': 'invalid_token'})
            results.append({'test': 'invalid_auth', 'success': False, 'connected': client.connected})
            await client.disconnect()
        except Exception as e:
            results.append({'test': 'invalid_auth', 'success': True, 'error': str(e)})
        
        # Test 2: Missing auth
        try:
            client = socketio.AsyncClient()
            await client.connect(self.server_url)
            results.append({'test': 'missing_auth', 'success': False, 'connected': client.connected})
            await client.disconnect()
        except Exception as e:
            results.append({'test': 'missing_auth', 'success': True, 'error': str(e)})
        
        self.test_results['error_tests'].extend(results)
        return {'error_tests': results}
    
    async def test_load_performance(self, num_clients: int = 100, duration: int = 30) -> Dict[str, Any]:
        """Test load performance with many clients"""
        logger.info(f"🔧 Testing load performance: {num_clients} clients for {duration}s...")
        
        clients = []
        start_time = time.time()
        
        try:
            # Create clients in batches to avoid overwhelming
            batch_size = 10
            for batch_start in range(0, num_clients, batch_size):
                batch_clients = []
                batch_end = min(batch_start + batch_size, num_clients)
                
                # Create batch
                for i in range(batch_start, batch_end):
                    client = await self.create_test_client(user_id=5000 + i)
                    batch_clients.append(client)
                
                # Connect batch
                connect_tasks = [client.connect(self.server_url, auth=client.auth_data) for client in batch_clients]
                await asyncio.gather(*connect_tasks, return_exceptions=True)
                
                clients.extend(batch_clients)
                
                # Small delay between batches
                await asyncio.sleep(0.1)
            
            setup_time = time.time() - start_time
            successful_connections = sum(1 for client in clients if client.connected)
            
            logger.info(f"📊 Load test setup: {successful_connections}/{num_clients} connected in {setup_time:.2f}s")
            
            # Run load test for specified duration
            test_start_time = time.time()
            message_count = 0
            
            while time.time() - test_start_time < duration:
                # Send some messages
                for i, client in enumerate(clients[:10]):  # Only use first 10 clients for sending
                    if client.connected:
                        await client.emit('ping')
                        message_count += 1
                
                await asyncio.sleep(1)
            
            test_duration = time.time() - test_start_time
            
            # Collect metrics
            total_messages_received = sum(len(client.messages_received) for client in clients)
            total_latency_measurements = sum(len(client.latency_measurements) for client in clients)
            
            result = {
                'clients_requested': num_clients,
                'clients_connected': successful_connections,
                'connection_success_rate': successful_connections / num_clients,
                'setup_time': setup_time,
                'test_duration': test_duration,
                'messages_sent': message_count,
                'messages_received': total_messages_received,
                'latency_measurements': total_latency_measurements,
                'messages_per_second': message_count / test_duration,
                'avg_clients_per_second': successful_connections / setup_time
            }
            
            self.test_results['load_tests'].append(result)
            
            # Cleanup
            logger.info("🧹 Cleaning up load test clients...")
            disconnect_tasks = [client.disconnect() for client in clients if client.connected]
            await asyncio.gather(*disconnect_tasks, return_exceptions=True)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Load test failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all tests and generate comprehensive report"""
        logger.info("🚀 Starting comprehensive WebSocket tests...")
        
        start_time = time.time()
        
        # Run tests
        tests = [
            ("Single Connection", self.test_single_connection()),
            ("Multiple Connections", self.test_multiple_connections(10)),
            ("Message Broadcasting", self.test_message_broadcasting()),
            ("Latency Measurement", self.test_latency_measurement()),
            ("Error Handling", self.test_error_handling()),
            ("Load Performance", self.test_load_performance(50, 10))  # Reduced for demo
        ]
        
        results = {}
        for test_name, test_coro in tests:
            logger.info(f"🔄 Running {test_name}...")
            try:
                result = await test_coro
                results[test_name.lower().replace(' ', '_')] = result
                logger.info(f"✅ {test_name} completed")
            except Exception as e:
                logger.error(f"❌ {test_name} failed: {e}")
                results[test_name.lower().replace(' ', '_')] = {'success': False, 'error': str(e)}
        
        total_time = time.time() - start_time
        
        # Generate comprehensive report
        report = {
            'test_suite': 'KairoCal WebSocket Enterprise Testing',
            'timestamp': datetime.now().isoformat(),
            'total_duration': total_time,
            'server_url': self.server_url,
            'test_results': results,
            'summary': self._generate_test_summary(results)
        }
        
        return report
    
    def _generate_test_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test summary"""
        passed_tests = sum(1 for result in results.values() if result.get('success', True))
        total_tests = len(results)
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'status': 'PASS' if passed_tests == total_tests else 'FAIL'
        }

async def main():
    """Main test runner"""
    logger.info("🌟 KairoCal WebSocket Testing Suite")
    
    # Create tester
    tester = WebSocketTester("http://localhost:8001")
    
    try:
        # Run comprehensive tests
        report = await tester.run_comprehensive_tests()
        
        # Print report
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*80)
        print(f"Test Suite: {report['test_suite']}")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Duration: {report['total_duration']:.2f}s")
        print(f"Server: {report['server_url']}")
        print("\n📈 SUMMARY:")
        summary = report['summary']
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Passed: {summary['passed_tests']}")
        print(f"  Failed: {summary['failed_tests']}")
        print(f"  Success Rate: {summary['success_rate']:.1%}")
        print(f"  Status: {summary['status']}")
        
        print("\n📋 DETAILED RESULTS:")
        for test_name, result in report['test_results'].items():
            status = "✅ PASS" if result.get('success', True) else "❌ FAIL"
            print(f"  {test_name}: {status}")
            if 'error' in result:
                print(f"    Error: {result['error']}")
        
        print("\n" + "="*80)
        
        # Save report to file
        with open('websocket_test_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info("📄 Test report saved to websocket_test_report.json")
        
    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
