from src.datascience import logger
from src.datascience.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.datascience.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.datascience.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline

logger.info('Welcome to the Data Science Project Template!')

STAGE_NAME = 'Data Ingestion Stage'

if __name__ == '__main__':
    try:
        logger.info(f'>>>>>> stage {STAGE_NAME} started <<<<<<')
        data_ingestion = DataIngestionTrainingPipeline()
        data_ingestion.initiate_data_ingestion()
        logger.info(f'>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x')
    except Exception as e:
        logger.exception(e)
        raise e
    


# Stage 2 - Data Validation
STAGE_NAME = 'Data Validation Stage'
try:
    logger.info(f'>>>>>> stage {STAGE_NAME} started <<<<<<')
    obj = DataValidationTrainingPipeline()
    obj.main()
    logger.info(f'>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x')
except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Data Transformation Stage"
try:
    logger.info(f'>>>>>> stage {STAGE_NAME} started <<<<<<')
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.main()
    logger.info(f'>>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x')
except Exception as e:
    logger.exception(e)
    raise e
