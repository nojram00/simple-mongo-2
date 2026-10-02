#!/usr/bin/env python3
"""
Basic usage examples for simple-mongo-2 library.
"""

from simple_mongo_2 import SimpleMongo

def basic_crud_examples():
    """Basic CRUD operations with simple-mongo-2."""
    
    print("=== Basic CRUD Operations ===")
    
    with SimpleMongo() as client:
        # Test connection
        if client.ping():
            print("✓ Connected to MongoDB")
        else:
            print("✗ Failed to connect to MongoDB")
            return
        
        # Get collection
        users = client.test_db.users
        
        # Clear existing data for demo
        users.delete_many({})
        print("Cleared existing users")
        
        # Insert documents
        alice_id = users.insert_one({
            "name": "Alice",
            "age": 28,
            "email": "alice@example.com",
            "status": "active"
        }).inserted_id
        
        bob_id = users.insert_one({
            "name": "Bob", 
            "age": 35,
            "email": "bob@example.com",
            "status": "active"
        }).inserted_id
        
        print(f"Inserted users with IDs: {alice_id}, {bob_id}")
        
        # Find operations
        print("\n=== Find Operations ===")
        
        # Find one
        alice = users.find_one({"name": "Alice"})
        print(f"Found Alice: {alice}")
        
        # Find many with cursor
        active_users = users.find({"status": "active"})
        print("Active users:")
        for user in active_users:
            print(f"  - {user.get('name')} (age: {user.get('age')})")
        
        # Find by ID
        user_by_id = users.find_one_by_id(alice_id)
        print(f"Found user by ID: {user_by_id.get('name')}")
        
        # Update operations
        print("\n=== Update Operations ===")
        
        update_result = users.update_one(
            {"name": "Alice"},
            {"$set": {"age": 29}}
        )
        print(f"Updated {update_result.modified_count} document(s)")
        
        # Verify update
        alice_updated = users.find_one({"name": "Alice"})
        print(f"Alice's age is now: {alice_updated.get('age')}")
        
        # Count documents
        print("\n=== Count Operations ===")
        active_count = users.count_documents({"status": "active"})
        print(f"Active users count: {active_count}")
        
        # Delete operations
        print("\n=== Delete Operations ===")
        delete_result = users.delete_one({"name": "Bob"})
        print(f"Deleted {delete_result.deleted_count} user(s)")
        
        # Final count
        final_count = users.count_documents({})
        print(f"Total users remaining: {final_count}")

def aggregation_examples():
    """Aggregation pipeline examples."""
    
    print("\n\n=== Aggregation Examples ===")
    
    with SimpleMongo() as client:
        # Get collection
        orders = client.test_db.orders
        
        # Clear existing data
        orders.delete_many({})
        
        # Insert sample orders
        orders.insert_many([
            {
                "order_id": "ORD001",
                "customer_id": "CUST001",
                "amount": 100.50,
                "status": "completed",
                "date": "2024-01-15",
                "items": ["Product A", "Product B"]
            },
            {
                "order_id": "ORD002",
                "customer_id": "CUST002",
                "amount": 250.75,
                "status": "completed", 
                "date": "2024-01-16",
                "items": ["Product C"]
            },
            {
                "order_id": "ORD003",
                "customer_id": "CUST001",
                "amount": 75.25,
                "status": "pending",
                "date": "2024-01-17",
                "items": ["Product A"]
            }
        ])
        
        print("Inserted sample orders")
        
        # Using AggregationFactory
        from simple_mongo_2 import AggregationFactory
        from simple_mongo_2.aggregation_pipeline import MatchStage, SortStage
        from typing import cast
        
        factory = orders.aggregation_factory
        
        # Simple aggregation
        print("\n--- Using AggregationFactory ---")
        results = (factory
            .match(cast(MatchStage, {"$match": {"status": "completed"}}))
            .sort(cast(SortStage, {"$sort": {"amount": -1}}))
            .execute()
        )
        
        print("Completed orders (sorted by amount descending):")
        for order in results:
            print(f"  - {order.get('order_id')}: ${order.get('amount')}")

def connection_configuration_examples():
    """Connection and configuration examples."""
    
    print("\n\n=== Connection Configuration Examples ===")
    
    # Custom URI
    print("Custom URI configuration:")
    client = SimpleMongo(uri="mongodb://localhost:27017")
    
    # With options
    print("With connection options:")
    client = SimpleMongo(
        uri="mongodb://localhost:27017",
        maxPoolSize=50,
        socketTimeoutMS=30000
    )
    
    # Using environment variable (from .env file)
    print("Using environment variable from .env file")
    # This will use MONGODB_URI from .env or default to localhost:27017

def escape_hatch_example():
    """Example of accessing underlying PyMongo objects."""
    
    print("\n\n=== Escape Hatch Example ===")
    
    with SimpleMongo() as client:
        # Get raw PyMongo objects
        raw_client = client.raw()
        raw_db = client.test_db.raw()
        raw_collection = client.test_db.users.raw()
        
        print("Accessing raw PyMongo objects:")
        print(f"  - Raw client type: {type(raw_client)}")
        print(f"  - Raw DB type: {type(raw_db)}")
        print(f"  - Raw collection type: {type(raw_collection)}")
        
        # You can now use any PyMongo method directly
        db_names = raw_client.list_database_names()
        print(f"Available databases: {db_names}")

if __name__ == "__main__":
    basic_crud_examples()
    aggregation_examples()
    connection_configuration_examples()
    escape_hatch_example()
    
    print("\n=== All examples completed ===")