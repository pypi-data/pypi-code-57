from ai_harness.configclasses import configclass, field
from ai_harness.configuration import Arguments
from .tasks import NewsSegmentTask, SentimentTask, \
    NewsClassification_WordAVGModel, NewsClassification_RNN, NewsClassfiction_CNN

TASKS = dict([
    ('news', NewsSegmentTask),
    ('sentiment', SentimentTask)
])


@configclass()
class TaskRunArguments:
    task: str = field('news', 'specified the task name: ' + str(TASKS.keys()))
    action: str = field('train', 'specified the action name: train')
    type: str = field('bert_base', 'specified the action name: bert_base, distil_bert, electra_base,electra_small')


def run(args):
    task = TASKS.get(args.task)()
    type = args.type

    eval('task.' + args.action + '(type)')


if __name__ == "__main__":
    run(Arguments(TaskRunArguments()).parse())
