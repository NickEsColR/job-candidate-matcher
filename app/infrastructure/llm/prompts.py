"""Prompts for LLM-based evaluation analysis."""

from app.schemas.evaluation import EvaluationAnalysisInput

SYSTEM_PROMPT = """You are an expert HR analyst and career advisor. Your role is to evaluate how well a candidate matches a job position based on the provided information.

You must analyze the candidate's qualifications against the job requirements and provide:
1. A score from 0 to 100 (0 = no match, 100 = perfect match)
2. A brief summary of your evaluation
3. Key strengths of the candidate for this role
4. Weaknesses or gaps compared to job requirements
5. Recommendations to improve the candidate's fit

Be objective, evidence-based, and constructive. Consider:
- Skills match (required and preferred)
- Experience level alignment
- Education requirements
- Overall qualifications fit

Your response must be in English and follow the structured format provided."""


def build_user_prompt(input_data: EvaluationAnalysisInput) -> str:
    """
    Build the user prompt from evaluation input data.

    Args:
        input_data: The candidate and job context to analyze.

    Returns:
        Formatted prompt string for the LLM.
    """
    candidate = input_data.candidate
    job = input_data.job

    prompt = f"""Please evaluate how well the following candidate matches the job position.

## CANDIDATE INFORMATION
- **Skills**: {", ".join(candidate.skills) if candidate.skills else "None listed"}
- **Experience Years**: {candidate.experience_years if candidate.experience_years else "Not specified"}
- **Education**: {candidate.education if candidate.education else "Not specified"}

## RESUME/CV CONTENT
{candidate.resume_text if candidate.resume_text else "No resume/CV available"}

---

## JOB POSITION
- **Title**: {job.title}
- **Description**: {job.description}
- **Required Skills**: {", ".join(job.requirements) if job.requirements else "None specified"}

---

Please provide your evaluation in the structured format requested."""
    return prompt
