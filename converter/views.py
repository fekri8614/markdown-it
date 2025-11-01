from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import pdf_to_markdown, image_to_text, call_model_to_markdown

def index(request):
    markdown_result = None
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded.name, uploaded)
        path = fs.path(filename)

        if uploaded.name.lower().endswith('.pdf'):
            markdown_result = pdf_to_markdown(path)
        else:
            text = image_to_text(path)
            markdown_result = call_model_to_markdown(text)

    return render(request, 'converter/index.html', {'markdown': markdown_result})
