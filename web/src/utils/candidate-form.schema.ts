import { z } from 'zod'

export const candidateFormSchema = z.object({
  name: z.string().min(1, { error: 'El nombre es obligatorio' }),
  email: z.email({ error: 'Ingrese un email válido' }),
  yearsOfExperience: z.coerce
    .number({ error: 'Ingrese un número válido' })
    .min(0, { error: 'La experiencia no puede ser negativa' })
    .max(50, { error: 'Máximo 50 años de experiencia' }),
  resumeUrl: z.url({ error: 'Ingrese una URL válida' }).or(z.literal('')),
  skills: z
    .array(z.string().min(1))
    .min(1, { error: 'Agregue al menos una habilidad' }),
})

export type CandidateFormData = z.infer<typeof candidateFormSchema>
