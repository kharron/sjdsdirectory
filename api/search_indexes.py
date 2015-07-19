import datetime
from haystack import indexes
from admin.models import Businesses

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
		text = indexes.CharField(document=True, use_template=true)

		def get_model(self):
				return Business

		def 
