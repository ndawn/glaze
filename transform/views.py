from image.models import Image
from transform.models import TransformationChain
from transform.string_parser import StringParser
from transform.transformations.chain import TransformationChainExecutor

from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.response import Response


class TransformView(RetrieveAPIView):
    queryset = Image.objects.all()

    def retrieve(self, request, *args, pk=None, **kwargs):
        chain_string = request.GET.get('chain', '')

        image = get_object_or_404(self.queryset, pk=pk)

        string_parser = StringParser(image)
        chain = string_parser.parse(chain_string)

        executor = TransformationChainExecutor(image, chain)

        cached_chain = TransformationChain.objects.filter(id=executor.sha256)

        if cached_chain.exists():
            cached_chain = cached_chain.first()
            return HttpResponse(cached_chain.file.read(), content_type=cached_chain.mime)

        transformed_image = executor.execute()

        return HttpResponse(transformed_image.file.read(), content_type=transformed_image.mime)
