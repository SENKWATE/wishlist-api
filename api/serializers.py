from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name',]

class ItemListSerializer(serializers.ModelSerializer):
	fav_count = serializers.SerializerMethodField()
	added_by = UserSerializer()
	detail = serializers.HyperlinkedIdentityField(
		view_name = "api-detail",
		lookup_field = "id",
		lookup_url_kwarg = "item_id"
		)
	
	class Meta:
		model = Item
		fields = [
			'name',
			'added_by',
			'detail',
			'fav_count',
			]
	def get_fav_count(self, obj):
		return obj.favoriteitem_set.count()

class ItemDetailSerializer(serializers.ModelSerializer):
	favorited_users = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = [
			'name',
			'description',
			'favorited_users',
			]
	def get_favorited_users(self, obj):
		 favs = obj.favoriteitem_set.all()
		 return FavoriteItemSerializer(favs, many=True).data

class FavoriteItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = FavoriteItem
		fields = ['user',]