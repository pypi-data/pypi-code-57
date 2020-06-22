#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 10/06/2020
           '''

def ignore_test():
  import torch
  import torch.nn as nn

  class MyModule(nn.Module):
    @torch.jit.ignore
    def debugger(self, x):
      import pdb
      pdb.set_trace()

    def forward(self, x):
      x += 10
      # The compiler would normally try to compile `debugger`,
      # but since it is `@ignore`d, it will be left as a call
      # to Python
      self.debugger(x)
      return x

  m = torch.jit.script(MyModule())

  # Error! The call `debugger` cannot be saved since it calls into Python
  m.save("m.pt")


def unused_test():
  import torch
  import torch.nn as nn

  class MyModule(nn.Module):
    def __init__(self, use_memory_efficent):
      super(MyModule, self).__init__()
      self.use_memory_efficent = use_memory_efficent

    @torch.jit.unused
    def memory_efficient(self, x):
      import pdb
      pdb.set_trace()
      return x + 10

    def forward(self, x):
      # Use not-yet-scriptable memory efficient mode
      if self.use_memory_efficient:
        return self.memory_efficient(x)
      else:
        return x + 10

  m = torch.jit.script(MyModule(use_memory_efficent=False))
  m.save("m.pt")

  m = torch.jit.script(MyModule(use_memory_efficient=True))
  # exception raised
  m(torch.rand(100))

def export_func_jit_test():
  import torch
  import torch.nn as nn

  class MyModule(nn.Module):
    def implicitly_compiled_method(self, x):
      return x + 99

    # `forward` is implicitly decorated with `@torch.jit.export`,
    # so adding it here would have no effect
    def forward(self, x):
      return x + 10

    @torch.jit.export
    def another_forward(self, x):
      # When the compiler sees this call, it will compile
      # `implicitly_compiled_method`
      return self.implicitly_compiled_method(x)

    def unused_method(self, x):
      return x - 20

  # `m` will contain compiled methods:
  #     `forward`
  #     `another_forward`
  #     `implicitly_compiled_method`
  # `unused_method` will not be compiled since it was not called from
  # any compiled methods and wasn't decorated with `@torch.jit.export`
  m = torch.jit.script(MyModule())


def all_test():
  # Same behavior as pre-PyTorch 1.2
  @torch.jit.script
  def some_fn():
    return 2

  # Marks a function as ignored, if nothing
  # ever calls it then this has no effect
  @torch.jit.ignore
  def some_fn2():
    return 2

  # As with ignore, if nothing calls it then it has no effect.
  # If it is called in script it is replaced with an exception.
  @torch.jit.unused
  def some_fn3():
    import pdb; pdb.set_trace()
    return 4

  # Doesn't do anything, this function is already
  # the main entry point
  @torch.jit.export
  def some_fn4():
    return 2

def global_disable_jit_annotation_test():
  ''' globally jit ignore '''
  #PYTORCH_JIT=0 python disable_jit_example.py

  @torch.jit.script
  def scripted_fn(x : torch.Tensor):

    for i in range(12):
      x = x + x

    return x

  def fn(x):
    x = torch.neg(x)
    import pdb
    pdb.set_trace()
    return scripted_fn(x)

  traced_fn = torch.jit.trace(fn, (torch.rand(4, 5),))
  traced_fn(torch.rand(3, 4))


def test_user_defined_classes_jit():
  import torch

  @torch.jit.script
  def foo(x, y):
    if x.max() > y.max():
      r = x
    else:
      r = y
    return r

  print(type(foo))  # torch.jit.ScriptFuncion

  # See the compiled graph as Python code
  print(foo.code)

  # Call the function using the TorchScript interpreter
  foo(torch.ones(2, 2), torch.ones(2, 2))


if __name__ == '__main__':
    test_user_defined_classes_jit()
