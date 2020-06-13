# -*- coding: utf-8 -*-
from typing import Union
import time

class Sequence(object):
  
  twepoch: Union[int] = 1288834974657
  
  worker_id_bits: Union[int] = 5
  datacenter_id_bits: Union[int] = 5
  max_worker_id: Union[int] = -1 ^ (-1 << worker_id_bits)
  max_datacenter_id: Union[int] = -1 ^ (-1 << datacenter_id_bits)
  
  sequence_bits: Union[int] = 12
  worker_id_shift: Union[int] = sequence_bits
  datacenter_id_shift: Union[int] = sequence_bits + worker_id_bits
  
  timestamp_left_shift = sequence_bits + worker_id_bits + datacenter_id_bits
  sequence_mark: Union[int] = -1 ^ (-1 << sequence_bits)
  
  worker_id: Union[int]
  datacenter_id: Union[int]
  sequence: Union[int] = 0
  last_timestamp: Union[int] = 1
  
  def __init__(self, datacenter_id: Union[int], worker_id: Union[int]):
    self.datacenter_id = datacenter_id
    self.worker_id = worker_id
  
  def time_gen(self) -> Union[int]:
    return int(time.time() * 1000)
  
  def get_next_millis(self) -> Union[int]:
    while True:
      if (t := self.time_gen()) > self.last_timestamp:
        return t
        
  
  def next_id(self) -> Union[int]:
    timestamp = self.time_gen()
    if timestamp < self.last_timestamp:
      raise Exception('clock is moving backwards. Rejecting requests until %d.'.format(self.last_timestamp))
    
    if timestamp == self.last_timestamp:
      self.sequence = (self.sequence + 1) & self.sequence_mark
      if self.sequence == 0:
        timestamp = self.get_next_millis()
    else:
      self.sequence = 0
    
    self.last_timestamp = timestamp

    return (timestamp - self.twepoch) << self.timestamp_left_shift |\
           (self.datacenter_id << self.datacenter_id_shift) |\
           (self.worker_id << self.worker_id_shift) |\
           self.sequence

def sequence(datacenter_id,  worker_id):
  s = Sequence(datacenter_id, worker_id)
  while True:
    yield s.next_id()

if __name__ == "__main__":
  s = sequence(1, 1)
  print(next(s))
  print(next(s))
  print(next(s))