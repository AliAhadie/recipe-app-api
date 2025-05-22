from rest_framework import serializers
from recipe.models import Recipe, Tag


class Tagserializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    tags = Tagserializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """create recipe."""
        tags = validated_data.pop("tags", [])
        auth_user = self.context["request"].user
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            tag_obj, _ = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:  # Allow clearing tags if an empty list is provided
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(user=instance.user, **tag_data)
                instance.tags.add(tag)
        return instance        


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
