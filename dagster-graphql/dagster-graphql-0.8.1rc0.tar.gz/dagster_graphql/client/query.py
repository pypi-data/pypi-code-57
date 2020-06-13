STEP_EVENT_FRAGMENTS = '''
fragment eventMetadataEntryFragment on EventMetadataEntry {
  __typename
  label
  description
  ... on EventPathMetadataEntry {
    path
  }
  ... on EventJsonMetadataEntry {
    jsonString
  }
  ... on EventUrlMetadataEntry {
    url
  }
  ... on EventTextMetadataEntry {
    text
  }
  ... on EventMarkdownMetadataEntry {
    mdStr
  }
  ... on EventPythonArtifactMetadataEntry {
    module
    name
  }
}

fragment errorFragment on PythonError {
  message
  stack
  className
  cause {
    message
    stack
    className
    cause {
      message
      stack
      className
    }
  }
}


fragment stepEventFragment on StepEvent {
  step {
    key
    inputs {
      name
      type {
        key
      }
      dependsOn {
        key
      }
    }
    outputs {
      name
      type {
        key
      }
    }
    solidHandleID
    kind
    metadata {
      key
      value
    }
  }
  ... on MessageEvent {
    runId
    message
    timestamp
    level
  }
  ... on StepExpectationResultEvent {
    expectationResult {
      success
      label
      description
      metadataEntries {
        ...eventMetadataEntryFragment
      }
    }
  }
  ... on StepMaterializationEvent {
    materialization {
      label
      description
      metadataEntries {
        ...eventMetadataEntryFragment
      }
    }
  }
  ... on ExecutionStepInputEvent {
    inputName
    typeCheck {
      __typename
      success
      label
      description
      metadataEntries {
        ...eventMetadataEntryFragment
      }
    }
  }
  ... on ExecutionStepOutputEvent {
    outputName
    typeCheck {
      __typename
      success
      label
      description
      metadataEntries {
        ...eventMetadataEntryFragment
      }
    }
  }
  ... on ExecutionStepFailureEvent {
    error {
      ...errorFragment
    }
    failureMetadata {
      label
      description
      metadataEntries {
        ...eventMetadataEntryFragment
      }
    }
  }
  ... on ExecutionStepUpForRetryEvent {
    retryError: error {
      ...errorFragment
    }
    secondsToWait
  }
  ... on EngineEvent {
    metadataEntries {
      ...eventMetadataEntryFragment
    }
    markerStart
    markerEnd
    engineError: error {
      ...errorFragment
    }
  }
}
'''

MESSAGE_EVENT_FRAGMENTS = (
    '''
fragment messageEventFragment on MessageEvent {
  runId
  message
  timestamp
  level
  ...stepEventFragment
  ... on PipelineInitFailureEvent {
    initError: error {
      ...errorFragment
    }
  }
}
'''
    + STEP_EVENT_FRAGMENTS
)


EXECUTE_RUN_IN_PROCESS_RESULT_FRAGMENT = '''
fragment executeRunInProcessResultFragment on ExecuteRunInProcessResult {
	__typename
	... on InvalidStepError {
		invalidStepKey
	}
	... on InvalidOutputError {
		stepKey
		invalidOutputName
	}
	... on PipelineConfigValidationInvalid {
    pipelineName
		errors {
			__typename
			message
			path
			reason
		}
	}
	... on PipelineNotFoundError {
		message
		pipelineName
	}
  ... on PythonError {
    message
    stack
  }
	... on ExecuteRunInProcessSuccess {
		run {
			runId
			status
			pipeline {
				name
			}
			runConfigYaml
			mode
		}
	}
}
'''

EXECUTE_RUN_IN_PROCESS_MUTATION = (
    '''
mutation(
  $repositoryLocationName: String!
  $repositoryName: String!
  $runId: String!
) {
  executeRunInProcess(
    repositoryLocationName: $repositoryLocationName
    repositoryName: $repositoryName
    runId: $runId
  ) {
    ...executeRunInProcessResultFragment
  }
}
'''
    + EXECUTE_RUN_IN_PROCESS_RESULT_FRAGMENT
)

EXECUTE_PLAN_MUTATION = (
    '''
mutation(
  $executionParams: ExecutionParams!
) {
  executePlan(
    executionParams: $executionParams,
  ) {
    __typename
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      message
      stack
    }
    ... on ExecutePlanSuccess {
      pipeline {
        name
      }
      hasFailures
      stepEvents {
        __typename
        ...stepEventFragment
      }
    }
  }
}
'''
    + STEP_EVENT_FRAGMENTS
)

RAW_EXECUTE_PLAN_MUTATION = '''
mutation(
  $executionParams: ExecutionParams!
) {
  executePlan(
    executionParams: $executionParams,
  ) {
    __typename
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      message
      stack
      cause {
          message
          stack
      }
    }
    ... on ExecutePlanSuccess {
      pipeline {
        name
      }
      hasFailures
      rawEventRecords
    }
  }
}
'''

SUBSCRIPTION_QUERY = (
    MESSAGE_EVENT_FRAGMENTS
    + '''
subscription subscribeTest($runId: ID!) {
    pipelineRunLogs(runId: $runId) {
        __typename
        ... on PipelineRunLogsSubscriptionSuccess {
            run {
              runId
            },
            messages {
                __typename
                ...messageEventFragment
            }
        }
        ... on PipelineRunLogsSubscriptionFailure {
            missingRunId
        }
    }
}
'''
)

LAUNCH_PIPELINE_EXECUTION_MUTATION = '''
mutation(
  $executionParams: ExecutionParams!
) {
  launchPipelineExecution(
    executionParams: $executionParams,
  ) {
    __typename
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on InvalidOutputError {
      stepKey
      invalidOutputName
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      message
      stack
    }
    ... on LaunchPipelineRunSuccess {
      run {
        runId
        status
        pipeline {
          name
        }
        runConfigYaml
        mode
      }
    }
  }
}
'''


LAUNCH_PIPELINE_REEXECUTION_MUTATION = '''
mutation(
  $executionParams: ExecutionParams!
) {
  launchPipelineReexecution(
    executionParams: $executionParams,
  ) {
    __typename
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on InvalidOutputError {
      stepKey
      invalidOutputName
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      message
      stack
    }
    ... on LaunchPipelineRunSuccess {
      run {
        runId
        status
        pipeline {
          name
        }
        runConfigYaml
        mode
      }
    }
  }
}
'''
