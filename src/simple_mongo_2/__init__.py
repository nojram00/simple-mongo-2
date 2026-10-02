from .aggregation_factory import AggregationPipeline, AggregationFactory, AggregationStage
from .db import Client as SimpleMongo
from .aggregation_pipeline_builder import PipelineBuilder

__all__ = [
    'AggregationPipeline',
    'AggregationStage',
    'AggregationFactory',
    'SimpleMongo',
    'PipelineBuilder'
]

def main():
    """Simple demonstration of the library."""
    print("simple-mongo-2 - A type-safe MongoDB client library")
    print("=" * 50)
    print("\nThis library provides:")
    print("• Type-safe MongoDB client wrapper")
    print("• Database and collection wrappers with dot notation")
    print("• Comprehensive aggregation pipeline support")
    print("• Fluent aggregation builder interface")
    print("• Environment variable configuration")
    print("\nFor usage examples, see the examples/ directory.")
    print("For API reference, see docs/API_REFERENCE.md")
