from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

app = FastAPI(
    title="OpenRoadmap API",
    description="API para la gestión comunitaria de cursos y roadmaps de aprendizaje",
    version="0.1.0"
)

# Configuración de CORS para permitir solicitudes desde el frontend Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos de prueba representativos alineados al BackendSchema
CURSOS_MOCK: List[Dict[str, Any]] = [
    {
        "id": 1,
        "titulo": "Python desde Cero para Desarrollo de Software",
        "tema": "Python & Buenas Prácticas",
        "version": "2026",
        "anio_edicion": 2026,
        "docentes": "Ing. Martín Ramos",
        "url": "https://www.youtube.com/playlist?list=ejemplo-python-2026",
        "tiene_cuestionarios": True,
        "requiere_examen": False,
        "extiende_certificado": True,
        "aval_organizacion": "Comunidad Abierta UTN",
        "estado": "publicado",
        "categoria": {"id": 1, "nombre": "Backend", "slug": "backend"},
        "declaracion_cursado": {
            "aportado_por_estudiante": "Lucas Gómez",
            "tomo_el_curso": True
        }
    },
    {
        "id": 2,
        "titulo": "FastAPI Moderno: APIs Asíncronas y Docker",
        "tema": "FastAPI & uv",
        "version": "v1.2",
        "anio_edicion": 2026,
        "docentes": "Dra. Elena Rossi",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "tiene_cuestionarios": True,
        "requiere_examen": True,
        "extiende_certificado": False,
        "aval_organizacion": "Open Source Community",
        "estado": "publicado",
        "categoria": {"id": 1, "nombre": "Backend", "slug": "backend"},
        "declaracion_cursado": {
            "aportado_por_estudiante": "Sofía Martínez",
            "tomo_el_curso": True
        }
    },
    {
        "id": 3,
        "titulo": "React 19 y Vite: Arquitectura de Interfaces Web",
        "tema": "Frontend & React",
        "version": "2026",
        "anio_edicion": 2026,
        "docentes": "Lic. Carlos Paez",
        "url": "https://react.dev/learn",
        "tiene_cuestionarios": False,
        "requiere_examen": False,
        "extiende_certificado": True,
        "aval_organizacion": "Frontend Masters Latino",
        "estado": "publicado",
        "categoria": {"id": 2, "nombre": "Frontend", "slug": "frontend"},
        "declaracion_cursado": {
            "aportado_por_estudiante": "Lucas Gómez",
            "tomo_el_curso": False
        }
    }
]

@app.get("/health", summary="Healthcheck del servicio")
def healthcheck():
    """Endpoint de comprobación de salud del backend."""
    return {"status": "ok"}

@app.get("/cursos", summary="Listado de cursos (ruta directa)")
def get_cursos_direct():
    """Devuelve el catálogo de cursos (compatibilidad con especificación del docente)."""
    return CURSOS_MOCK

@app.get("/api/v1/cursos", summary="Listado de cursos (ruta API v1)")
def get_cursos_v1():
    """Devuelve el catálogo de cursos formateado para el frontend."""
    return CURSOS_MOCK
