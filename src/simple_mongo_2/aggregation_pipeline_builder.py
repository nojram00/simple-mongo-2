from .aggregation_pipeline import AggregationStage, AggregationPipeline

class PipelineBuilder(list[AggregationStage]): 
    @classmethod
    def create(cls, *pipeline : AggregationStage) -> AggregationPipeline:
        return cls(pipeline)