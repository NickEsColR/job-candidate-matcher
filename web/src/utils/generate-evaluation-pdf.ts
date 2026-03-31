import { jsPDF } from 'jspdf'
import type { CompletedEvaluation } from '@/domain/types'

interface GeneratePdfParams {
  evaluation: CompletedEvaluation
  candidateName: string
  jobTitle: string
}

/**
 * Genera y descarga un PDF con el reporte de evaluación.
 * Función pura — no importa Preact ni hace fetch.
 */
export function generateEvaluationPdf({
  evaluation,
  candidateName,
  jobTitle,
}: GeneratePdfParams): void {
  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()
  const margin = 20
  const contentWidth = pageWidth - margin * 2
  let y = margin

  // --- Header ---
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(20)
  doc.text('Reporte de Evaluación', margin, y)
  y += 10

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(11)
  doc.text(`Candidato: ${candidateName}`, margin, y)
  y += 6
  doc.text(`Puesto: ${jobTitle}`, margin, y)
  y += 6
  doc.text(`Fecha: ${new Date().toLocaleDateString('es-AR')}`, margin, y)
  y += 10

  // Línea separadora
  doc.setDrawColor(180)
  doc.line(margin, y, pageWidth - margin, y)
  y += 10

  // --- Score ---
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(14)
  doc.text('Puntuación', margin, y)
  y += 18

  const scoreText = `${evaluation.score}`
  doc.setFontSize(36)
  doc.text(scoreText, margin, y)
  doc.setFontSize(16)
  doc.setFont('helvetica', 'normal')
  doc.text(`/ ${evaluation.maxScore}`, margin + doc.getTextWidth(scoreText) + 8, y)
  y += 20

  // --- Resumen Ejecutivo ---
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(14)
  doc.text('Resumen Ejecutivo', margin, y)
  y += 8

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  const summaryLines = doc.splitTextToSize(evaluation.executiveSummary, contentWidth)
  doc.text(summaryLines, margin, y)
  y += summaryLines.length * 5 + 10

  // --- Fortalezas ---
  y = ensureSpace(doc, y, 30)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(14)
  doc.text('Fortalezas', margin, y)
  y += 8

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  for (const strength of evaluation.strengths) {
    y = ensureSpace(doc, y, 10)
    const lines = doc.splitTextToSize(`• ${strength}`, contentWidth)
    doc.text(lines, margin, y)
    y += lines.length * 5 + 3
  }
  y += 5

  // --- Áreas de Mejora ---
  y = ensureSpace(doc, y, 30)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(14)
  doc.text('Áreas de Mejora', margin, y)
  y += 8

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  for (const area of evaluation.improvementAreas) {
    y = ensureSpace(doc, y, 10)
    const lines = doc.splitTextToSize(`• ${area}`, contentWidth)
    doc.text(lines, margin, y)
    y += lines.length * 5 + 3
  }
  y += 5

  // --- Recomendaciones Finales ---
  y = ensureSpace(doc, y, 30)
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(14)
  doc.text('Recomendaciones Finales', margin, y)
  y += 8

  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  for (const rec of evaluation.finalRecommendations) {
    y = ensureSpace(doc, y, 10)
    const lines = doc.splitTextToSize(`${evaluation.finalRecommendations.indexOf(rec) + 1}. ${rec}`, contentWidth)
    doc.text(lines, margin, y)
    y += lines.length * 5 + 3
  }

  // Descargar
  const filename = `evaluacion-${candidateName.replace(/\s+/g, '-').toLowerCase()}.pdf`
  doc.save(filename)
}

/**
 * Si no hay espacio suficiente en la página, agrega una nueva.
 */
function ensureSpace(doc: jsPDF, y: number, needed: number): number {
  const pageHeight = doc.internal.pageSize.getHeight()
  if (y + needed > pageHeight - 20) {
    doc.addPage()
    return 20
  }
  return y
}
