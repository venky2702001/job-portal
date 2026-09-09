import re
from pypdf import PdfReader
import docx
from django.shortcuts import render
from functools import wraps

def extract_text_from_resume(file_field):
    """
    file_field: a Django FieldFile (e.g. profile.resume). Uses .open()/.read()
    instead of .path so this works with remote storage backends (Cloudinary,
    S3) as well as local FileSystemStorage, which don't support .path.
    """
    text = ""
    name = file_field.name.lower()
    if name.endswith(".pdf"):
        with file_field.open("rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif name.endswith(".docx"):
        with file_field.open("rb") as f:
            doc = docx.Document(f)
            for para in doc.paragraphs:
                text += para.text + "\n"
    return text

def extract_skills(text):
    skills_keywords = ["Python", "Django", "JavaScript", "React", "SQL", "HTML", "CSS"]
    found = [skill for skill in skills_keywords if re.search(rf"\b{skill}\b", text, re.IGNORECASE)]
    return ", ".join(found)

#role-based access control decorator


def recruiter_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'recruiter':
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', status=403)
    return wrapper

def candidate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'candidate':
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', status=403)
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return render(request, '403.html', status=403)
    return wrapper
