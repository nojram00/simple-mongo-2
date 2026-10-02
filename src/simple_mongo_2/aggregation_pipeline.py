"""
MongoDB Aggregation Pipeline Type Definitions.

This module provides type-safe Python definitions for MongoDB aggregation pipeline
stages using Python's TypedDict. These type definitions enable static type checking
for MongoDB aggregation queries, providing better development experience and
catching potential errors at development time.

The module defines individual TypedDicts for each MongoDB aggregation stage, along
with type aliases for composing full aggregation pipelines.

Usage Examples
--------------
>>> from typing import cast
>>> from langchain_test_proj.aggregation_pipeline import *
>>> 
>>> # Creating a type-safe aggregation pipeline
>>> pipeline: AggregationPipeline = [
>>>     cast(MatchStage, {"$match": {"status": "active"}}),
>>>     cast(SortStage, {"$sort": {"created_at": -1}}),
>>>     cast(ProjectStage, {"$project": {"_id": 0, "name": 1}})
>>> ]
>>> 
>>> # Individual stage usage
>>> match_stage: MatchStage = {"$match": {"age": {"$gte": 18}}}
>>> sort_stage: SortStage = {"$sort": {"name": 1}}
>>> 
>>> # Usage with AggregationFactory (from aggregation_factory.py)
>>> # factory = AggregationFactory(collection)
>>> # factory.match(match_stage).sort(sort_stage).execute()

Note: The `cast` function from typing module is recommended when creating stage
dictionaries to ensure proper type inference with static type checkers.

Type Aliases
------------
- `AggregationStage`: Union type of all supported aggregation stages
- `AggregationPipeline`: List of AggregationStage objects

For detailed MongoDB aggregation documentation, refer to:
https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
"""

from __future__ import annotations
from typing import Any, TypedDict, NotRequired, TypeAlias, Union

MatchStage = TypedDict(
    "MatchStage",
    {
        "$match": dict[str, Any],
    },
)

MatchStage.__doc__ = """
MongoDB $match stage for filtering documents.

The $match stage filters documents that match
the specified conditions.

Example
-------
stage: MatchStage = {
    "$match": {
        "status": "active",
        "age": {
            "$gte": 18,
        },
    },
}
"""

ProjectStage = TypedDict(
    "ProjectStage",
    {
        "$project": dict[str, Any]
    }
)
"""
MongoDB $project stage for reshaping documents.

The $project stage passes along documents with requested fields to the next
stage in the pipeline. It can be used to include, exclude, or add computed fields.

Example
-------
>>> from typing import cast
>>> stage: ProjectStage = cast(ProjectStage, {
...     "$project": {"_id": 0, "name": 1, "age": 1}
... })
"""

LimitStage = TypedDict(
    "LimitStage",
    {
        "$limit": int,
    },
)
"""
MongoDB $limit stage for limiting document count.

The $limit stage restricts the number of documents passed to the next stage.

Example
-------
>>> from typing import cast
>>> stage: LimitStage = cast(LimitStage, {"$limit": 10})
"""

SortStage = TypedDict(
    "SortStage",
    {
        "$sort": dict[str, int]
    }
)
"""
MongoDB $sort stage for ordering documents.

The $sort stage orders all input documents and returns them to the pipeline
in sorted order. Use 1 for ascending and -1 for descending.

Example
-------
>>> from typing import cast
>>> stage: SortStage = cast(SortStage, {"$sort": {"created_at": -1, "name": 1}})
"""

SkipStage = TypedDict(
    "SkipStage",
    {
        "$skip": int
    }
)
"""
MongoDB $skip stage for skipping documents.

The $skip stage skips over the specified number of documents and passes the
remaining documents to the next stage.

Example
-------
>>> from typing import cast
>>> stage: SkipStage = cast(SkipStage, {"$skip": 5})
"""

UnsetStage = TypedDict(
    "UnsetStage", 
    {
        "$unset": Union[str, list[str]]
    }
)
"""
MongoDB $unset stage for removing fields.

The $unstage stage removes/excludes fields from documents.

Example
-------
>>> from typing import cast
>>> # Single field
>>> stage: UnsetStage = cast(UnsetStage, {"$unset": "internal_id"})
>>> # Multiple fields
>>> stage: UnsetStage = cast(UnsetStage, {"$unset": ["internal_id", "debug_info"]})
"""

