# simple-mongo-2

A modern, type-safe MongoDB client library for Python with intuitive chaining syntax and comprehensive aggregation pipeline support.

## Features

- **Type-safe MongoDB operations**: Full static type checking support
- **Intuitive chaining syntax**: Access databases and collections with dot notation
- **Comprehensive aggregation support**: Type-safe aggregation pipeline stages
- **Modern Python**: Built with Python 3.14+, using TypedDict for type safety
- **Environment configuration**: Easy configuration via `.env` files
- **Escape hatches**: Access underlying PyMongo objects when needed

## Installation

```bash
pip install simple-mongo-2
```

Or using uv:

```bash
uv add simple-mongo-2
```

## Quick Start

### Basic Connection

```python
from simple_mongo_2 import SimpleMongo

# Connect to MongoDB (defaults to MONGODB_URI environment variable or localhost:27017)
with SimpleMongo() as client:
    # Test connection
    client.ping()
    
    # Access database and collection using dot notation
    users = client.test_db.users
    
    # Insert a document
    result = users.insert_one({
        "name": "John",
        "age": 25,
        "email": "john@example.com"
    })
    
    # Find a document
    user = users.find_one({"name": "John"})
    print(user)
```

### Environment Configuration

Create a `.env` file in your project root:

```env
MONGODB_URI=mongodb://username:password@localhost:27017/your-database
```

Or configure programmatically:

```python
client = SimpleMongo(uri="mongodb://username:password@host:port/database")
```

## Core Concepts

### Client Wrapper

The `SimpleMongo` class (imported as `Client` in code) provides a high-level wrapper around PyMongo's `MongoClient`:

```python
from simple_mongo_2 import SimpleMongo

client = SimpleMongo()

# Access databases
db = client.my_database

# Access collections
collection = db.my_collection
# or with explicit method
collection = client.database("my_database").collection("my_collection")
```

### Database and Collection Wrappers

The library provides `DatabaseWrapper` and `CollectionWrapper` classes that wrap PyMongo objects:

```python
# Collection operations
users = client.test_db.users

# Find operations
users.find_one({"name": "John"})
users.find({"age": {"$gte": 18}})

# Insert operations
users.insert_one({"name": "Alice", "age": 30})
users.insert_many([
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
])

# Update operations
users.update_one({"name": "Alice"}, {"$set": {"age": 31}})
users.update_many({"age": {"$lt": 30}}, {"$inc": {"age": 1}})

# Delete operations
users.delete_one({"name": "Bob"})
users.delete_many({"age": {"$gte": 40}})

# Count documents
count = users.count_documents({"status": "active"})
```

### Type-Safe Aggregation

#### Using AggregationFactory

The `AggregationFactory` provides a fluent interface for building aggregation pipelines:

```python
from simple_mongo_2 import SimpleMongo, AggregationFactory
from simple_mongo_2.aggregation_pipeline import MatchStage, SortStage, ProjectStage
from typing import cast

client = SimpleMongo()
users = client.test_db.users

# Get aggregation factory from collection
factory = users.aggregation_factory

# Build and execute pipeline
results = (factory
    .match(cast(MatchStage, {"$match": {"status": "active"}}))
    .sort(cast(SortStage, {"$sort": {"created_at": -1}}))
    .limit(cast(LimitStage, {"$limit": 10}))
    .project(cast(ProjectStage, {"$project": {"_id": 0, "name": 1, "email": 1}}))
    .execute()
)

for result in results:
    print(result)
```

#### Direct Pipeline Building

You can also build pipelines directly:

```python
from simple_mongo_2 import AggregationPipeline, AggregationStage
from simple_mongo_2.aggregation_pipeline import MatchStage, SortStage
from typing import cast

# Build pipeline
pipeline: AggregationPipeline = [
    cast(MatchStage, {"$match": {"age": {"$gte": 18}}}),
    cast(SortStage, {"$sort": {"name": 1}}),
]

# Execute with collection
results = users.aggregate(pipeline)
```

#### Using PipelineBuilder

The `PipelineBuilder` provides another way to construct pipelines:

```python
from simple_mongo_2 import PipelineBuilder
from simple_mongo_2.aggregation_pipeline import MatchStage, SortStage, ProjectStage
from typing import cast

# Create a pipeline
pipeline = PipelineBuilder.create(
    cast(MatchStage, {"$match": {"status": "active"}}),
    cast(SortStage, {"$sort": {"created_at": -1}}),
    cast(ProjectStage, {"$project": {"_id": 0, "name": 1}})
)

# Execute
results = users.aggregate(pipeline)
```

### Available Aggregation Stages

The library supports all MongoDB aggregation stages with type-safe definitions:

