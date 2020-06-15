#!/usr/bin/env python
# coding=utf-8
import numpy as np
import tqdm

from abc import ABCMeta, abstractmethod

class Evaluation_Base(metaclass=ABCMeta):
    
    __slots__ = ['num_ent', 'num_rel']
    
    def __init__(self, num_entities, num_relstions):
        self.num_ent = num_entities
        self.num_rel = num_relstions
         
    @staticmethod
    def __generate_graph(data):
        data_set = {}
        pairs = set()
        for triplet in data:
            src, rel, dst = triplet
            if (src, rel) in pairs:
                data_set[(src, rel)].append(dst)
            else:
                pairs.add((src, rel))
                data_set[(src, rel)] = [dst]
        return data_set, np.array([[x[0], x[1]] for x in pairs])
    
    @abstractmethod
    def calculate(self, target_function, data=None, batch_size=512, filters=None):
        pass
    
    @staticmethod
    def sort_ranks(socres, targets):
        return np.array([np.sum(socres - socres[x] >= 0) for x in targets])
    
    def __call__(self, target_function, train_data, test_data, batch_size=512):
        train_pair_dict, _ = self.__generate_graph(train_data)
        
        print('Calculate the ranks of predicted tails (dst)')
        pred_tail_ranks = self.calculate(target_function,
                                         test_data, batch_size=512,
                                         filters=train_pair_dict)
            
        src, rel, dst = test_data.transpose(1, 0)
        test_data = np.stack((dst, rel + self.num_rel, src)).transpose(1, 0)
        print('Calculate the ranks of predicted heads (src)')
        pred_head_ranks = self.calculate(target_function,
                                         test_data, batch_size=512,
                                         filters=train_pair_dict)
        return pred_tail_ranks, pred_head_ranks
        
class Evaluate_Triplet(Evaluation_Base):
    
    def calculate(self, target_function, data, batch_size=512, filters=None):
        data = self.__generate_graph(data)
        num_batchs = self.num_ent // batch_size + 1
        ranks, franks = [], []
        for pair in tqdm.tqdm(data[1]):
            scores = np.zeros(self.num_ent)
            fscores = np.zeros(self.num_ent)
            new_pairs = np.tile(pair.reshape((1, -1)), (self.num_ent, 3))
            new_tails = np.arange(self.num_ent).reshape((-1, 1))
            new_triplets = np.concatenate((new_pairs, new_tails), 1)
            
            for i in range(num_batchs):
                i = i * batch_size
                score = target_function(new_triplets[i: i + batch_size, :])
                scores[i: i + batch_size] += score
                fscores[i: i + batch_size] += score
            
            if filters is not None:
                
                # 训练数据可能与测试数据有交集 ！！！ 代码未添加
                
                fscores[filters[(pair[0], pair[1])]] = np.min(fscores)
            rank = self.sort_ranks(scores, data[0][(pair[0], pair[1])])
            frank = self.sort_ranks(fscores, data[0][(pair[0], pair[1])])
            for i in rank:
                ranks.append(i)
            for i in frank:
                franks.append(i)
        del data
        return ranks, franks
   
class Evaluate_Pair(Evaluation_Base):
    
    def calculate(self, target_function, data, batch_size=512, filters=None):
        data = self.__generate_graph(data)
        ranks, franks = [], []
        for pair in tqdm.tqdm(data[1]):
            scores = np.zeros(self.num_ent)
            fscores = np.zeros(self.num_ent)
            
            score = target_function(pair.reshape((1, -1)))
            scores += score
            fscores += score
            
            if filters is not None:
                
                # 训练数据可能与测试数据有交集 ！！！ 代码未添加
                
                fscores[filters[(pair[0], pair[1])]] = np.min(fscores)
            rank = self.sort_ranks(scores, data[0][(pair[0], pair[1])])
            frank = self.sort_ranks(fscores, data[0][(pair[0], pair[1])])
            for i in rank:
                ranks.append(i)
            for i in frank:
                franks.append(i)
        del data
        return ranks, franks

