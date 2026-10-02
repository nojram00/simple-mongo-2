# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release of simple-mongo-2
- Type-safe MongoDB client wrapper (`SimpleMongo`)
- Database wrapper with dot notation access (`DatabaseWrapper`)
- Collection wrapper with intuitive CRUD operations (`CollectionWrapper`)
- Comprehensive type-safe aggregation pipeline definitions
- Fluent aggregation builder (`AggregationFactory`)
- Pipeline builder utility (`PipelineBuilder`)
- Environment variable configuration support
- Context manager support for automatic cleanup
- Escape hatches to access underlying PyMongo objects
- Full static type checking support with Python 3.14+
- Complete documentation with examples

### Features
- Dot notation for database and collection access
- Type-safe aggregation stage definitions using TypedDict
- Support for all MongoDB aggregation stages
- Connection pooling and configuration options
- Batch operation support
- Error handling with PyMongo exceptions
- Connection testing with `ping()` method

### Technical Details
- Built on PyMongo 4.18.2+
- Python 3.14+ requirement for TypedDict features
- Environment configuration via python-dotenv
- MIT License