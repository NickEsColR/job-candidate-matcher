import { z } from 'zod'

export const jobFormSchema = z.object({
  title: z.string().min(1, { error: 'El título es obligatorio' }),
  summary: z.string().min(1, { error: 'El resumen es obligatorio' }),
  requirements: z
    .array(z.string().min(1))
    .min(1, { error: 'Agregue al menos un requisito' }),
  location: z.string(),
  salaryRange: z.string(),
})

export type JobFormData = z.infer<typeof jobFormSchema>
