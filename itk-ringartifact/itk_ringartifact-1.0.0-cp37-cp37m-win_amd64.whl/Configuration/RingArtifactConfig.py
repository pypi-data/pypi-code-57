depends = ('ITKPyBase', 'ITKFFT', 'ITKCommon', )
templates = (
  ('FourierStripeArtifactImageFilter', 'itk::FourierStripeArtifactImageFilter', 'itkFourierStripeArtifactImageFilterIF2', True, 'itk::Image< float,2 >'),
  ('FourierStripeArtifactImageFilter', 'itk::FourierStripeArtifactImageFilter', 'itkFourierStripeArtifactImageFilterID2', True, 'itk::Image< double,2 >'),
  ('FourierStripeArtifactImageFilter', 'itk::FourierStripeArtifactImageFilter', 'itkFourierStripeArtifactImageFilterIF3', True, 'itk::Image< float,3 >'),
  ('FourierStripeArtifactImageFilter', 'itk::FourierStripeArtifactImageFilter', 'itkFourierStripeArtifactImageFilterID3', True, 'itk::Image< double,3 >'),
)
snake_case_functions = ('fourier_stripe_artifact_image_filter', )
