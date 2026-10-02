from typing import List

from .aggregation_pipeline import *

# ---------------------------------------------------------------------------
# Aggregation Factory wrapper
# ---------------------------------------------------------------------------

from pymongo.collection import Collection
from .aggregation_pipeline import AggregationPipeline

class AggregationFactory:
    def __init__(self, collection : Collection) -> None:
        self.collection = collection
        self._pipelines : AggregationPipeline = []

    def execute(self):
        return self.collection.aggregate(self._pipelines)

    def match(self, pipeline : MatchStage):
        self._pipelines.append(pipeline)
        return self

    def sort(self, pipeline : SortStage):
        self._pipelines.append(pipeline)
        return self

    def limit(self, pipeline : LimitStage):
        self._pipelines.append(pipeline)
        return self

    def project(self, pipeline: ProjectStage):
        self._pipelines.append(pipeline)
        return self

    def skip(self, pipeline: SkipStage):
        self._pipelines.append(pipeline)
        return self

    def unset(self, pipeline: UnsetStage):
        self._pipelines.append(pipeline)
        

    def group(self, pipeline: GroupStage):
        self._pipelines.append(pipeline)
        return self

    def unwind(self, pipeline: UnwindStage):
        self._pipelines.append(pipeline)
        return self

    def vector_search(self, pipeline: VectorSearchStage):
        self._pipelines.append(pipeline)
        return self

    def lookup(self, pipeline: LookupStage):
        self._pipelines.append(pipeline)
        return self

    def add_fields(self, pipeline: AddFieldsStage):
        self._pipelines.append(pipeline)
        return self

    def set(self, pipeline: SetStage):
        self._pipelines.append(pipeline)
        return self

    def bucket(self, pipeline: BucketStage):
        self._pipelines.append(pipeline)
        return self

    def bucket_auto(self, pipeline: BucketAutoStage):
        self._pipelines.append(pipeline)
        return self

    def count(self, pipeline: CountStage):
        self._pipelines.append(pipeline)
        return self

    def densify(self, pipeline: DensifyStage):
        self._pipelines.append(pipeline)
        return self

    def documents(self, pipeline: DocumentsStage):
        self._pipelines.append(pipeline)
        return self

    def facet(self, pipeline: FacetStage):
        self._pipelines.append(pipeline)
        return self

    def fill(self, pipeline: FillStage):
        self._pipelines.append(pipeline)
        return self

    def geo_near(self, pipeline: GeoNearStage):
        self._pipelines.append(pipeline)
        return self

    def graph_lookup(self, pipeline: GraphLookupStage):
        self._pipelines.append(pipeline)
        return self

    def replace_root(self, pipeline: ReplaceRootStage):
        self._pipelines.append(pipeline)
        return self

    def replace_with(self, pipeline: ReplaceWithStage):
        self._pipelines.append(pipeline)
        return self

    def sample(self, pipeline: SampleStage):
        self._pipelines.append(pipeline)
        return self

    def sort_by_count(self, pipeline: SortByCountStage):
        self._pipelines.append(pipeline)
        return self

    def set_window_fields(self, pipeline: SetWindowFieldsStage):
        self._pipelines.append(pipeline)
        return self

    def union_with(self, pipeline: UnionWithStage):
        self._pipelines.append(pipeline)
        return self

    def merge(self, pipeline: MergeStage):
        self._pipelines.append(pipeline)
        return self

    def out(self, pipeline: OutStage):
        self._pipelines.append(pipeline)
        return self

    def search(self, pipeline: SearchStage):
        self._pipelines.append(pipeline)
        return self

    def search_meta(self, pipeline: SearchMetaStage):
        self._pipelines.append(pipeline)
        return self

    def list_search_indexes(self, pipeline: ListSearchIndexesStage):
        self._pipelines.append(pipeline)
        return self

    def change_stream(self, pipeline: ChangeStreamStage):
        self._pipelines.append(pipeline)
        return self

    def change_stream_split_large_event(self, pipeline: ChangeStreamSplitLargeEventStage):
        self._pipelines.append(pipeline)
        return self

    def coll_stats(self, pipeline: CollStatsStage):
        self._pipelines.append(pipeline)
        return self

    def current_op(self, pipeline: CurrentOpStage):
        self._pipelines.append(pipeline)
        return self

    def index_stats(self, pipeline: IndexStatsStage):
        self._pipelines.append(pipeline)
        return self

    def list_local_sessions(self, pipeline: ListLocalSessionsStage):
        self._pipelines.append(pipeline)
        return self

    def list_sessions(self, pipeline: ListSessionsStage):
        self._pipelines.append(pipeline)
        return self

    def plan_cache_stats(self, pipeline: PlanCacheStatsStage):
        self._pipelines.append(pipeline)
        return self

    def query_stats(self, pipeline: QueryStatsStage):
        self._pipelines.append(pipeline)
        return self
        