from sentence_transformers import SentenceTransformer, util
import re
import torch 

usedevice = "cuda" if torch.cuda.is_available() else "cpu"

# Load free sentence-transformer model
model = SentenceTransformer('all-MiniLM-L6-v2', device="cuda")

# Example skill list from your resume
resume_skills = {
    # Cloud Technologies
    "Databricks",
    # "Power BI",
    "aws",
    "Azure Data Factory",
    # "Azure DevOps",
    # "GitHub",
    "Azure Synapse",

    # Programming
    "Spark SQL",
    "PySpark",
    "Scala",
    "Python",
    # "PgSQL",
    # "MongoDB",
    # "Cosmos DB",

    # Security & Governance
    "Unity Catalog",
    # "Access Management",

    # Additional Tools & Platforms (from projects)
    # "PgSQL",
    # "ADB",
    # "ADLS",
    "ADF",
    # "SFTP",
    # "Salesforce",
    # "Core Data Platforms",
    # "Azure Cloud Products"
}

# def analyze_job_fit(job_description, resume_text, resume_skills): #, critical_skills=None
#     # --- Semantic similarity ---
#     emb_job = model.encode(job_description, convert_to_tensor=True)
#     emb_resume = model.encode(resume_text, convert_to_tensor=True)
#     similarity = util.cos_sim(emb_resume, emb_job).item()
#     match_pct = round(similarity * 100, 2)

#     # --- Skill matching with embeddings ---
#     found_skills, missing_skills = set(), set()
#     for skill in resume_skills:
#         emb_skill = model.encode(skill, convert_to_tensor=True)
#         sim = util.cos_sim(emb_skill, emb_job).item()
#         if sim > 0.45 or skill.lower() in job_description.lower():
#             found_skills.add(skill)
#         else:
#             missing_skills.add(skill)

#     # --- Weighted scoring (penalize missing critical skills) ---
#     # if critical_skills:
#     #     penalties = sum(10 for skill in critical_skills if skill in missing_skills)
#     #     match_pct = max(0, match_pct - penalties)

#     return round(match_pct, 2), found_skills, missing_skills

def analyze_job_fit(job_description, resume_text, resume_skills, threshold=0.4):
    # Document-level similarity
    emb_job = model.encode(job_description, convert_to_tensor=True)
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    doc_similarity = util.cos_sim(emb_resume, emb_job).item()

    # Skill-level similarity
    matched, missing = set(), set()
    skill_scores = []
    for skill in resume_skills:
        emb_skill = model.encode(skill, convert_to_tensor=True)
        sim = util.cos_sim(emb_skill, emb_job).item()
        if sim > threshold or skill.lower() in job_description.lower():
            matched.add(skill)
            skill_scores.append(sim)
        else:
            missing.add(skill)

    skill_overlap_score = sum(skill_scores) / len(skill_scores) if skill_scores else 0

    # Weighted combination
    final_score = (0.6 * skill_overlap_score) + (0.4 * doc_similarity)
    match_pct = round(final_score * 100, 2)

    return match_pct, matched, missing
