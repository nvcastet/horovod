# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import subprocess
import sys

def is_mx_cuda():
    try:
        from mxnet import runtime
        features = runtime.Features()
        return features.is_enabled('CUDA')
    except Exception:
        if 'linux' in sys.platform:
            try:
                import mxnet as mx
                mx_libs = mx.libinfo.find_lib_path()
                for mx_lib in mx_libs:
                    output = subprocess.check_output(['readelf', '-d', mx_lib])
                    if 'cuda' in str(output):
                        return True
                return False
            except Exception:
                return False
    return False

def is_mx_mkldnn():
    try:
        from mxnet import runtime
        features = runtime.Features()
        return features.is_enabled('MKLDNN')
    except Exception:
        msg = 'INFO: Cannot detect if MKLDNN is enabled in MXNet. Please \
            set MXNET_USE_MKLDNN=1 if MKLDNN is enabled in your MXNet build.'
        if 'linux' not in sys.platform:
            # MKLDNN is only enabled by default in MXNet Linux build. Return
            # False by default for non-linux build but still allow users to
            # enable it by using MXNET_USE_MKLDNN env variable.
            print(msg)
            return os.environ.get('MXNET_USE_MKLDNN', '0') == '1'
        else:
            try:
                import mxnet as mx
                mx_libs = mx.libinfo.find_lib_path()
                for mx_lib in mx_libs:
                    output = subprocess.check_output(['readelf', '-d', mx_lib])
                    if 'mkldnn' in str(output):
                        return True
                return False
            except Exception:
                print(msg)
                return os.environ.get('MXNET_USE_MKLDNN', '0') == '1'