def hits_at_n_score(ranks, n):
    r"""Hits@N

    The function computes how many elements of a vector of rankings ``ranks`` make it to the top ``n`` positions.

    It can be used in conjunction with the learning to rank evaluation protocol of
    :meth:`ampligraph.evaluation.evaluate_performance`.

    It is formally defined as follows:

    .. math::

        Hits@N = \sum_{i = 1}^{|Q|} 1 \, \text{if } rank_{(s, p, o)_i} \leq N

    where :math:`Q` is a set of triples and :math:`(s, p, o)` is a triple :math:`\in Q`.


    Consider the following example. Each of the two positive triples identified by ``*`` are ranked
    against four corruptions each. When scored by an embedding model, the first triple ranks 2nd, and the other triple
    ranks first. Hits@1 and Hits@3 are: ::

        s	 p	   o		score	rank
        Jack   born_in   Ireland	0.789	   1
        Jack   born_in   Italy		0.753	   2  *
        Jack   born_in   Germany	0.695	   3
        Jack   born_in   China		0.456	   4
        Jack   born_in   Thomas		0.234	   5

        s	 p	   o		score	rank
        Jack   friend_with   Thomas	0.901	   1  *
        Jack   friend_with   China      0.345	   2
        Jack   friend_with   Italy      0.293	   3
        Jack   friend_with   Ireland	0.201	   4
        Jack   friend_with   Germany    0.156	   5

        Hits@3=1.0
        Hits@1=0.5


    Parameters
    ----------
    ranks: ndarray or list, shape [n] or [n,2]
        Input ranks of n test statements.
    n: int
        The maximum rank considered to accept a positive.

    Returns
    -------
    hits_n_score: float
        The Hits@n score

    Examples
    --------
    >>> import numpy as np
    >>> from metrics import hits_at_n_score
    >>> rankings = np.array([1, 12, 6, 2])
    >>> hits_at_n_score(rankings, n=3)
    0.5
    """
    if isinstance(ranks, list):
        ranks = np.asarray(ranks)
    ranks = ranks.reshape(-1)
    return np.sum(ranks <= n) / len(ranks)


def mrr_score(ranks):
    r"""Mean Reciprocal Rank (MRR)

    The function computes the mean of the reciprocal of elements of a vector of rankings ``ranks``.

    It is used in conjunction with the learning to rank evaluation protocol of
    :meth:`ampligraph.evaluation.evaluate_performance`.

    It is formally defined as follows:

    .. math::

        MRR = \frac{1}{|Q|}\sum_{i = 1}^{|Q|}\frac{1}{rank_{(s, p, o)_i}}

    where :math:`Q` is a set of triples and :math:`(s, p, o)` is a triple :math:`\in Q`.

    .. note::
        This metric is similar to mean rank (MR) :meth:`ampligraph.evaluation.mr_score`. Instead of averaging ranks,
        it averages their reciprocals. This is done to obtain a metric which is more robust to outliers.


    Consider the following example. Each of the two positive triples identified by ``*`` are ranked
    against four corruptions each. When scored by an embedding model, the first triple ranks 2nd, and the other triple
    ranks first. The resulting MRR is: ::

        s	 p	   o		score	rank
        Jack   born_in   Ireland	0.789	   1
        Jack   born_in   Italy		0.753	   2  *
        Jack   born_in   Germany	0.695	   3
        Jack   born_in   China		0.456	   4
        Jack   born_in   Thomas		0.234	   5

        s	 p	   o		score	rank
        Jack   friend_with   Thomas	0.901	   1  *
        Jack   friend_with   China      0.345	   2
        Jack   friend_with   Italy      0.293	   3
        Jack   friend_with   Ireland	0.201	   4
        Jack   friend_with   Germany    0.156	   5

        MRR=0.75

    Parameters
    ----------
    ranks: ndarray or list, shape [n] or [n,2]
        Input ranks of n test statements.

    Returns
    -------
    mrr_score: float
        The MRR score

    Examples
    --------
    >>> import numpy as np
    >>> from metrics import mrr_score
    >>> rankings = np.array([1, 12, 6, 2])
    >>> mrr_score(rankings)
    0.4375

    """
    if isinstance(ranks, list):
        ranks = np.asarray(ranks)
    ranks = ranks.reshape(-1)
    return np.sum(1 / ranks) / len(ranks)


