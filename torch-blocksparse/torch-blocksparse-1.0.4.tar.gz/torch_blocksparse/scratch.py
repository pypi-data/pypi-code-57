import torch_blocksparse
import torch
from torch.utils.cpp_extension import load_inline

source = '''
#include <iostream>

at::Tensor load_balance(at::Tensor layout) {
  size_t H = layout.size(0);
  size_t M = layout.size(1);
  size_t N = layout.size(2);
  at::Tensor ret = at::zeros_like(layout);
  for(size_t h = 0; h < H; h++)
  for(size_t m = 0; m < M; m++)
  for(size_t n = 0; n < N; n++){
    int v = layout[h][m][n].item<int>();
    if(v == 0)
      continue;
    int topleft  = (m > 0) && (n > 0) ? ret[h][m-1][n-1].item<int>() : 0;
    int top      = (m > 0)            ? ret[h][m-1][n].item<int>() : 0;
    int left     = (n > 0)            ? ret[h][m][n-1].item<int>() : 0;
    int width    = std::min(left, std::min(top, topleft)) + 1;
    ret[h][m][n] = width;
    if(width == 4){
    int firstm = m - width + 1;
    int firstn = n - width + 1;
    for(size_t mm = firstm; mm <= m; mm++)
    for(size_t nn = firstn; nn <= n; nn++){
        layout[h][mm][nn] = 0;
        ret[h][mm][nn] = 0;
    }
    m = firstm;
    n = firstn;
    }
  }
  return ret;
}
'''

block = 16
L = 256
stride = 128
layout = torch_blocksparse.MultiheadAttention._make_layout(1, L // block, 'fixed', stride // block, True, 1, 1)
module = load_inline(name='load_balance',
                    cpp_sources=[source],
                    functions=['load_balance'])
balanced = module.load_balance(layout)
print(layout)
print(balanced)