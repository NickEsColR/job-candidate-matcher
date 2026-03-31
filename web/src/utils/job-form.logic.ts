import { jobFormSchema, type JobFormData } from './job-form.schema'
import type { JobOpening } from '@/domain/types'

/**
 * Adds a requirement to the current list if it's non-empty and not already present.
 * Returns new requirements array and whether the input should be cleared.
 */
export function addRequirementToCurrentRequirements(
  currentRequirements: string[],
  requirementInput: string,
): { newRequirements: string[]; inputCleared: boolean } {
  const trimmed = requirementInput.trim()
  if (trimmed && !currentRequirements.includes(trimmed)) {
    return {
      newRequirements: [...currentRequirements, trimmed],
      inputCleared: true,
    }
  }
  return {
    newRequirements: currentRequirements,
    inputCleared: false,
  }
}

/**
 * Removes a requirement from the current list.
 */
export function removeRequirementFromCurrentRequirements(
  currentRequirements: string[],
  requirementToRemove: string,
): string[] {
  return currentRequirements.filter((r) => r !== requirementToRemove)
}

/**
 * Validates job form data using Zod schema.
 * Returns either validated data or a field-errors map.
 */
export function validateJobForm(
  data: JobFormData,
):
  | { success: true; data: JobFormData }
  | { success: false; errors: Record<string, string> } {
  const result = jobFormSchema.safeParse(data)
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
 * Prepares job data for submission, converting requirements strings to JobRequirement objects.
 */
export function prepareJobForSubmission(
  data: JobFormData,
): Omit<JobOpening, 'id'> {
  return {
    title: data.title,
    summary: data.summary,
    requirements: data.requirements.map((label, i) => ({
      id: `req-${Date.now()}-${i}`,
      label,
    })),
    location: data.location || '',
    salaryRange: data.salaryRange || '',
  }
}
