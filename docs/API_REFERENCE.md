# API Reference

This document provides a comprehensive reference for the simple-mongo-2 library API.

## Table of Contents

- [SimpleMongo (Client)](#simplemongo-client)
- [DatabaseWrapper](#databasewrapper)
- [CollectionWrapper](#collectionwrapper)
- [AggregationFactory](#aggregationfactory)
- [Aggregation Stages](#aggregation-stages)
- [PipelineBuilder](#pipelinebuilder)

---

## SimpleMongo (Client)

The main client class for connecting to MongoDB.

### Class: `SimpleMongo`

**Alias:** `Client` (in source code)

#### Constructor

```python
SimpleMongo(
    uri: str = MONGODB_URI,
    **kwargs: Any
) -> None
```

**Parameters:**
- `uri` (str, optional): MongoDB connection URI. Defaults to `MONGODB_URI` environment variable or `"mongodb://localhost:27017"`.
- `**kwargs`: Additional options passed directly to PyMongo `MongoClient`.

#### Methods

##### `ping() -> bool`
Check whether MongoDB is reachable.

**Returns:**
- `bool`: `True` if MongoDB responds successfully.

**Raises:**
- `pymongo.errors.PyMongoError`: If the connection fails.

##### `close() -> None`
Close the MongoDB client connection.

##### `raw() -> MongoClient[Any]`
Return the underlying PyMongo `MongoClient`.

##### `database(name: str) -> DatabaseWrapper`
Explicitly access a database by name.

**Parameters:**
- `name` (str): Database name.

**Returns:**
- `DatabaseWrapper`: Database wrapper instance.

#### Properties

##### Attribute Access (`client.<database_name>`)
Access databases using dot notation.

**Example:**
```python
db = client.my_database  # Returns DatabaseWrapper
```

#### Context Manager Support

```python
with SimpleMongo() as client:
    # Use client
    pass
# Client automatically closed
```

---

## DatabaseWrapper

Wrapper around PyMongo Database for convenient collection access.

### Class: `DatabaseWrapper`

#### Constructor

```python
DatabaseWrapper(database: Database[Any]) -> None
```

**Parameters:**
- `database`: Underlying PyMongo Database.

#### Methods

##### `collection(name: str) -> CollectionWrapper`
Explicitly access a collection by name.

**Parameters:**
- `name` (str): Collection name.

**Returns:**
- `CollectionWrapper`: Collection wrapper instance.

##### `raw() -> Database[Any]`
Return the underlying PyMongo Database.

#### Properties

##### Attribute Access (`db.<collection_name>`)
Access collections using dot notation.

**Example:**
```python
collection = db.users  # Returns CollectionWrapper
```

---

## CollectionWrapper

Wrapper around PyMongo Collection providing convenient interface for MongoDB operations.

### Class: `CollectionWrapper`

#### Constructor

```python
CollectionWrapper(collection: Collection[Any]) -> None
```

**Parameters:**
- `collection`: Underlying PyMongo Collection.

#### Query Methods

##### `find(filter: Optional[Mapping[str, Any]] = None, projection: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> Cursor[Any]`
Find multiple documents.

**Parameters:**
- `filter` (optional): Query filter document.
- `projection` (optional): Projection specification.
- `**kwargs`: Additional arguments passed to PyMongo `find`.

**Returns:**
- `Cursor[Any]`: PyMongo Cursor for further chaining.

##### `find_one(filter: Optional[Mapping[str, Any]] = None, projection: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> Optional[Document]`
Find a single document.

**Returns:**
- `Document` or `None`: Matching document or `None` if not found.

##### `find_one_by_id(document_id: ObjectId | str) -> Optional[Document]`
Find a document by its MongoDB `_id`.

**Parameters:**
- `document_id`: MongoDB ObjectId or its string representation.

#### Insert Methods

##### `insert_one(document: Document, **kwargs: Any) -> InsertOneResult`
Insert a single document.

##### `insert_many(documents: Sequence[Document], **kwargs: Any) -> InsertManyResult`
Insert multiple documents.

#### Update Methods

##### `update_one(filter: Mapping[str, Any], update: Mapping[str, Any], **kwargs: Any) -> UpdateResult`
Update a single document.

##### `update_many(filter: Mapping[str, Any], update: Mapping[str, Any], **kwargs: Any) -> UpdateResult`
Update multiple documents.

#### Delete Methods

##### `delete_one(filter: Mapping[str, Any], **kwargs: Any) -> DeleteResult`
Delete a single document.

##### `delete_many(filter: Mapping[str, Any], **kwargs: Any) -> DeleteResult`
Delete multiple documents.

#### Count Method

##### `count_documents(filter: Mapping[str, Any], **kwargs: Any) -> int`
Count documents matching a filter.

#### Aggregation Methods

##### `aggregate(pipeline: AggregationPipeline)`
Execute an aggregation pipeline.

**Parameters:**
- `pipeline`: Aggregation pipeline.

##### `pipe_aggregate(builders: list[PipelineBuilder])`
Execute aggregation pipeline built by pipeline builders.

**Parameters:**
- `builders`: List of pipeline builder functions.

##### `aggregation_factory` (property) -> `AggregationFactory`
Get an `AggregationFactory` instance for this collection.

#### Collection Metadata

##### `name` (property) -> `str`
Return the collection name.

##### `database` (property) -> `Database[Any]`
Return the parent database.

#### Escape Hatch

##### `raw() -> Collection[Any]`
Return the underlying PyMongo Collection.

---

## AggregationFactory

Fluent interface for building aggregation pipelines.

### Class: `AggregationFactory`

#### Constructor

```python
AggregationFactory(collection: Collection) -> None
```

**Parameters:**
- `collection`: PyMongo Collection for execution.

#### Methods

All methods follow the pattern:

```python
def stage_name(self, pipeline: StageType) -> AggregationFactory:
    """Add a stage to the pipeline."""
    self._pipelines.append(pipeline)
    return self
```

Where `StageType` is one of the type-safe aggregation stage TypedDicts.

#### Available Stage Methods

- `match(pipeline: MatchStage)`
- `sort(pipeline: SortStage)`
- `limit(pipeline: LimitStage)`
- `project(pipeline: ProjectStage)`
- `skip(pipeline: SkipStage)`
- `unset(pipeline: UnsetStage)`
- `group(pipeline: GroupStage)`
- `unwind(pipeline: UnwindStage)`
- `vector_search(pipeline: VectorSearchStage)`
- `lookup(pipeline: LookupStage)`
- `add_fields(pipeline: AddFieldsStage)`
- `set(pipeline: SetStage)`
- `bucket(pipeline: BucketStage)`
- `bucket_auto(pipeline: BucketAutoStage)`
- `count(pipeline: CountStage)`
- `densify(pipeline: DensifyStage)`
- `documents(pipeline: DocumentsStage)`
- `facet(pipeline: FacetStage)`
- `fill(pipeline: FillStage)`
- `geo_near(pipeline: GeoNearStage)`
- `graph_lookup(pipeline: GraphLookupStage)`
- `replace_root(pipeline: ReplaceRootStage)`
- `replace_with(pipeline: ReplaceWithStage)`
- `sample(pipeline: SampleStage)`
- `sort_by_count(pipeline: SortByCountStage)`
- `set_window_fields(pipeline: SetWindowFieldsStage)`
- `union_with(pipeline: UnionWithStage)`
- `merge(pipeline: MergeStage)`
- `out(pipeline: OutStage)`
- `search(pipeline: SearchStage)`
- `search_meta(pipeline: SearchMetaStage)`

#### Execution

##### `execute()`
Execute the built aggregation pipeline.

**Returns:**
- Aggregation cursor results.

#### Usage Example

```python
factory = collection.aggregation_factory
results = (factory
    .match({"$match": {"status": "active"}})
    .sort({"$sort": {"name": 1}})
    .limit({"$limit": 10})
    .execute()
)
```

---

## Aggregation Stages

Type-safe TypedDict definitions for MongoDB aggregation stages.

### Type Aliases

```python
AggregationStage = Union[
    MatchStage, SortStage, LimitStage, ProjectStage, SkipStage,
    UnsetStage, GroupStage, UnwindStage, VectorSearchStage,
    LookupStage, AddFieldsStage, SetStage, BucketStage,
    BucketAutoStage, CountStage, DensifyStage, DocumentsStage,
    FacetStage, FillStage, GeoNearStage, GraphLookupStage,
    ReplaceRootStage, ReplaceWithStage, SampleStage, SortByCountStage,
    SetWindowFieldsStage, UnionWithStage, MergeStage, OutStage,
    SearchStage, SearchMetaStage
]

AggregationPipeline = list[AggregationStage]
```

### Available Stage Types

Each stage is defined as a TypedDict with a single key matching the MongoDB aggregation operator:

#### Query Stages
- `MatchStage = TypedDict("MatchStage", {"$match": dict[str, Any]})`
- `SortStage = TypedDict("SortStage", {"$sort": dict[str, Any]})`
- `LimitStage = TypedDict("LimitStage", {"$limit": int})`
- `SkipStage = TypedDict("SkipStage", {"$skip": int})`
- `ProjectStage = TypedDict("ProjectStage", {"$project": dict[str, Any]})`

#### Grouping Stages
- `GroupStage = TypedDict("GroupStage", {"$group": dict[str, Any]})`
- `UnwindStage = TypedDict("UnwindStage", {"$unwind": str | dict[str, Any]})`
- `BucketStage = TypedDict("BucketStage", {"$bucket": dict[str, Any]})`
- `BucketAutoStage = TypedDict("BucketAutoStage", {"$bucketAuto": dict[str, Any]})`
- `SortByCountStage = TypedDict("SortByCountStage", {"$sortByCount": str | dict[str, Any]})`

#### Join Stages
- `LookupStage = TypedDict("LookupStage", {"$lookup": dict[str, Any]})`
- `GraphLookupStage = TypedDict("GraphLookupStage", {"$graphLookup": dict[str, Any]})`

#### Field Modification
- `AddFieldsStage = TypedDict("AddFieldsStage", {"$addFields": dict[str, Any]})`
- `SetStage = TypedDict("SetStage", {"$set": dict[str, Any]})`
- `UnsetStage = TypedDict("UnsetStage", {"$unset": str | list[str]})`
- `ReplaceRootStage = TypedDict("ReplaceRootStage", {"$replaceRoot": dict[str, Any]})`
- `ReplaceWithStage = TypedDict("ReplaceWithStage", {"$replaceWith": dict[str, Any]})`

#### Search Stages
- `SearchStage = TypedDict("SearchStage", {"$search": dict[str, Any]})`
- `VectorSearchStage = TypedDict("VectorSearchStage", {"$vectorSearch": dict[str, Any]})`
- `SearchMetaStage = TypedDict("SearchMetaStage", {"$searchMeta": dict[str, Any]})`

#### Statistical Stages
- `FacetStage = TypedDict("FacetStage", {"$facet": dict[str, Any]})`
- `CountStage = TypedDict("CountStage", {"$count": str})`
- `SampleStage = TypedDict("SampleStage", {"$sample": dict[str, Any]})`

#### Time Series
- `DensifyStage = TypedDict("DensifyStage", {"$densify": dict[str, Any]})`
- `FillStage = TypedDict("FillStage", {"$fill": dict[str, Any]})`

#### Geospatial
- `GeoNearStage = TypedDict("GeoNearStage", {"$geoNear": dict[str, Any]})`

#### Window Operations
- `SetWindowFieldsStage = TypedDict("SetWindowFieldsStage", {"$setWindowFields": dict[str, Any]})`

#### Collection Operations
- `UnionWithStage = TypedDict("UnionWithStage", {"$unionWith": str | dict[str, Any]})`
- `MergeStage = TypedDict("MergeStage", {"$merge": dict[str, Any]})`
- `OutStage = TypedDict("OutStage", {"$out": str | dict[str, Any]})`

#### System Stages
- `CollStatsStage = TypedDict("CollStatsStage", {"$collStats": dict[str, Any]})`
- `IndexStatsStage = TypedDict("IndexStatsStage", {"$indexStats": dict[str, Any]})`

---

## PipelineBuilder

Utility class for building aggregation pipelines.

### Class: `PipelineBuilder`

#### Class Methods

##### `create(*pipeline: AggregationStage) -> AggregationPipeline`
Create an aggregation pipeline from stages.

**Parameters:**
- `*pipeline`: Variable number of aggregation stages.

**Returns:**
- `AggregationPipeline`: Aggregation pipeline.

**Usage:**
```python
from typing import cast
pipeline = PipelineBuilder.create(
    cast(MatchStage, {"$match": {"status": "active"}}),
    cast(SortStage, {"$sort": {"name": 1}})
)
```

---

## Type Definitions

### Document Type

```python
Document = dict[str, Any]
```

### PipelineBuilder Type

```python
PipelineBuilder = Callable[[AggregationPipeline], AggregationPipeline]
```

### Configuration Constants

```python
MONGODB_URI: str = os.environ.get(
    "MONGODB_URI",
    "mongodb://localhost:27017",
)
```

---

## Exports

Main module exports:

```python
__all__ = [
    'AggregationPipeline',
    'AggregationStage', 
    'AggregationFactory',
    'SimpleMongo',
    'PipelineBuilder'
]
```

---

## Error Handling

All methods may raise PyMongo exceptions. Common exceptions include:

- `pymongo.errors.ConnectionFailure`: Connection issues
- `pymongo.errors.OperationFailure`: Operation failures
- `pymongo.errors.DuplicateKeyError`: Duplicate key violations
- `pymongo.errors.WriteError`: Write operation errors

---

## Performance Considerations

1. **Connection Pooling**: The library uses PyMongo's built-in connection pooling.
2. **Cursor Streaming**: `find()` returns cursors for memory-efficient streaming.
3. **Batch Operations**: Use `insert_many()`, `update_many()`, `delete_many()` for bulk operations.
4. **Indexing**: Ensure appropriate indexes for query and aggregation performance.

---

## Best Practices

1. Always use context manager (`with SimpleMongo() as client:`) for automatic cleanup.
2. Use type casting with `typing.cast()` for better type safety with aggregation stages.
3. Leverage aggregation factory for complex pipelines with fluent syntax.
4. Use `raw()` method only when needed for PyMongo-specific features.
5. Configure connection options for production environments.