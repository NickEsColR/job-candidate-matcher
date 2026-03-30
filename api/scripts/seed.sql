-- ============================================================
-- Seed script for job-candidate-matcher
-- Creates tables (if not exist) and inserts sample data
-- ============================================================

-- Tabla de candidatos
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    skills JSONB DEFAULT '[]'::jsonb,
    experience INTEGER,
    resume_url VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de jobs
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    requirements JSONB DEFAULT '[]'::jsonb,
    location VARCHAR,
    salary_range VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de evaluaciones
CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id),
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    status VARCHAR DEFAULT 'pending',
    score INTEGER,
    summary TEXT,
    strengths JSONB DEFAULT '[]'::jsonb,
    weaknesses JSONB DEFAULT '[]'::jsonb,
    recommendations JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- ============================================================
-- Candidatos
-- ============================================================
INSERT INTO candidates (name, email, skills, experience, resume_url, created_at) VALUES
(
    'María García López',
    'maria.garcia@example.com',
    '["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "Redis"]'::jsonb,
    5,
    'https://resumes.example.com/maria-garcia.pdf',
    NOW() - INTERVAL '10 days'
),
(
    'Carlos Rodríguez Pérez',
    'carlos.rodriguez@example.com',
    '["Python", "Django", "React", "TypeScript", "GraphQL", "Kubernetes"]'::jsonb,
    7,
    'https://resumes.example.com/carlos-rodriguez.pdf',
    NOW() - INTERVAL '8 days'
),
(
    'Ana Fernández Silva',
    'ana.fernandez@example.com',
    '["Python", "FastAPI", "SQLAlchemy", "Docker", "CI/CD", "Terraform"]'::jsonb,
    3,
    'https://resumes.example.com/ana-fernandez.pdf',
    NOW() - INTERVAL '5 days'
),
(
    'Lucas Martínez Díaz',
    'lucas.martinez@example.com',
    '["Go", "Python", "gRPC", "PostgreSQL", "Kafka", "AWS"]'::jsonb,
    10,
    'https://resumes.example.com/lucas-martinez.pdf',
    NOW() - INTERVAL '3 days'
),
(
    'Sofía Herrera Ríos',
    'sofia.herrera@example.com',
    '["Python", "FastAPI", "Machine Learning", "TensorFlow", "Pandas", "Docker"]'::jsonb,
    4,
    'https://resumes.example.com/sofia-herrera.pdf',
    NOW() - INTERVAL '1 day'
);

-- ============================================================
-- Jobs
-- ============================================================
INSERT INTO jobs (title, description, requirements, location, salary_range, created_at) VALUES
(
    'Senior Backend Engineer',
    'Buscamos un ingeniero backend senior para liderar el desarrollo de nuestra plataforma de matching. Trabajarás con FastAPI, PostgreSQL y sistemas de mensajería asíncrona para construir APIs de alto rendimiento que procesan miles de evaluaciones por día.',
    '["Python", "FastAPI", "PostgreSQL", "5+ años experiencia", "Arquitectura de microservicios", "CI/CD"]'::jsonb,
    'Buenos Aires, Argentina (Remoto)',
    'USD 4500-6500/mes',
    NOW() - INTERVAL '15 days'
),
(
    'Full Stack Developer',
    'Únete al equipo de producto para desarrollar features end-to-end. Necesitamos alguien que se mueva cómodo tanto en el backend con Django como en el frontend con React/TypeScript.',
    '["Python", "Django", "React", "TypeScript", "3+ años experiencia", "GraphQL"]'::jsonb,
    'Córdoba, Argentina (Híbrido)',
    'USD 3000-4500/mes',
    NOW() - INTERVAL '12 days'
),
(
    'Platform Engineer',
    'Necesitamos un ingeniero de infraestructura que nos ayude a escalar nuestra plataforma. Experiencia con orquestación de contenedores, infraestructura como código y observabilidad.',
    '["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "5+ años experiencia"]'::jsonb,
    'Remoto (LATAM)',
    'USD 5000-7000/mes',
    NOW() - INTERVAL '7 days'
),
(
    'ML Engineer',
    'Posición para desarrollar y mantener modelos de ML que potencian nuestro motor de matching. Trabajarás con datos de candidatos y job descriptions para mejorar la calidad de las evaluaciones.',
    '["Python", "Machine Learning", "TensorFlow o PyTorch", "NLP", "3+ años experiencia", "MLOps"]'::jsonb,
    'Buenos Aires, Argentina (Remoto)',
    'USD 4000-6000/mes',
    NOW() - INTERVAL '2 days'
);

-- ============================================================
-- Una evaluación de ejemplo (matching parcial)
-- ============================================================
INSERT INTO evaluations (candidate_id, job_id, status, score, summary, strengths, weaknesses, recommendations, created_at, completed_at) VALUES
(
    1, -- María García → Senior Backend Engineer
    1,
    'completed',
    85,
    'Excelente match para la posición. María combina fuertes habilidades técnicas en Python/FastAPI/PostgreSQL con experiencia sólida en AWS y Docker. Su experiencia de 5 años alinea bien con el nivel senior requerido.',
    '["Dominio de FastAPI y PostgreSQL", "Experiencia con Docker y AWS", "5 años de experiencia alineados"]'::jsonb,
    '["No menciona experiencia con mensajería asíncrona", "Falta detalle sobre arquitectura de microservicios"]'::jsonb,
    '["Avanzar a entrevista técnica", "Evaluar experiencia con sistemas distribuidos"]'::jsonb,
    NOW() - INTERVAL '2 days',
    NOW() - INTERVAL '2 days' + INTERVAL '30 seconds'
);

-- Confirmar inserciones
SELECT 'Candidatos insertados: ' || COUNT(*) AS resultado FROM candidates;
SELECT 'Jobs insertados: ' || COUNT(*) AS resultado FROM jobs;
SELECT 'Evaluaciones insertadas: ' || COUNT(*) AS resultado FROM evaluations;
