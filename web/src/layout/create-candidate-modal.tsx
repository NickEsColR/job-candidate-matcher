import { useState } from "preact/hooks";
import type { Candidate } from "@/domain/types";
import type { CandidateFormData } from "@/utils/candidate-form.schema";
import {
  addSkillToCurrentSkills,
  removeSkillFromCurrentSkills,
  validateCandidateForm,
  prepareCandidateForSubmission,
} from "@/utils/candidate-form.logic";

interface CreateCandidateModalProps {
  onClose: () => void;
  onCreate: (candidate: Omit<Candidate, "id">) => Promise<Candidate>;
}

export function CreateCandidateModal({
  onClose,
  onCreate,
}: CreateCandidateModalProps) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [yearsOfExperience, setYearsOfExperience] = useState("0");
  const [resumeUrl, setResumeUrl] = useState("");
  const [skills, setSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  function addSkill() {
    const { newSkills, skillInputCleared } = addSkillToCurrentSkills(
      skills,
      skillInput,
    );
    if (skillInputCleared) {
      setSkills(newSkills);
      setSkillInput("");
      setErrors((prev) => {
        const next = { ...prev };
        delete next.skills;
        return next;
      });
    }
  }

  function removeSkill(skill: string) {
    setSkills(removeSkillFromCurrentSkills(skills, skill));
  }

  function handleSkillKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter") {
      e.preventDefault();
      addSkill();
    }
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    setErrors({});

    const raw: CandidateFormData = {
      name,
      email,
      yearsOfExperience: Number(yearsOfExperience),
      resumeUrl,
      skills,
    };

    const validation = validateCandidateForm(raw);

    if (!validation.success) {
      setErrors(validation.errors);
      return;
    }

    setSaving(true);
    try {
      const candidateData = prepareCandidateForSubmission(validation.data);
      await onCreate(candidateData);
      onClose();
    } finally {
      setSaving(false);
    }
  }

  return (
    <div
      class="fixed inset-0 z-[60] flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-candidate-title"
    >
      {/* Backdrop */}
      <div
        class="absolute inset-0 bg-background/60 backdrop-blur-md"
        onClick={onClose}
      />

      {/* Modal Content */}
      <div class="relative backdrop-blur-md w-full max-w-2xl overflow-hidden rounded-xl border border-outline-variant/20 bg-surface-container-low shadow-2xl">
        <div class="p-8">
          <div class="mb-8 flex items-start justify-between">
            <div>
              <h1
                id="create-candidate-title"
                class="text-2xl font-bold tracking-tight text-primary"
              >
                Crear Candidato
              </h1>
              <p class="mt-1 text-sm text-on-surface-variant">
                Ingrese los detalles para el nuevo perfil de evaluación
                estratégica.
              </p>
            </div>
            <button
              class="material-symbols-outlined text-on-surface-variant transition-colors hover:text-on-surface"
              onClick={onClose}
              type="button"
              aria-label="Cerrar modal"
            >
              close
            </button>
          </div>

          <form class="space-y-6" onSubmit={handleSubmit}>
            <div class="grid grid-cols-2 gap-6">
              {/* Name Field */}
              <div class="space-y-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  Nombre Completo <span class="text-error">*</span>
                </label>
                <input
                  class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface placeholder:text-on-surface-variant/30 transition-all focus:ring-2 focus:ring-primary/40"
                  placeholder="Ej. Javier Domínguez"
                  type="text"
                  value={name}
                  onInput={(e) => {
                    setName((e.currentTarget as HTMLInputElement).value);
                    setErrors((prev) => {
                      const next = { ...prev };
                      delete next.name;
                      return next;
                    });
                  }}
                />
                {errors.name && <p class="text-xs text-error">{errors.name}</p>}
              </div>

              {/* Email Field */}
              <div class="space-y-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  Email <span class="text-error">*</span>
                </label>
                <input
                  class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface placeholder:text-on-surface-variant/30 transition-all focus:ring-2 focus:ring-primary/40"
                  placeholder="javier@empresa.com"
                  type="email"
                  value={email}
                  onInput={(e) => {
                    setEmail((e.currentTarget as HTMLInputElement).value);
                    setErrors((prev) => {
                      const next = { ...prev };
                      delete next.email;
                      return next;
                    });
                  }}
                />
                {errors.email && (
                  <p class="text-xs text-error">{errors.email}</p>
                )}
              </div>
            </div>

            {/* Skills List */}
            <div class="space-y-3">
              <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                Habilidades Técnicas <span class="text-error">*</span>
              </label>
              <div class="flex min-h-12 flex-wrap items-center gap-2 rounded-lg bg-surface-container p-3">
                {skills.map((skill) => (
                  <span
                    key={skill}
                    class="flex items-center gap-2 rounded-md bg-secondary-container px-3 py-1 text-sm text-on-secondary-container"
                  >
                    {skill}
                    <button
                      class="material-symbols-outlined text-[16px]"
                      onClick={() => removeSkill(skill)}
                      type="button"
                    >
                      close
                    </button>
                  </span>
                ))}
                <input
                  class="w-24 border-none bg-transparent py-1 text-sm placeholder:text-on-surface-variant/30 focus:ring-0"
                  placeholder="Añadir..."
                  type="text"
                  value={skillInput}
                  onInput={(e) =>
                    setSkillInput((e.currentTarget as HTMLInputElement).value)
                  }
                  onKeyDown={handleSkillKeyDown}
                />
              </div>
              {errors.skills && (
                <p class="text-xs text-error">{errors.skills}</p>
              )}
            </div>

            <div class="grid grid-cols-12 gap-6">
              {/* Experience Field */}
              <div class="col-span-4 space-y-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  Experiencia (Años) <span class="text-error">*</span>
                </label>
                <div class="relative">
                  <input
                    class="w-full rounded-lg border-none bg-surface-container p-3 text-on-surface transition-all focus:ring-2 focus:ring-primary/40"
                    type="number"
                    min="0"
                    max="50"
                    value={yearsOfExperience}
                    onInput={(e) => {
                      setYearsOfExperience(
                        (e.currentTarget as HTMLInputElement).value,
                      );
                      setErrors((prev) => {
                        const next = { ...prev };
                        delete next.yearsOfExperience;
                        return next;
                      });
                    }}
                  />
                  <span
                    class="material-symbols-outlined pointer-events-none absolute top-1/2 right-3 -translate-y-1/2 text-sm text-on-surface-variant/50"
                    aria-hidden="true"
                  >
                    unfold_more
                  </span>
                </div>
                {errors.yearsOfExperience && (
                  <p class="text-xs text-error">{errors.yearsOfExperience}</p>
                )}
              </div>

              {/* CV URL Field */}
              <div class="col-span-8 space-y-2">
                <label class="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  URL de Currículum
                </label>
                <div class="flex items-center overflow-hidden rounded-lg bg-surface-container transition-all focus-within:ring-2 focus-within:ring-primary/40">
                  <span class="material-symbols-outlined px-3 text-on-surface-variant/50">
                    link
                  </span>
                  <input
                    class="w-full border-none bg-transparent p-3 text-on-surface placeholder:text-on-surface-variant/30 focus:ring-0"
                    placeholder="https://linkedin.com/in/perfil"
                    type="url"
                    value={resumeUrl}
                    onInput={(e) =>
                      setResumeUrl((e.currentTarget as HTMLInputElement).value)
                    }
                  />
                </div>
                {errors.resumeUrl && (
                  <p class="text-xs text-error">{errors.resumeUrl}</p>
                )}
              </div>
            </div>

            {/* Footer Actions */}
            <div class="mt-8 flex justify-end gap-4 border-t border-outline-variant/10 pt-6">
              <button
                class="rounded-full px-6 py-2.5 font-medium text-on-surface-variant transition-all hover:bg-surface-container hover:text-on-surface"
                onClick={onClose}
                type="button"
              >
                Cancelar
              </button>
              <button
                class="flex items-center gap-2 rounded-full bg-primary-container px-8 py-2.5 font-bold text-white shadow-lg shadow-primary-container/20 transition-all hover:bg-inverse-primary disabled:opacity-50"
                disabled={saving}
                type="submit"
              >
                <span class="material-symbols-outlined text-[20px]">save</span>
                {saving ? "Guardando..." : "Guardar Candidato"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
