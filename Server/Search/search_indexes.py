from .models import GameInfo
from haystack import indexes


class GameInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True,model_attr='name')

    def get_model(self):
        return GameInfo

    def index_queryset(self, using=None):
        """
        used when the entire index for model is updated.
        """
        return self.get_model().objects.all()  # 确定在建立索引时有些记录被索引，这里我们简单的返回所有记录