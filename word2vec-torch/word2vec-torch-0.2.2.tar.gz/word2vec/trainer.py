import torch
import torch.optim as optim
from torch.utils.data import DataLoader, sampler
from tqdm import tqdm
from data_reader import Word2vecDataset
from model import SkipGramModel


class Word2VecTrainer:
    def __init__(self, input_file, output_file, side_num=1, neg_num=5, sentences_count=100000, emb_size=[1000000,],
                 emb_dimension=100, batch_size=32, iterations=3,
                 initial_lr=0.001):

        # self.data = DataReader(input_file, min_count)
        dataset = Word2vecDataset(input_file, side_num=side_num , neg_num=neg_num , sentences_count=sentences_count)
        self.dataloader = DataLoader(dataset, batch_size=batch_size,
                                     shuffle=False, num_workers=1, collate_fn=dataset.collate)

        self.output_file_name = output_file
        self.emb_size = emb_size
        self.emb_dimension = emb_dimension
        self.batch_size = batch_size
        self.iterations = iterations
        self.initial_lr = initial_lr
        self.skip_gram_model = SkipGramModel(self.emb_size, self.emb_dimension)
        # print('parameters:',self.skip_gram_model.parameters())

        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        if self.use_cuda:
            self.skip_gram_model.cuda()

    def train(self):

        for iteration in range(self.iterations):

            print("\n\n\nIteration: " + str(iteration + 1))
            optimizer = optim.SparseAdam(self.skip_gram_model.parameters(), lr=self.initial_lr)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, len(self.dataloader))

            running_loss = 0.0
            for i, sample_batched in enumerate(tqdm(self.dataloader)):

                if len(sample_batched[0]) > 1:
                    pos_u = sample_batched[0].to(self.device)
                    pos_v = sample_batched[1].to(self.device)
                    neg_v = sample_batched[2].to(self.device)

                    scheduler.step()
                    optimizer.zero_grad()
                    loss = self.skip_gram_model.forward(pos_u, pos_v, neg_v)
                    loss.backward()
                    optimizer.step()

                    running_loss = running_loss * 0.9 + loss.item() * 0.1
                    if i<=1 or i % 500 == 0:
                        print(" Loss: " + str(running_loss))

            self.skip_gram_model.save_embedding(self.output_file_name)


if __name__ == '__main__':
    w2v = Word2VecTrainer(input_file="input.txt2", output_file="out.vec2",side_num=1, neg_num=2, sentences_count=3, emb_size=[100,],batch_size=1)
    w2v.train()
