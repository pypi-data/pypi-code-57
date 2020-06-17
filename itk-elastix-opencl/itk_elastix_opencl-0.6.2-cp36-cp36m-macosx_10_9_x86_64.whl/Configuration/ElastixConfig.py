depends = ('ITKPyBase', 'ITKSmoothing', 'ITKImageSources', 'ITKImageGrid', 'ITKIOImageBase', 'ITKCommon', )
templates = (
  ('ParameterObject', 'elastix::ParameterObject', 'elastixParameterObject', False),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('ElastixRegistrationMethod', 'itk::ElastixRegistrationMethod', 'itkElastixRegistrationMethodID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterIF2', True, 'itk::Image< float,2 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterIF3', True, 'itk::Image< float,3 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterID2', True, 'itk::Image< double,2 >'),
  ('TransformixFilter', 'itk::TransformixFilter', 'itkTransformixFilterID3', True, 'itk::Image< double,3 >'),
)
snake_case_functions = ('elastix_registration_method', 'transformix_filter', )
