#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################

import multiprocessing


def foo(queue_in, queue_out, index):
    text, data_loader = queue_in.get()

    data, _, _ = data_loader[index]
    value = data["in2"].value

    queue_out.put("hello " + text + " {}".format(value))
    queue_in.task_done()


class Algorithm:
    def prepare(self, data_loaders):
        data_loader = data_loaders.loaderOf("in2")

        data, _, _ = data_loader[0]
        self.offset = data["in2"].value

        return True

    def process(self, inputs, data_loaders, outputs):
        data_loader = data_loaders.loaderOf("in2")

        for i in range(data_loader.count()):
            data, _, _ = data_loader[i]
            data["in2"].value

        num_thread = data_loader.count()

        queue_in = multiprocessing.JoinableQueue(num_thread)
        queue_out = []

        # Start worker processes
        jobs = []
        for i in range(num_thread):
            queue_out.append(multiprocessing.Queue())
            p = multiprocessing.Process(target=foo, args=(queue_in, queue_out[i], i))
            jobs.append(p)
            p.start()

        # Add None to the queue to kill the workers
        for task in range(num_thread):
            queue_in.put(("test {}".format(task), data_loader))

        # Wait for all the tasks to finish
        queue_in.join()

        outputs["out"].write({"value": inputs["in1"].data.value + self.offset})

        return True