GroupStage = TypedDict(
    "GroupStage",
    {
        "$group": dict[str, Any]
    }
)
"""
MongoDB $group stage for grouping documents.

The $group stage groups documents by a specified identifier expression and
applies accumulator expressions to each group.

Example
-------
>>> from typing import cast
>>> stage: GroupStage = cast(GroupStage, {
...     "$group": {
...         "_id": "$department",
...         "avgSalary": {"$avg": "$salary"},
...         "count": {"$sum": 1}
...     }
... })
"""

UnwindStage = TypedDict(
    "UnwindStage",
    {
        "$unwind": Union[str, dict[str, Any]]
    }
)
"""
MongoDB $unwind stage for deconstructing arrays.

The $unwind stage deconstructs an array field from input documents to output
a document for each element in the array.

Example
-------
>>> from typing import cast
>>> # Simple unwind
>>> stage: UnwindStage = cast(UnwindStage, {"$unwind": "$tags"})
>>> # With options
>>> stage: UnwindStage = cast(UnwindStage, {
...     "$unwind": {
...         "path": "$tags",
...         "preserveNullAndEmptyArrays": True
...     }
... })
"""

VectorSearchStage = TypedDict(
    "VectorSearchStage",
    {
        "$vectorSearch": dict[str, Any]
    }
)
"""
MongoDB $vectorSearch stage for semantic search.

The $vectorSearch stage performs a vector similarity search using Atlas
Vector Search indexes.

Example
-------
>>> from typing import cast
>>> stage: VectorSearchStage = cast(VectorSearchStage, {
...     "$vectorSearch": {
...         "index": "vector_index",
...         "path": "embedding",
...         "queryVector": [0.1, 0.2, 0.3],
...         "numCandidates": 100,
...         "limit": 10
...     }
... })
"""

LookupEquality = TypedDict(
    "LookupEquality",
    {
        "from": str,
        "localField": str,
        "foreignField": str,
        "as": str
    }
)
"""
Equality lookup configuration for $lookup stage.

Used when performing simple equality joins between fields.
"""

LookupPipeline = TypedDict(
    "LookupPipeline",
    {
        "from": str,
        "let": dict[str, Any],
        "pipeline": list[dict[str, Any]],
        "as": str
    }
)
"""
Pipeline lookup configuration for $lookup stage.

Used when performing complex joins using sub-pipelines.
"""

LookupStage = TypedDict(
    "LookupStage",
    {
        "$lookup": Union[LookupEquality, LookupPipeline]
    }
)
"""
MongoDB $lookup stage for joining collections.

The $lookup stage performs a left outer join to an unsharded collection
in the same database.

Example
-------
>>> from typing import cast
>>> # Equality join
>>> stage: LookupStage = cast(LookupStage, {
...     "$lookup": {
...         "from": "users",
...         "localField": "user_id",
...         "foreignField": "_id",
...         "as": "user_info"
...     }
... })
>>> # Pipeline join
>>> stage: LookupStage = cast(LookupStage, {
...     "$lookup": {
...         "from": "orders",
...         "let": {"user_id": "$_id"},
...         "pipeline": [
...             {"$match": {"$expr": {"$eq": ["$user_id", "$$user_id"]}}}
...         ],
...         "as": "user_orders"
...     }
... })
"""

AddFieldsStage = TypedDict("AddFieldsStage", {"$addFields": dict[str, Any]})
"""
MongoDB $addFields stage for adding computed fields.

The $addFields stage adds new fields to documents while preserving all
existing fields.

Example
-------
>>> from typing import cast
>>> stage: AddFieldsStage = cast(AddFieldsStage, {
...     "$addFields": {
...         "total": {"$add": ["$price", "$tax"]},
...         "isDiscounted": {"$lt": ["$price", 100]}
...     }
... })
"""

