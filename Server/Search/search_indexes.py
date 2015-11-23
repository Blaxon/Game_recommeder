from .models import GameInfo
from haystack import indexes


class GameInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, model_attr='name')
    name = indexes.CharField(model_attr='name')
    simple_intro = indexes.CharField(model_attr='simple_intro')
    type = indexes.CharField(model_attr='type')
    language = indexes.CharField(model_attr='language')
    display = indexes.CharField(model_attr='display')
    theme = indexes.CharField(model_attr='theme')
    company = indexes.CharField(model_attr='company')
    time = indexes.CharField(model_attr='time')
    tag = indexes.CharField(model_attr='tag')
    player_vote = indexes.CharField(model_attr='player_vote')
    game_score = indexes.FloatField(model_attr='score')  # attention score in model change into game_score
    introduction = indexes.CharField(model_attr='introduction')
    picture = indexes.CharField(model_attr='picture')

    def get_model(self):
        return GameInfo

    def index_queryset(self, using=None):
        """
        used when the entire index for model is updated.
        """
        return self.get_model().objects.all()  # 确定在建立索引时有些记录被索引，这里我们简单的返回所有记录