- **Query Stages**: `$match`, `$sort`, `$limit`, `$skip`, `$project`
- **Grouping Stages**: `$group`, `$unwind`, `$bucket`, `$bucketAuto`, `$sortByCount`
- **Join Stages**: `$lookup`, `$graphLookup`
- **Field Modification**: `$addFields`, `$set`, `$unset`, `$replaceRoot`, `$replaceWith`
- **Search Stages**: `$search`, `$vectorSearch`, `$searchMeta`
- **Statistical Stages**: `$facet`, `$count`, `$sample`
- **Time Series**: `$densify`, `$fill`
- **Geospatial**: `$geoNear`
- **Window Operations**: `$setWindowFields`
- **Collection Operations**: `$merge`, `$out`, `$unionWith`
- **System Stages**: `$collStats`, `$indexStats`, `$planCacheStats`

## Advanced Usage

### Accessing Underlying PyMongo Objects

When you need direct access to PyMongo functionality:

```python
# Get raw PyMongo objects
raw_client = client.raw()           # MongoClient
raw_db = client.test_db.raw()       # Database
raw_collection = users.raw()        # Collection
```

### Context Manager

The client supports context manager syntax for automatic cleanup:

```python
with SimpleMongo() as client:
    # Use client
    users = client.test_db.users
    # ...
# Client automatically closed when exiting the context
```

### Connection Pooling and Configuration

```python
# Custom connection options
client = SimpleMongo(
    uri="mongodb://localhost:27017",
    maxPoolSize=50,
    minPoolSize=10,
    connectTimeoutMS=30000,
    socketTimeoutMS=30000
)
```

## Type Safety

The library uses Python's `TypedDict` to provide type hints for all MongoDB operations:

```python
from typing import cast
from simple_mongo_2.aggregation_pipeline import MatchStage

# Type-safe stage definition
match_stage: MatchStage = cast(MatchStage, {"$match": {"age": {"$gte": 18}}})
# Type checker will catch incorrect field names or operators
```

## Error Handling

```python
from pymongo.errors import PyMongoError

try:
    with SimpleMongo() as client:
        # Test connection
        if not client.ping():
            print("MongoDB not reachable")
        
        # Your operations...
        users = client.test_db.users
        
except PyMongoError as e:
    print(f"MongoDB error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

## Examples

### Complex Aggregation Pipeline

```python
from simple_mongo_2 import SimpleMongo
from simple_mongo_2.aggregation_pipeline import *
from typing import cast

client = SimpleMongo()
orders = client.ecommerce.orders

# Complex pipeline with multiple stages
results = orders.aggregate([
    cast(MatchStage, {"$match": {"status": "completed", "date": {"$gte": "2024-01-01"}}}),
    cast(LookupStage, {
        "$lookup": {
            "from": "customers",
            "localField": "customer_id",
            "foreignField": "_id",
            "as": "customer_info"
        }
    }),
    cast(UnwindStage, {"$unwind": "$customer_info"}),
    cast(GroupStage, {
        "$group": {
            "_id": "$customer_info.country",
            "total_sales": {"$sum": "$amount"},
            "average_order": {"$avg": "$amount"},
            "order_count": {"$count": {}}
        }
    }),
    cast(SortStage, {"$sort": {"total_sales": -1}}),
    cast(ProjectStage, {
        "$project": {
            "_id": 0,
            "country": "$_id",
            "total_sales": 1,
            "average_order": 1,
            "order_count": 1
        }
    })
])

for result in results:
    print(result)
```

### Batch Operations

```python
from simple_mongo_2 import SimpleMongo

client = SimpleMongo()
products = client.inventory.products

# Bulk insert
new_products = [
    {"name": "Product A", "category": "Electronics", "price": 99.99, "stock": 50},
    {"name": "Product B", "category": "Books", "price": 19.99, "stock": 100},
    {"name": "Product C", "category": "Clothing", "price": 49.99, "stock": 75}
]

result = products.insert_many(new_products)
print(f"Inserted {len(result.inserted_ids)} products")

# Bulk update
update_result = products.update_many(
    {"category": "Electronics"},
    {"$inc": {"price": 5.00}}
)
print(f"Updated {update_result.modified_count} electronics products")
```

## Project Structure

```
simple_mongo_2/
├── __init__.py              # Main exports
├── db.py                    # Client, Database, Collection wrappers
├── aggregation_pipeline.py  # Type definitions for aggregation stages
├── aggregation_factory.py   # Fluent aggregation builder
└── aggregation_pipeline_builder.py  # Pipeline builder utility
```

## Dependencies

- **pymongo>=4.18.2**: MongoDB driver
- **python-dotenv>=0.9.9**: Environment variable management
- **Python>=3.14**: Required for TypedDict features

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd simple-mongo-2

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black isort mypy
```

### Running Tests

```bash
pytest tests/ --cov=simple_mongo_2 --cov-report=html
```

### Type Checking

```bash
mypy src/simple_mongo_2
```

### Code Formatting

```bash
black src/simple_mongo_2
isort src/simple_mongo_2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and type checking succeeds
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

## Acknowledgments

- Built on top of the excellent [PyMongo](https://pymongo.readthedocs.io/) library
- Inspired by modern type-safe database clients in other languages
- Thanks to all contributors and users