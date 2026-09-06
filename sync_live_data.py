import urllib.request
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_backend.settings")
django.setup()

from core.models import SiteSetting
from portfolio.models import Education, Experience, Project, ResearchPaper

def sync():
    url = "https://tareq052.pythonanywhere.com/api/all/"
    print(f"Fetching from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    print("Fetched successfully!")

    # 1. SiteSetting
    ss_data = data.get("site_setting", {})
    if ss_data:
        ss, _ = SiteSetting.objects.get_or_create(pk=1)
        for k, v in ss_data.items():
            if hasattr(ss, k) and k not in ("id", "created_at", "updated_at"):
                setattr(ss, k, v)
        ss.save()
        print("Synced SiteSetting.")

    # 2. Education
    edu_list = data.get("education", [])
    if edu_list:
        Education.objects.all().delete()
        for item in edu_list:
            Education.objects.create(
                degree=item.get("degree", ""),
                institution=item.get("institution", ""),
                location=item.get("location", ""),
                start_year=item.get("start_year", ""),
                end_year=item.get("end_year", ""),
                grade_or_cgpa=item.get("grade_or_cgpa", ""),
                field_of_study=item.get("field_of_study", ""),
                thesis_or_description=item.get("thesis_or_description", ""),
                order=item.get("order", 1),
                is_active=item.get("is_active", True)
            )
        print(f"Synced {len(edu_list)} education entries.")

    # 3. Experience
    exp_list = data.get("experience", [])
    if exp_list:
        Experience.objects.all().delete()
        for item in exp_list:
            Experience.objects.create(
                role=item.get("role", ""),
                company=item.get("company", ""),
                period=item.get("period", ""),
                location=item.get("location", ""),
                job_type=item.get("job_type", ""),
                description=item.get("description", ""),
                technologies=item.get("technologies", ""),
                order=item.get("order", 1),
                is_active=item.get("is_active", True)
            )
        print(f"Synced {len(exp_list)} experience entries.")

    # 4. Projects
    proj_list = data.get("projects", [])
    if proj_list:
        Project.objects.all().delete()
        media_dir = os.path.join(os.getcwd(), "media", "projects")
        os.makedirs(media_dir, exist_ok=True)

        for item in proj_list:
            img_url = item.get("image", "")
            local_img_rel = ""
            if img_url and img_url.startswith("http"):
                filename = os.path.basename(img_url)
                dest_path = os.path.join(media_dir, filename)
                try:
                    urllib.request.urlretrieve(img_url, dest_path)
                    local_img_rel = f"projects/{filename}"
                    print(f"Downloaded project image: {filename}")
                except Exception as e:
                    print(f"Failed downloading {img_url}: {e}")

            Project.objects.create(
                title=item.get("title", ""),
                description=item.get("description", ""),
                category=item.get("category", "Applied AI & ML"),
                image_url=item.get("image_url", "/projects/project1.png"),
                image_file=local_img_rel if local_img_rel else None,
                live_url=item.get("live_url", ""),
                github_url=item.get("github_url", ""),
                tech_stack=item.get("tech_stack", ""),
                is_featured=item.get("is_featured", True),
                order=item.get("order", 1)
            )
        print(f"Synced {len(proj_list)} projects.")

    print("All live data successfully imported into local SQLite database!")

if __name__ == "__main__":
    sync()
