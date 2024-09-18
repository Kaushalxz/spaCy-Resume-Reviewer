# 📄 Resume Analyzer


A powerful AI-driven application that helps you analyze resumes and match them with job descriptions using advanced Natural Language Processing (NLP) techniques. This project uses a Django REST API backend and a React-based frontend to deliver an intuitive and seamless experience.

## 🚀 Features

- **Resume Upload**: Upload resumes in PDF and analyze them.
- **Job Description Matching**: Compare the resume with a job description to find the best match.
- **Keyword Extraction**: Extracts key skills and phrases from resumes and job descriptions.
- **TF-IDF Matching**: Uses TF-IDF to determine keyword importance and match scores.
- **Semantic Similarity**: Calculates how semantically similar a resume is to the job description.
- **Custom Recommendations**: Provides tailored suggestions to enhance resume relevance.

## 🛠️ Tech Stack

- **Frontend**: React, Axios, HTML, CSS
- **Backend**: Django REST Framework
- **AI & NLP**: Python, spaCy, scikit-learn (TF-IDF)
- **Database**: SQLite (or any Django-supported database)
- **File Handling**: Python `os`, `pymupdf` for PDF handling

## 🧠 How It Works

1. **Upload Resume**: Users upload their resumes and provide a job description.
2. **NLP Processing**: The backend processes the resume using spaCy to extract keywords and evaluate semantic similarity.
3. **TF-IDF Analysis**: The system computes keyword match scores using TF-IDF vectorization.
4. **Results**: The backend sends the analysis results back to the frontend, which are displayed to the user.


## References

1. https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
2. https://www.youtube.com/watch?v=lBO1L8pgR9s
3. https://vasista.medium.com/preparing-the-text-data-with-scikit-learn-b31a3df567e
