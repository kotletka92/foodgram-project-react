import base64
import uuid

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from recipes.models import Recipe


def post(request, pk, model, serializer):
    recipe = get_object_or_404(Recipe, id=pk)
    if model.objects.filter(author=request.user, recipe=recipe).exists():
        return Response(
            {'errors': 'Recipe has already been added'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    instance = model(recipe=recipe, author=request.user)
    instance.save()
    serializer = serializer(
            get_object_or_404(Recipe, id=pk), context={"request": request}
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete(request, pk, model):
    recipe = get_object_or_404(Recipe, id=pk)
    if model.objects.filter(author=request.user, recipe=recipe).exists():
        follow = get_object_or_404(model, author=request.user,
                                   recipe=recipe)
        follow.delete()
        return Response(
            'Recipe has been deleted',
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        {'errors': 'The recipy was not in the list'},
        status=status.HTTP_400_BAD_REQUEST
    )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            formating, imgstr = data.split(';base64,')
            ext = formating.split('/')[-1]
            id = uuid.uuid4()
            data = ContentFile(
                base64.b64decode(imgstr),
                name=id.urn[9:] + '.' + ext)
        return super().to_internal_value(data)
