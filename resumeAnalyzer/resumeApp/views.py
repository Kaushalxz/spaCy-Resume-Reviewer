from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Resume
from django.http import JsonResponse
from .serializers import ResumeSerializer
from django.core import serializers
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from rest_framework import status
from django.http import Http404,HttpRequest,HttpResponse
import fitz
from .config import skills_and_languages

# Load SpaCy model
nlp = spacy.load('en_core_web_md')
def analyze_resume(resume_path, job_description):
    encodings = ['utf-8', 'latin-1', 'utf-16']
    resume_text = None
    
    for encoding in encodings:
        try:
            with open(resume_path, 'r', encoding=encoding) as file:
                resume_text = file.read()
            break  # Successfully read the file, exit the loop
        except UnicodeDecodeError:
            continue  # Try the next encoding
    
    if resume_text is None:
        raise ValueError(f"Failed to decode {resume_path} with any of the specified encodings.")
    
    #jobdec = extract_text_from_pdf(job_description)
    resume_text = extract_text_from_pdf(resume_path)
    
    job_doc = nlp(job_description)
    resume_doc = nlp(resume_text)

    # Extract keywords and phrases
    job_keywords = [token.lemma_ for token in job_doc if not token.is_stop and not token.is_punct and token.lemma_ in skills_and_languages]
    resume_keywords = [token.lemma_ for token in resume_doc if not token.is_stop and not token.is_punct and token.lemma_ in skills_and_languages]
# Join keywords into a single string for each
    job_keywords_str = ' '.join(job_keywords)
    resume_keywords_str = ' '.join(resume_keywords)

    # Keyword matching using TF-IDF on filtered keywords
    tfidf = TfidfVectorizer().fit([job_keywords_str, resume_keywords_str])
    job_vector = tfidf.transform([job_keywords_str])# convert the job and resume keyword strings into numerical vectors based on the TF-IDF weights calculated during the fitting process
    resume_vector = tfidf.transform([resume_keywords_str])# convert the job and resume keyword strings into numerical vectors based on the TF-IDF weights calculated during the fitting process
    keyword_match_score = (job_vector * resume_vector.T).toarray()[0][0]#measures the similarity between the two vectors, with a higher score indicating a greater degree of similarity.

    # Semantic similarity
    semantic_similarity = resume_doc.similarity(job_doc)

    # Compile analysis results
    analysis_results = {
        'keyword_match_score': keyword_match_score,
        'semantic_similarity': semantic_similarity,
        'recommendations': generate_recommendations(resume_doc, job_doc,semantic_similarity,keyword_match_score),
        'resume_keywords': resume_keywords,
        'job_keywords': job_keywords
    }

    return resume_text, analysis_results

def extract_text_from_pdf(pdf):
    text = ""
    with fitz.open(pdf) as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_recommendations(resume_doc, job_doc,semantic_similarity,keyword_match_score):
    recommendations = []
    if semantic_similarity >= 0.5:
        recommendations.append("the overall topics, context, and meanings within the resume dont closely align with those in the job")
    # Example recommendation logic
    # Add your custom recommendation logic here
    return recommendations

class ResumeUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        resumes = Resume.objects.all()
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        file_serializer = ResumeSerializer(data=request.data, partial=True)
        if file_serializer.is_valid():
            resume = file_serializer.save()
            resume_path = resume.file.path
            job_description = request.data.get('job_description')

            # Perform analysis
            text_content, analysis_results = analyze_resume(resume_path, job_description)

            # Update Resume instance with analysis results
            resume.text_content = text_content
            resume.analysis_results = analysis_results
            resume.save()

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def resume_list_view(request):
    resumes = Resume.objects.all()
    resumes_json = serializers.serialize('json', resumes)
    return JsonResponse(resumes_json, safe=False)
        
# def pdf_text_extractor_view(request):
#     # Example PDF path - you might want to make this dynamic
#     pdf_path = 'path/to/your/pdf/file.pdf'
#     extracted_text = extract_text_from_pdf(pdf_path)
#     return HttpResponse(extracted_text, content_type="text/plain")