SetStage = TypedDict("SetStage", {"$set": dict[str, Any]})
"""
MongoDB $set stage for adding or replacing fields.

The $set stage adds new fields or replaces the value of existing fields
(alias for $addFields).

Example
-------
>>> from typing import cast
>>> stage: SetStage = cast(SetStage, {
...     "$set": {"status": "processed", "processed_at": "$$NOW"}
... })
"""

BucketStage = TypedDict("BucketStage", {"$bucket": dict[str, Any]})
"""
MongoDB $bucket stage for bucketing documents.

The $bucket stage categorizes documents into groups based on specified
boundaries.

Example
-------
>>> from typing import cast
>>> stage: BucketStage = cast(BucketStage, {
...     "$bucket": {
...         "groupBy": "$age",
...         "boundaries": [0, 18, 30, 50, 100],
...         "default": "Other",
...         "output": {"count": {"$sum": 1}}
...     }
... })
"""

BucketAutoStage = TypedDict("BucketAutoStage", {"$bucketAuto": dict[str, Any]})
"""
MongoDB $bucketAuto stage for automatic bucketing.

The $bucketAuto stage categorizes documents into a specific number of
buckets, automatically determining boundaries.

Example
-------
>>> from typing import cast
>>> stage: BucketAutoStage = cast(BucketAutoStage, {
...     "$bucketAuto": {
...         "groupBy": "$price",
...         "buckets": 5,
...         "output": {"count": {"$sum": 1}}
...     }
... })
"""

CountStage = TypedDict("CountStage", {"$count": str})
"""
MongoDB $count stage for counting documents.

The $count stage returns a count of the documents at that stage.

Example
-------
>>> from typing import cast
>>> stage: CountStage = cast(CountStage, {"$count": "total_users"})
"""

DensifyStage = TypedDict("DensifyStage", {"$densify": dict[str, Any]})
"""
MongoDB $densify stage for creating documents.

The $densify stage creates new documents in a sequence to fill gaps.

Example
-------
>>> from typing import cast
>>> stage: DensifyStage = cast(DensifyStage, {
...     "$densify": {
...         "field": "timestamp",
...         "range": {"step": 3600000, "unit": "millisecond"}
...     }
... })
"""

DocumentsStage = TypedDict("DocumentsStage", {"$documents": list[dict[str, Any]]})
"""
MongoDB $documents stage for generating documents.

The $documents stage returns literal documents from input expressions.

Example
-------
>>> from typing import cast
>>> stage: DocumentsStage = cast(DocumentsStage, {
...     "$documents": [
...         {"name": "John", "role": "admin"},
...         {"name": "Jane", "role": "user"}
...     ]
... })
"""

FacetStage = TypedDict("FacetStage", {"$facet": dict[str, list[dict[str, Any]]]})
"""
MongoDB $facet stage for multi-faceted aggregations.

The $facet stage processes multiple aggregation pipelines within a single
stage.

Example
-------
>>> from typing import cast
>>> stage: FacetStage = cast(FacetStage, {
...     "$facet": {
...         "categories": [{"$group": {"_id": "$category"}}],
...         "price_stats": [
...             {"$group": {
...                 "_id": None,
...                 "avg": {"$avg": "$price"},
...                 "max": {"$max": "$price"}
...             }}
...         ]
...     }
... })
"""

FillStage = TypedDict("FillStage", {"$fill": dict[str, Any]})
"""
MongoDB $fill stage for filling null values.

The $fill stage populates null and missing field values within documents.

Example
-------
>>> from typing import cast
>>> stage: FillStage = cast(FillStage, {
...     "$fill": {
...         "output": {"price": {"value": "linear"}},
...         "partitionBy": "$product_id",
...         "sortBy": {"timestamp": 1}
...     }
... })
"""

GeoNearStage = TypedDict("GeoNearStage", {"$geoNear": dict[str, Any]})
"""
MongoDB $geoNear stage for geospatial queries.

The $geoNear stage returns documents in order of proximity to a
geospatial point.

Example
-------
>>> from typing import cast
>>> stage: GeoNearStage = cast(GeoNearStage, {
...     "$geoNear": {
...         "near": {"type": "Point", "coordinates": [-73.9667, 40.78]},
...         "distanceField": "distance",
...         "maxDistance": 5000,
...         "spherical": True
...     }
... })
"""

