#!/usr/bin/env python3
"""
Advanced aggregation examples demonstrating the full power of simple-mongo-2.
"""

from simple_mongo_2 import SimpleMongo, AggregationFactory, PipelineBuilder
from simple_mongo_2.aggregation_pipeline import *
from typing import cast

def complex_aggregation_example():
    """Demonstrate complex aggregation pipelines with multiple stages."""
    
    print("=== Complex Aggregation Example ===")
    
    with SimpleMongo() as client:
        # Setup: Create sample e-commerce data
        orders = client.ecommerce.orders
        products = client.ecommerce.products
        customers = client.ecommerce.customers
        
        # Clear existing data
        orders.delete_many({})
        products.delete_many({})
        customers.delete_many({})
        
        # Insert sample products
        products.insert_many([
            {"_id": "PROD001", "name": "Laptop", "category": "Electronics", "price": 999.99},
            {"_id": "PROD002", "name": "Mouse", "category": "Electronics", "price": 29.99},
            {"_id": "PROD003", "name": "Book", "category": "Books", "price": 19.99},
            {"_id": "PROD004", "name": "Shirt", "category": "Clothing", "price": 49.99},
        ])
        
        # Insert sample customers
        customers.insert_many([
            {"_id": "CUST001", "name": "John Doe", "country": "USA", "tier": "premium"},
            {"_id": "CUST002", "name": "Jane Smith", "country": "UK", "tier": "standard"},
            {"_id": "CUST003", "name": "Bob Johnson", "country": "USA", "tier": "premium"},
            {"_id": "CUST004", "name": "Alice Brown", "country": "Canada", "tier": "standard"},
        ])
        
        # Insert sample orders
        orders.insert_many([
            {
                "order_id": "ORD001",
                "customer_id": "CUST001",
                "product_ids": ["PROD001", "PROD002"],
                "amount": 1029.98,
                "status": "completed",
                "date": "2024-01-15",
                "discount_applied": 0.10
            },
            {
                "order_id": "ORD002",
                "customer_id": "CUST002",
                "product_ids": ["PROD003"],
                "amount": 19.99,
                "status": "completed",
                "date": "2024-01-16",
                "discount_applied": 0.05
            },
            {
                "order_id": "ORD003",
                "customer_id": "CUST001",
                "product_ids": ["PROD004"],
                "amount": 49.99,
                "status": "pending",
                "date": "2024-01-17",
                "discount_applied": 0.00
            },
            {
                "order_id": "ORD004",
                "customer_id": "CUST003",
                "product_ids": ["PROD001", "PROD003"],
                "amount": 1019.98,
                "status": "completed",
                "date": "2024-01-18",
                "discount_applied": 0.15
            },
        ])
        
        print("Sample data inserted")
        
        # Example 1: Multi-stage aggregation with AggregationFactory
        print("\n--- Example 1: Multi-stage Aggregation with AggregationFactory ---")
        
        factory = orders.aggregation_factory
        
        results = (factory
            .match(cast(MatchStage, {"$match": {"status": "completed"}}))
            .lookup(cast(LookupStage, {
                "$lookup": {
                    "from": "customers",
                    "localField": "customer_id",
                    "foreignField": "_id",
                    "as": "customer_info"
                }
            }))
            .unwind(cast(UnwindStage, {"$unwind": "$customer_info"}))
            .add_fields(cast(AddFieldsStage, {
                "$addFields": {
                    "final_amount": {
                        "$multiply": ["$amount", {"$subtract": [1, "$discount_applied"]}]
                    }
                }
            }))
            .group(cast(GroupStage, {
                "$group": {
                    "_id": "$customer_info.country",
                    "total_sales": {"$sum": "$final_amount"},
                    "average_order_value": {"$avg": "$final_amount"},
                    "order_count": {"$count": {}},
                    "customers": {"$addToSet": "$customer_info.name"}
                }
            }))
            .sort(cast(SortStage, {"$sort": {"total_sales": -1}}))
            .project(cast(ProjectStage, {
                "$project": {
                    "_id": 0,
                    "country": "$_id",
                    "total_sales": 1,
                    "average_order_value": 1,
                    "order_count": 1,
                    "customer_count": {"$size": "$customers"}
                }
            }))
            .execute()
        )
        
        print("Sales by country:")
        for result in results:
            print(f"  {result['country']}:")
            print(f"    Total sales: ${result['total_sales']:.2f}")
            print(f"    Avg order: ${result['average_order_value']:.2f}")
            print(f"    Orders: {result['order_count']}")
            print(f"    Customers: {result['customer_count']}")
        
        # Example 2: Using direct pipeline building with PipelineBuilder
        print("\n--- Example 2: Direct Pipeline Building with PipelineBuilder ---")
        
        pipeline = PipelineBuilder.create(
            cast(MatchStage, {"$match": {"status": "completed"}}),
            cast(UnwindStage, {"$unwind": "$product_ids"}),
            cast(LookupStage, {
                "$lookup": {
                    "from": "products",
                    "localField": "product_ids",
                    "foreignField": "_id",
                    "as": "product_info"
                }
            }),
            cast(UnwindStage, {"$unwind": "$product_info"}),
            cast(GroupStage, {
                "$group": {
                    "_id": "$product_info.category",
                    "total_revenue": {"$sum": "$amount"},
                    "product_count": {"$sum": 1},
                    "avg_price": {"$avg": "$product_info.price"},
                    "products": {"$addToSet": "$product_info.name"}
                }
            }),
            cast(ProjectStage, {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "total_revenue": 1,
                    "product_count": 1,
                    "avg_price": 1,
                    "unique_products": {"$size": "$products"}
                }
            }),
            cast(SortStage, {"$sort": {"total_revenue": -1}})
        )
        
        results = orders.aggregate(pipeline)
        
        print("Revenue by product category:")
        for result in results:
            print(f"  {result['category']}:")
            print(f"    Revenue: ${result['total_revenue']:.2f}")
            print(f"    Products sold: {result['product_count']}")
            print(f"    Avg product price: ${result['avg_price']:.2f}")
            print(f"    Unique products: {result['unique_products']}")
        
        # Example 3: Time-based analysis with date operations
        print("\n--- Example 3: Time-based Analysis ---")
        
        # Note: This example assumes date strings for simplicity
        # In real usage, you'd use proper Date objects
        
        # Example 4: Advanced filtering with multiple conditions
        print("\n--- Example 4: Advanced Filtering ---")
        
        results = orders.aggregate([
            cast(MatchStage, {
                "$match": {
                    "status": "completed",
                    "amount": {"$gt": 50},
                    "discount_applied": {"$gt": 0}
                }
            }),
            cast(SortStage, {"$sort": {"amount": -1}}),
            cast(ProjectStage, {
                "$project": {
                    "_id": 0,
                    "order_id": 1,
                    "amount": 1,
                    "discount_applied": 1,
                    "discounted_amount": {
                        "$multiply": ["$amount", {"$subtract": [1, "$discount_applied"]}]
                    }
                }
            })
        ])
        
        print("High-value discounted orders:")
        for result in results:
            print(f"  {result['order_id']}:")
            print(f"    Original: ${result['amount']:.2f}")
            print(f"    Discount: {result['discount_applied']*100:.0f}%")
            print(f"    Final: ${result['discounted_amount']:.2f}")