def rank_score(y_true, y_pred, num_entities=None, pos_lab=1):
    """Rank of a triple

        The rank of a positive element against a list of negatives.

    .. math::

        rank_{(s, p, o)_i}

    Parameters
    ----------
    y_true : ndarray, shape [n]
        An array of binary labels. The array only contains one positive.
    y_pred : ndarray, shape [n]
        An array of scores, for the positive element and the n-1 negatives.
    pos_lab : int
        The value of the positive label (default = 1).

    Returns
    -------
    rank : int
        The rank of the positive element against the negatives.

    Examples
    --------
    >>> import numpy as np
    >>> from metrics import rank_score
    >>> y_pred = np.array([.434, .65, .21, .84])
    >>> y_true = np.array([0, 0, 1, 0])
    >>> rank_score(y_true, y_pred)
    np.array([4])
    """
    def _rank(x, y):
        return x - y
    
    if num_entities is not None:
        y_true_bin = np.zeros(num_entities)
        y_true_bin[y_true] = 1
    else:
        y_true_bin = y_true
    idx = np.argsort(y_pred)[::-1]
    y_ord = y_true_bin[idx]
    rank = np.where(y_ord == pos_lab)[0] + 1
    rank = np.sort(rank)
    rank_idx = np.arange(rank.shape[0])
    return rank - rank_idx


def mr_score(ranks):
    r"""Mean Rank (MR)

    The function computes the mean of of a vector of rankings ``ranks``.

    It can be used in conjunction with the learning to rank evaluation protocol of
    :meth:`ampligraph.evaluation.evaluate_performance`.

    It is formally defined as follows:

    .. math::
        MR = \frac{1}{|Q|}\sum_{i = 1}^{|Q|}rank_{(s, p, o)_i}

    where :math:`Q` is a set of triples and :math:`(s, p, o)` is a triple :math:`\in Q`.

    .. note::
        This metric is not robust to outliers.
        It is usually presented along the more reliable MRR :meth:`ampligraph.evaluation.mrr_score`.

    Consider the following example. Each of the two positive triples identified by ``*`` are ranked
    against four corruptions each. When scored by an embedding model, the first triple ranks 2nd, and the other triple
    ranks first. The resulting MR is: ::

        s	 p	   o		score	rank
        Jack   born_in   Ireland	0.789	   1
        Jack   born_in   Italy		0.753	   2  *
        Jack   born_in   Germany	0.695	   3
        Jack   born_in   China		0.456	   4
        Jack   born_in   Thomas		0.234	   5

        s	 p	   o		score	rank
        Jack   friend_with   Thomas	0.901	   1  *
        Jack   friend_with   China      0.345	   2
        Jack   friend_with   Italy      0.293	   3
        Jack   friend_with   Ireland	0.201	   4
        Jack   friend_with   Germany    0.156	   5

        MR=1.5

    Parameters
    ----------
    ranks: ndarray or list, shape [n] or [n,2]
        Input ranks of n test statements.

    Returns
    -------
    mr_score: float
        The MR score

    Examples
    --------
    >>> from metrics import mr_score
    >>> ranks= [5, 3, 4, 10, 1]
    >>> mr_score(ranks)
    4.6
    """

    if isinstance(ranks, list):
        ranks = np.asarray(ranks)
    ranks = ranks.reshape(-1)
    return np.sum(ranks) / len(ranks)