GraphLookupStage = TypedDict("GraphLookupStage", {"$graphLookup": dict[str, Any]})
"""
MongoDB $graphLookup stage for graph traversals.

The $graphLookup stage performs recursive search on a collection.

Example
-------
>>> from typing import cast
>>> stage: GraphLookupStage = cast(GraphLookupStage, {
...     "$graphLookup": {
...         "from": "employees",
...         "startWith": "$reports_to",
...         "connectFromField": "reports_to",
...         "connectToField": "_id",
...         "as": "management_chain"
...     }
... })
"""

ReplaceRootStage = TypedDict("ReplaceRootStage", {"$replaceRoot": dict[str, Any]})
"""
MongoDB $replaceRoot stage for replacing document root.

The $replaceRoot stage replaces the input document with a new document.

Example
-------
>>> from typing import cast
>>> stage: ReplaceRootStage = cast(ReplaceRootStage, {
...     "$replaceRoot": {"newRoot": "$user_info"}
... })
"""

ReplaceWithStage = TypedDict("ReplaceWithStage", {"$replaceWith": Any})
"""
MongoDB $replaceWith stage for replacing documents.

The $replaceWith stage replaces the input document (alias for $replaceRoot).

Example
-------
>>> from typing import cast
>>> stage: ReplaceWithStage = cast(ReplaceWithStage, {
...     "$replaceWith": {"$mergeObjects": ["$$ROOT", {"processed": True}]}
... })
"""

SampleStage = TypedDict("SampleStage", {"$sample": dict[str, int]})
"""
MongoDB $sample stage for random sampling.

The $sample stage randomly selects documents.

Example
-------
>>> from typing import cast
>>> stage: SampleStage = cast(SampleStage, {"$sample": {"size": 10}})
"""

SortByCountStage = TypedDict("SortByCountStage", {"$sortByCount": Any})
"""
MongoDB $sortByCount stage for sorting by frequency.

The $sortByCount stage groups documents and sorts by count.

Example
-------
>>> from typing import cast
>>> stage: SortByCountStage = cast(SortByCountStage, {
...     "$sortByCount": "$category"
... })
"""

SetWindowFieldsStage = TypedDict("SetWindowFieldsStage", {"$setWindowFields": dict[str, Any]})
"""
MongoDB $setWindowFields stage for window functions.

The $setWindowFields stage performs operations on a specified range of
documents (window).

Example
-------
>>> from typing import cast
>>> stage: SetWindowFieldsStage = cast(SetWindowFieldsStage, {
...     "$setWindowFields": {
...         "partitionBy": "$department",
...         "sortBy": {"salary": -1},
...         "output": {"rank": {"$rank": {}}}
...     }
... })
"""

UnionWithStage = TypedDict("UnionWithStage", {"$unionWith": Union[str, dict[str, Any]]})
"""
MongoDB $unionWith stage for combining pipelines.

The $unionWith stage combines documents from multiple collections.

Example
-------
>>> from typing import cast
>>> # Simple collection union
>>> stage: UnionWithStage = cast(UnionWithStage, {"$unionWith": "archived_users"})
>>> # Collection union with pipeline
>>> stage: UnionWithStage = cast(UnionWithStage, {
...     "$unionWith": {
...         "coll": "archived_users",
...         "pipeline": [{"$match": {"status": "inactive"}}]
...     }
... })
"""

MergeStage = TypedDict("MergeStage", {"$merge": Union[str, dict[str, Any]]})
"""
MongoDB $merge stage for outputting results.

The $merge stage writes the pipeline results to a collection.

Example
-------
>>> from typing import cast
>>> # Simple merge
>>> stage: MergeStage = cast(MergeStage, {"$merge": "summary_stats"})
>>> # Merge with options
>>> stage: MergeStage = cast(MergeStage, {
...     "$merge": {
...         "into": "summary_stats",
...         "on": "_id",
...         "whenMatched": "merge",
...         "whenNotMatched": "insert"
...     }
... })
"""

