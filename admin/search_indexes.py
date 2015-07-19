import datetime
from haystack import indexes
from admin.models import Business

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
		text = indexes.CharField(document=True, use_template=true)

		def get_model(self):
				return Business

		def index_queryset(self):
				return self.get_model().objects.all()
