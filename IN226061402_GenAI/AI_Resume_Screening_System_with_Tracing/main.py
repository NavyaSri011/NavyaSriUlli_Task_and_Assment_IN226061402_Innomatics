import os
from dotenv import load_dotenv

from chains.extractor_chain import extractor_chain
from chains.matcher_chain import matcher_chain
from chains.scoring_chain import scoring_chain
from chains.explanation_chain import explanation_chain

load_dotenv()


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_pipeline(resume_path, job_path):

    resume = load_file(resume_path)
    job = load_file(job_path)

    # STEP 1: Extract Skills
    extracted = extractor_chain.invoke({"resume": resume})
    print("\n=== SKILL EXTRACTION ===\n")
    print(extracted.content)

    # STEP 2: Matching (FIXED)
    matched = matcher_chain.invoke({
        "resume_skills": extracted.content,
        "job_description": job
    })
    print("\n=== MATCHING ===\n")
    print(matched.content)

    # STEP 3: Scoring
    score = scoring_chain.invoke({
        "match_result": matched.content
    })
    print("\n=== SCORE ===\n")
    print(score.content)

    # STEP 4: Explanation
    explanation = explanation_chain.invoke({
        "score": score.content,
        "match_result": matched.content
    })
    print("\n=== EXPLANATION ===\n")
    print(explanation.content)


if __name__ == "__main__":

    print("\n######## STRONG CANDIDATE ########")
    run_pipeline("data/resumes/strong.txt", "data/job_description.txt")

    print("\n######## AVERAGE CANDIDATE ########")
    run_pipeline("data/resumes/average.txt", "data/job_description.txt")

    print("\n######## WEAK CANDIDATE ########")
    run_pipeline("data/resumes/weak.txt", "data/job_description.txt")