OutStage = TypedDict("OutStage", {"$out": Union[str, dict[str, Any]]})
"""
MongoDB $out stage for writing results.

The $out stage writes the pipeline results to a collection, replacing
existing content.

Example
-------
>>> from typing import cast
>>> # Simple output
>>> stage: OutStage = cast(OutStage, {"$out": "report_results"})
>>> # Output to different database
>>> stage: OutStage = cast(OutStage, {
...     "$out": {"db": "analytics", "coll": "reports"}
... })
"""

SearchStage = TypedDict("SearchStage", {"$search": dict[str, Any]})
"""
MongoDB $search stage for Atlas Search queries.

The $search stage performs full-text search using Atlas Search.

Example
-------
>>> from typing import cast
>>> stage: SearchStage = cast(SearchStage, {
...     "$search": {
...         "index": "default",
...         "text": {"query": "mongodb", "path": "description"}
...     }
... })
"""

SearchMetaStage = TypedDict("SearchMetaStage", {"$searchMeta": dict[str, Any]})
"""
MongoDB $searchMeta stage for search metadata.

The $searchMeta stage returns metadata for Atlas Search queries.

Example
-------
>>> from typing import cast
>>> stage: SearchMetaStage = cast(SearchMetaStage, {
...     "$searchMeta": {
...         "index": "default",
...         "highlight": {"path": "description"}
...     }
... })
"""

ListSearchIndexesStage = TypedDict("ListSearchIndexesStage", {"$listSearchIndexes": dict[str, Any]})
"""
MongoDB $listSearchIndexes stage for listing search indexes.

The $listSearchIndexes stage returns information about Atlas Search indexes.

Example
-------
>>> from typing import cast
>>> stage: ListSearchIndexesStage = cast(ListSearchIndexesStage, {
...     "$listSearchIndexes": {}
... })
"""

ChangeStreamStage = TypedDict("ChangeStreamStage", {"$changeStream": dict[str, Any]})
"""
MongoDB $changeStream stage for change streams.

The $changeStream stage creates a change stream cursor.

Example
-------
>>> from typing import cast
>>> stage: ChangeStreamStage = cast(ChangeStreamStage, {
...     "$changeStream": {
...         "fullDocument": "updateLookup",
...         "resumeAfter": {"_data": "8264..."}
...     }
... })
"""

ChangeStreamSplitLargeEventStage = TypedDict(
    "ChangeStreamSplitLargeEventStage", {"$changeStreamSplitLargeEvent": dict[str, Any]}
)
"""
MongoDB $changeStreamSplitLargeEvent stage for large change events.

The $changeStreamSplitLargeEvent stage splits large change stream events.

Example
-------
>>> from typing import cast
>>> stage: ChangeStreamSplitLargeEventStage = cast(ChangeStreamSplitLargeEventStage, {
...     "$changeStreamSplitLargeEvent": {}
... })
"""

CollStatsStage = TypedDict("CollStatsStage", {"$collStats": dict[str, Any]})
"""
MongoDB $collStats stage for collection statistics.

The $collStats stage returns statistics regarding a collection.

Example
-------
>>> from typing import cast
>>> stage: CollStatsStage = cast(CollStatsStage, {
...     "$collStats": {"storageStats": {}}
... })
"""

CurrentOpStage = TypedDict("CurrentOpStage", {"$currentOp": dict[str, Any]})
"""
MongoDB $currentOp stage for current operations.

The $currentOp stage returns information on current operations.

Example
-------
>>> from typing import cast
>>> stage: CurrentOpStage = cast(CurrentOpStage, {
...     "$currentOp": {"allUsers": True}
... })
"""

IndexStatsStage = TypedDict("IndexStatsStage", {"$indexStats": dict[str, Any]})
"""
MongoDB $indexStats stage for index statistics.

The $indexStats stage returns statistics regarding use of each index.

Example
-------
>>> from typing import cast
>>> stage: IndexStatsStage = cast(IndexStatsStage, {"$indexStats": {}})
"""

