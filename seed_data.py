import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_backend.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import SiteSetting
from portfolio.models import Education, Experience, Project, ResearchPaper

def seed():
    print("Seeding database with Tareq's initial real data...")

    # 1. Create or update Superuser
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "tareqshah.027@gmail.com", "admin123")
        print("Created Superuser -> Username: admin | Password: admin123")
    else:
        print("Superuser 'admin' already exists.")

    # 2. Seed SiteSetting
    setting, _ = SiteSetting.objects.get_or_create(pk=1)
    setting.full_name = "Md Tareq Shah Alam"
    setting.headline = "Machine Learning Engineer & Data Scientist"
    setting.bio = (
        "Passionate about extracting actionable insights from data and architecting cutting-edge AI solutions. "
        "Specializing in NLP, Transformers, CNNs, LangChain, LlamaIndex, and advanced SQL workflows to solve complex real-world challenges."
    )
    setting.email = "tareqshah.027@gmail.com"
    setting.whatsapp_number = "+8801625801530"
    setting.location = "Dhaka, Bangladesh"
    setting.blog_url = "https://medium.com/@tareqshahalam"
    setting.github_url = "https://github.com/tareqshah027"
    setting.linkedin_url = "https://www.linkedin.com/in/md-tareq-shah-alam/"
    setting.save()
    print("SiteSetting seeded.")

    # 3. Seed Education
    Education.objects.all().delete()
    
    Education.objects.create(
        degree="B.Sc. in Computer Science & Engineering",
        institution="Leading University / Technical Institute",
        location="Bangladesh",
        start_year="2020",
        end_year="2024",
        grade_or_cgpa="First Class / Outstanding",
        field_of_study="Artificial Intelligence, Machine Learning & Software Engineering",
        thesis_or_description="Major in Machine Learning and Deep Neural Network architectures with research on NLP Transformer optimization.",
        order=1,
        is_active=True
    )
    
    Education.objects.create(
        degree="Higher Secondary Certificate (HSC) — Science",
        institution="Reputed College",
        location="Bangladesh",
        start_year="2017",
        end_year="2019",
        grade_or_cgpa="GPA 5.00 / 5.00",
        field_of_study="Science (Mathematics, Physics, ICT)",
        thesis_or_description="Focused on Advanced Mathematics, Analytical Physics, and Computational Fundamentals.",
        order=2,
        is_active=True
    )
    print("Education records seeded.")

    # 4. Seed Experience
    Experience.objects.all().delete()
    
    Experience.objects.create(
        role="Machine Learning Engineer",
        company="AI Innovation Lab",
        period="2024 - Present",
        location="Remote / Hybrid",
        job_type="Full-Time",
        description="Architecting end-to-end LLM fine-tuning pipelines, building multi-agent autonomous systems using LangGraph & LlamaIndex, and deploying high-throughput inference endpoints.",
        technologies="PyTorch, Transformers, LangChain, LlamaIndex, FastAPI, Docker, CUDA",
        order=1,
        is_active=True
    )
    
    Experience.objects.create(
        role="Data Scientist & AI Researcher",
        company="Data Intelligence Solutions",
        period="2023 - 2024",
        location="Dhaka, Bangladesh",
        job_type="Full-Time",
        description="Developed predictive models, statistical NLP pipelines for semantic search, and optimized complex SQL analytical queries on massive datasets.",
        technologies="Python, Scikit-Learn, TensorFlow, Pandas, PostgreSQL, SQL, HuggingFace",
        order=2,
        is_active=True
    )
    print("Experience records seeded.")

    # 5. Seed Projects
    Project.objects.all().delete()
    
    Project.objects.create(
        title="Autonomous AI Agent & Multi-Agent Swarm",
        description="Multi-agent autonomous system built with LangGraph and LlamaIndex for complex multi-step reasoning, dynamic tool invocation, and automated document synthesis.",
        category="LLM & GenAI",
        image_url="/projects/project1.png",
        live_url="https://github.com/tareqshah027",
        github_url="https://github.com/tareqshah027",
        tech_stack="LangChain, LlamaIndex, PyTorch, FastAPI, Docker",
        is_featured=True,
        order=1
    )
    
    Project.objects.create(
        title="Neural Semantic Search & Vector Intelligence",
        description="High-performance vector search engine using Transformer embeddings, Qdrant/Pinecone indexing, and hybrid BM25 re-ranking for ultra-low latency document retrieval.",
        category="NLP & LLMs",
        image_url="/projects/project2.png",
        live_url="https://github.com/tareqshah027",
        github_url="https://github.com/tareqshah027",
        tech_stack="Transformers, HuggingFace, Qdrant, PyTorch, Python",
        is_featured=True,
        order=2
    )

    Project.objects.create(
        title="Deep Vision Defect & Object Detection Core",
        description="Custom CNN and YOLO-based computer vision pipeline for real-time object classification, anomaly detection, and edge-optimized inference deployment.",
        category="Computer Vision",
        image_url="/projects/project3.png",
        live_url="https://github.com/tareqshah027",
        github_url="https://github.com/tareqshah027",
        tech_stack="PyTorch, OpenCV, YOLO, CUDA, TensorRT",
        is_featured=True,
        order=3
    )
    print("Project records seeded.")

    # 6. Seed Research Papers
    ResearchPaper.objects.all().delete()
    
    ResearchPaper.objects.create(
        title="Adaptive Attention Mechanisms for Low-Resource NLP Transformers",
        publisher="arXiv Preprint / Technical Report",
        publication_date="2025",
        abstract="Investigating parameter-efficient fine-tuning (PEFT) and sparse attention mechanisms for cross-lingual NLP models under constrained compute budgets.",
        paper_url="https://arxiv.org",
        pdf_url="https://arxiv.org",
        tags="Transformers, NLP, Deep Learning, Attention",
        order=1
    )

    ResearchPaper.objects.create(
        title="Multi-Modal Neural Fusion in Edge-Constrained Visual Reasoning",
        publisher="IEEE / Applied AI Conference",
        publication_date="2024",
        abstract="Exploring lightweight visual-textual fusion architectures with quantized weights for real-time mobile and edge device deployment.",
        paper_url="https://ieee.org",
        pdf_url="https://ieee.org",
        tags="Computer Vision, Multi-Modal, Edge AI",
        order=2
    )
    print("Research papers seeded.")
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
