from rest_framework import viewsets

from comment.models import Comment
from comment.serializers import CommentSerializer
from comment.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