ListLocalSessionsStage = TypedDict("ListLocalSessionsStage", {"$listLocalSessions": dict[str, Any]})
"""
MongoDB $listLocalSessions stage for local sessions.

The $listLocalSessions stage lists sessions cached locally.

Example
-------
>>> from typing import cast
>>> stage: ListLocalSessionsStage = cast(ListLocalSessionsStage, {
...     "$listLocalSessions": {}
... })
"""

ListSessionsStage = TypedDict("ListSessionsStage", {"$listSessions": dict[str, Any]})
"""
MongoDB $listSessions stage for sessions.

The $listSessions stage lists all sessions in the system.

Example
-------
>>> from typing import cast
>>> stage: ListSessionsStage = cast(ListSessionsStage, {"$listSessions": {}})
"""

PlanCacheStatsStage = TypedDict("PlanCacheStatsStage", {"$planCacheStats": dict[str, Any]})
"""
MongoDB $planCacheStats stage for plan cache statistics.

The $planCacheStats stage returns plan cache statistics.

Example
-------
>>> from typing import cast
>>> stage: PlanCacheStatsStage = cast(PlanCacheStatsStage, {"$planCacheStats": {}})
"""

QueryStatsStage = TypedDict("QueryStatsStage", {"$queryStats": dict[str, Any]})
"""
MongoDB $queryStats stage for query statistics.

The $queryStats stage returns query statistics.

Example
-------
>>> from typing import cast
>>> stage: QueryStatsStage = cast(QueryStatsStage, {"$queryStats": {}})
"""

AggregationStage: TypeAlias = Union[
    MatchStage,
    ProjectStage,
    SortStage,
    LimitStage,
    SkipStage,
    UnsetStage,
    GroupStage,
    UnwindStage,
    VectorSearchStage,
    LookupStage,
    AddFieldsStage,
    SetStage,
    BucketStage,
    BucketAutoStage,
    CountStage,
    DensifyStage,
    DocumentsStage,
    FacetStage,
    FillStage,
    GeoNearStage,
    GraphLookupStage,
    ReplaceRootStage,
    ReplaceWithStage,
    SampleStage,
    SortByCountStage,
    SetWindowFieldsStage,
    UnionWithStage,
    MergeStage,
    OutStage,
    SearchStage,
    SearchMetaStage,
    ListSearchIndexesStage,
    ChangeStreamStage,
    ChangeStreamSplitLargeEventStage,
    CollStatsStage,
    CurrentOpStage,
    IndexStatsStage,
    ListLocalSessionsStage,
    ListSessionsStage,
    PlanCacheStatsStage,
    QueryStatsStage
]
"""
Union type representing any valid MongoDB aggregation stage.

This type alias includes all supported aggregation stages, enabling type-safe
composition of aggregation pipelines.

Example
-------
>>> from typing import cast
>>> from langchain_test_proj.aggregation_pipeline import *
>>>
>>> # Individual stage usage
>>> stage1: AggregationStage = cast(MatchStage, {"$match": {"active": True}})
>>> stage2: AggregationStage = cast(SortStage, {"$sort": {"created_at": -1}})
>>>
>>> # Type checking ensures only valid stages are used
>>> # This would cause a type error with static type checkers:
>>> # invalid_stage: AggregationStage = {"$invalid": {"field": "value"}}
"""


AggregationPipeline: TypeAlias = list[AggregationStage]
"""
Type alias representing a complete MongoDB aggregation pipeline.

A pipeline is an ordered list of aggregation stages that documents pass through.

Example
-------
>>> from typing import cast
>>> from langchain_test_proj.aggregation_pipeline import *
>>>
>>> # Complete type-safe pipeline
>>> pipeline: AggregationPipeline = [
>>>     cast(MatchStage, {"$match": {"status": "active"}}),
>>>     cast(SortStage, {"$sort": {"score": -1}}),
>>>     cast(ProjectStage, {"$project": {"_id": 0, "name": 1, "score": 1}}),
>>>     cast(LimitStage, {"$limit": 10})
>>> ]
>>>
>>> # Usage with CollectionWrapper
>>> # collection = client.test_db.users
>>> # results = collection.aggregate(pipeline)
"""