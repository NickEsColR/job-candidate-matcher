import { candidateFormSchema, type CandidateFormData } from './candidate-form.schema'
import type { Candidate } from '@/domain/types'

/**
 * Adds a skill to the current list if it's non-empty and not already present.
 * Returns new skills array and whether the skill input should be cleared.
 */
export function addSkillToCurrentSkills(
  currentSkills: string[],
  skillInput: string,
): { newSkills: string[]; skillInputCleared: boolean } {
  const trimmed = skillInput.trim()
  if (trimmed && !currentSkills.includes(trimmed)) {
    return {
      newSkills: [...currentSkills, trimmed],
      skillInputCleared: true,
    }
  }
  return {
    newSkills: currentSkills,
    skillInputCleared: false,
  }
}

/**
 * Removes a skill from the current list.
 */
export function removeSkillFromCurrentSkills(
  currentSkills: string[],
  skillToRemove: string,
): string[] {
  return currentSkills.filter(s => s !== skillToRemove)
}

/**
 * Validates candidate form data using Zod schema.
 * Returns either validated data or a field-errors map.
 */
export function validateCandidateForm(
  data: CandidateFormData,
): { success: true; data: CandidateFormData } | { success: false; errors: Record<string, string> } {
  const result = candidateFormSchema.safeParse(data)
  if (!result.success) {
    const fieldErrors: Record<string, string> = {}
    for (const issue of result.error.issues) {
      const field = issue.path[0]
      if (field && !fieldErrors[String(field)]) {
        fieldErrors[String(field)] = issue.message
      }
    }
    return { success: false, errors: fieldErrors }
  }
  return { success: true, data: result.data }
}

/**
 * Prepares candidate data for submission, ensuring resumeUrl is empty string if missing.
 */
export function prepareCandidateForSubmission(
  data: CandidateFormData,
): Omit<Candidate, 'id'> {
  return {
    name: data.name,
    email: data.email,
    yearsOfExperience: data.yearsOfExperience,
    resumeUrl: data.resumeUrl || '',
    skills: data.skills,
  }
}