def type_safety_demo():
    """Demonstrate the type safety features of the library."""
    
    print("\n\n=== Type Safety Demonstration ===")
    
    # The following would be caught by static type checkers:
    # 1. Invalid field names in aggregation stages
    # 2. Missing required stage properties
    # 3. Incorrect data types for stage parameters
    
    # Correct usage (type-safe)
    from typing import cast
    
    # This is type-safe and will pass mypy/type checkers
    match_stage: MatchStage = cast(MatchStage, {"$match": {"status": "active"}})
    sort_stage: SortStage = cast(SortStage, {"$sort": {"name": 1}})
    
    # Example of what would fail type checking:
    # match_stage: MatchStage = {"$match": "invalid"}  # Wrong type for $match value
    # match_stage: MatchStage = {"match": {"status": "active"}}  # Wrong key name
    # sort_stage: SortStage = {"$sort": {"name": "asc"}}  # Wrong type for sort value
    
    print("Type safety examples demonstrated:")
    print("  - Static type checking prevents incorrect aggregation stage structures")
    print("  - TypedDict ensures proper field names and data types")
    print("  - Cast function helps type inference")

def performance_comparison():
    """Demonstrate performance patterns and best practices."""
    
    print("\n\n=== Performance Best Practices ===")
    
    with SimpleMongo() as client:
        # Setup large dataset for demonstration
        test_collection = client.test_db.performance_test
        
        # Clear existing data
        test_collection.delete_many({})
        
        # Create large dataset
        batch_size = 1000
        total_docs = 10000
        
        print(f"Creating {total_docs} documents...")
        
        documents = []
        for i in range(total_docs):
            documents.append({
                "index": i,
                "value": i * 1.5,
                "category": f"cat_{i % 10}",
                "timestamp": f"2024-01-{i % 28 + 1:02d}",
                "metadata": {"source": f"source_{i % 5}", "processed": i % 2 == 0}
            })
            
            # Insert in batches for better performance
            if len(documents) >= batch_size:
                test_collection.insert_many(documents)
                documents = []
        
        if documents:
            test_collection.insert_many(documents)
        
        print(f"Inserted {total_docs} documents")
        
        # Performance comparison: Batch vs individual operations
        print("\nPerformance considerations:")
        print("  1. Use insert_many() instead of insert_one() in loops")
        print("  2. Use aggregation pipelines for complex data processing")
        print("  3. Create appropriate indexes for frequent queries")
        print("  4. Use projection to limit returned fields")
        print("  5. Leverage MongoDB's built-in aggregation optimizations")

if __name__ == "__main__":
    complex_aggregation_example()
    type_safety_demo()
    performance_comparison()
    
    print("\n=== Advanced examples completed ===")
    print("\nKey takeaways:")
    print("  - simple-mongo-2 provides type-safe MongoDB operations")
    print("  - Fluent aggregation builder for complex pipelines")
    print("  - Direct access to PyMongo when needed")
    print("  - Environment-based configuration")
    print("  - Comprehensive error handling")