#!/usr/bin/env python3

# Copyright 2020 kubeflow.org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from kfp.compiler.main import main as kfp_compiler_main
# from kfp.compiler.main import compile_pyfile as kfp_compile_pyfile
# from typing import List

from kfp_tekton.compiler.main import compile_pyfile as kfptekton_compile_pyfile


# from kfp_tekton.compiler import monkey_patch


# for dev test only
if __name__ == '__main__':
    # monkey_patch()

    # debug for development
    project_root = "/Users/ckadner/PycharmProjects/kfp-tekton_ckadner"
    pyfile = f"{project_root}/sdk/python/tests/compiler/testdata/parallel_join.py"
    output = f"{project_root}/sdk/python/tests/compiler/testdata/parallel_join_embedded.yaml"
    #
    # pyfile = './build/kubeflow/pipelines/samples/contrib/seldon/mnist_tf.py'
    # output = './temp/pipeline.yaml'

    kfptekton_compile_pyfile(pyfile=pyfile, function_name=None, output_path=output, type_check=True)


# cat <<EOF |kubectl apply -f -
# apiVersion: rbac.authorization.k8s.io/v1beta1
# kind: ClusterRoleBinding
# metadata:
#   name: default-admin
# subjects:
#   - kind: ServiceAccount
#     name: default
#     namespace: kubeflow
# roleRef:
#   kind: ClusterRole
#   name: cluster-admin
#   apiGroup: rbac.authorization.k8s.io
# EOF
