from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar, TypedDict

from dotenv import load_dotenv

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import (
    DeleteResult,
    InsertOneResult,
    InsertManyResult,
    UpdateResult,
)

from .aggregation_factory import AggregationFactory
from .aggregation_pipeline import AggregationPipeline


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

MONGODB_URI: str = os.environ.get(
    "MONGODB_URI",
    "mongodb://localhost:27017",
)

Document = dict[str, Any]
T = TypeVar("T")

PipelineBuilder = Callable[[AggregationPipeline], AggregationPipeline]

# ---------------------------------------------------------------------------
# Collection wrapper
# ---------------------------------------------------------------------------

class CollectionWrapper:
    """
    Wrapper around a PyMongo Collection.

    Provides a convenient interface for common MongoDB operations while
    preserving access to the underlying PyMongo collection.

    Example
    -------
    >>> users = client.test_db.users

    >>> users.find_one({"name": "John"})

    >>> users.find({"age": {"$gte": 18}}).sort("name", 1).limit(10)
    """

    def __init__(self, collection: Collection[Any]) -> None:
        """
        Initialize a collection wrapper.

        Parameters
        ----------
        collection:
            The underlying PyMongo collection.
        """
        self.collection = collection

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------

    def find(
        self,
        filter: Optional[Mapping[str, Any]] = None,
        projection: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> Cursor[Any]:
        """
        Find multiple documents.

        Returns a PyMongo Cursor, allowing normal MongoDB chaining.

        Example
        -------
        >>> users.find({"age": {"$gte": 18}}).sort("name", 1).limit(10)
        """
        return self.collection.find(
            filter,
            projection,
            **kwargs,
        )

    def find_one(
        self,
        filter: Optional[Mapping[str, Any]] = None,
        projection: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> Optional[Document]:
        """
        Find a single document.

        Returns None if no matching document exists.
        """
        return self.collection.find_one(
            filter,
            projection,
            **kwargs,
        )

    def find_one_by_id(
        self,
        document_id: ObjectId | str,
    ) -> Optional[Document]:
        """
        Find a document by its MongoDB _id.

        Parameters
        ----------
        document_id:
            MongoDB ObjectId or its string representation.
        """
        if isinstance(document_id, str):
            document_id = ObjectId(document_id)

        return self.collection.find_one({
            "_id": document_id,
        })

    # ------------------------------------------------------------------
    # Insert methods
    # ------------------------------------------------------------------

    def insert_one(
        self,
        document: Document,
        **kwargs: Any,
    ) -> InsertOneResult:
        """
        Insert a single document.
        """
        return self.collection.insert_one(
            document,
            **kwargs,
        )

    def insert_many(
        self,
        documents: Sequence[Document],
        **kwargs: Any,
    ) -> InsertManyResult:
        """
        Insert multiple documents.
        """
        return self.collection.insert_many(
            documents,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Update methods
    # ------------------------------------------------------------------

    def update_one(
        self,
        filter: Mapping[str, Any],
        update: Mapping[str, Any],
        **kwargs: Any,
    ) -> UpdateResult:
        """
        Update a single document.
        """
        return self.collection.update_one(
            filter,
            update,
            **kwargs,
        )

    def update_many(
        self,
        filter: Mapping[str, Any],
        update: Mapping[str, Any],
        **kwargs: Any,
    ) -> UpdateResult:
        """
        Update multiple documents.
        """
        return self.collection.update_many(
            filter,
            update,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Delete methods
    # ------------------------------------------------------------------

    def delete_one(
        self,
        filter: Mapping[str, Any],
        **kwargs: Any,
    ) -> DeleteResult:
        """
        Delete a single document.
        """
        return self.collection.delete_one(
            filter,
            **kwargs,
        )

    def delete_many(
        self,
        filter: Mapping[str, Any],
        **kwargs: Any,
    ) -> DeleteResult:
        """
        Delete multiple documents.
        """
        return self.collection.delete_many(
            filter,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Collection metadata
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Return the collection name."""
        return self.collection.name

    @property
    def database(self) -> Database[Any]:
        """Return the parent database."""
        return self.collection.database

    def count_documents(
        self,
        filter: Mapping[str, Any],
        **kwargs: Any,
    ) -> int:
        """
        Count documents matching a filter.
        """
        return self.collection.count_documents(
            filter,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    @property
    def aggregation_factory(self) -> AggregationFactory:
        return AggregationFactory(self.collection)
    
    def aggregate(self, pipeline : AggregationPipeline):
        return self.collection.aggregate(pipeline)

    def pipe_aggregate(self, builders : list[PipelineBuilder]):
        pipeline : AggregationPipeline = []

        for builder in builders:
            pipeline = builder(pipeline)

        return self.collection.aggregate(pipeline)

    # ------------------------------------------------------------------
    # Escape hatch
    # ------------------------------------------------------------------

    def raw(self) -> Collection[Any]:
        """
        Return the underlying PyMongo Collection.

        Useful when you need a PyMongo feature that this wrapper does not
        explicitly expose.
        """
        return self.collection


# ---------------------------------------------------------------------------
# Database wrapper
# ---------------------------------------------------------------------------

class DatabaseWrapper:
    """
    Wrapper around a PyMongo Database.

    Collections can be accessed using attribute syntax:

        client.test_db.users
        client.test_db.products

    The resulting objects are CollectionWrapper instances.
    """

    def __init__(self, database: Database[Any]) -> None:
        """
        Initialize a database wrapper.
        """
        self.database = database

    def __getattr__(self, name: str) -> CollectionWrapper:
        """
        Resolve an attribute into a MongoDB collection.

        Example
        -------
        >>> client.test_db.users

        is equivalent to:

        >>> client.test_db["users"]
        """
        if name.startswith("_"):
            raise AttributeError(name)

        return CollectionWrapper(
            self.database.get_collection(name)
        )

    def collection(self, name: str) -> CollectionWrapper:
        """
        Explicitly access a collection by name.

        This is useful when the collection name contains characters that
        cannot be used in Python attribute syntax.
        """
        return CollectionWrapper(
            self.database.get_collection(name)
        )

    def raw(self) -> Database[Any]:
        """
        Return the underlying PyMongo Database.
        """
        return self.database


# ---------------------------------------------------------------------------
# MongoDB client wrapper
# ---------------------------------------------------------------------------

class Client:
    """
    High-level MongoDB client wrapper.

    Databases and collections can be accessed using chained attributes.

    Example
    -------
    >>> client = Client()

    >>> client.test_db.users.find_one({
    ...     "name": "John"
    ... })

    >>> client.test_db.users.find({
    ...     "age": {"$gte": 18}
    ... }).sort("name", 1).limit(10)

    The underlying PyMongo MongoClient is kept open for the lifetime of
    this object.
    """

    def __init__(
        self,
        uri: str = MONGODB_URI,
        **kwargs: Any,
    ) -> None:
        """
        Create a MongoDB client.

        Parameters
        ----------
        uri:
            MongoDB connection URI.

        **kwargs:
            Additional options passed directly to PyMongo MongoClient.
        """
        self.instance: MongoClient[Any] = MongoClient(
            uri,
            **kwargs,
        )

    def __enter__(self) -> Client:
        """
        Enter the context manager.

        The existing MongoClient is returned rather than creating another
        connection.
        """
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        """
        Close the MongoDB client when leaving the context manager.
        """
        self.close()

    def __getattr__(self, name: str) -> DatabaseWrapper:
        """
        Resolve an attribute into a MongoDB database.

        Example
        -------
        >>> client.test_db

        is equivalent to:

        >>> client.instance.get_database("test_db")
        """
        if name.startswith("_"):
            raise AttributeError(name)

        return DatabaseWrapper(
            self.instance.get_database(name)
        )

    def database(self, name: str) -> DatabaseWrapper:
        """
        Explicitly access a database by name.
        """
        return DatabaseWrapper(
            self.instance.get_database(name)
        )

    def ping(self) -> bool:
        """
        Check whether MongoDB is reachable.

        Returns
        -------
        bool
            True if MongoDB responds successfully.

        Raises
        ------
        pymongo.errors.PyMongoError
            If the connection fails.
        """
        self.instance.admin.command("ping")
        return True

    def close(self) -> None:
        """
        Close the MongoDB client.
        """
        self.instance.close()

    def raw(self) -> MongoClient[Any]:
        """
        Return the underlying PyMongo MongoClient.

        This acts as an escape hatch when direct PyMongo functionality
        is required.
        """
        return self.instance


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    with Client() as client:

        # Test connection
        client.ping()

        # Database
        users = client.test_db.users

        # Insert
        result = users.insert_one({
            "name": "John",
            "age": 25,
        })

        print("Inserted:", result.inserted_id)

        # Find one
        user = users.find_one({
            "name": "John",
        })

        print(user)

        # Chained MongoDB cursor
        cursor = (
            users
            .find({"age": {"$gte": 18}})
            .sort("name", 1)
            .limit(10)
        )

        for user in cursor:
            print(user)
