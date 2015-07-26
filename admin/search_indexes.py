import datetime
from haystack import indexes
from admin.models import Business

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
		text = indexes.CharField(document=True, use_template=True)
		name = indexes.CharField(model_attr='name')
		description = indexes.CharField(model_attr='description')

		def get_model(self):
				return Business

		def index_queryset(self, using=None):
				return self.get_model().objects.all()
	
class ProductIndex(indexes.SearchIndex, indexes.Indexable):
		text = indexes.CharField(document=True, use_template=True)
		name = indexes.CharField(model_attr='name')

		def get_model(self):
				return Products

		def index_queryset(self, using=None):
				''' Return a list of businesses related to a product '''

