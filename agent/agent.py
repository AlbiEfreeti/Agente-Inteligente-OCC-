"""
Agente Generador de Informes Académicos - Modelo emocional OCC.
Estructura: Introducción, Desarrollo (párrafos), Conclusiones y Bibliografía.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import csv

try:
    from google.adk.agents.llm_agent import Agent
except Exception:
    from google.adk.agents import Agent

from google.adk.models.lite_llm import LiteLlm 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# --- 1. ESTRUCTURA DE DATOS ---

@dataclass(frozen=True)
class OccRow:
    """Representa una sección de contenido, ya sea del CSV o generada."""
    contenido: str
    nombre: str = ""
    word_count: int = 0

class OccDataStore:
    """Almacén para los datos de entrada (CSV) y de salida (Informe final)."""
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self._db: Optional[Dict[str, OccRow]] = None
        self.report_sections: List[OccRow] = []

    def _load_data(self) -> Dict[str, OccRow]:
        path = self.base_dir / "occ.csv"
        db: Dict[str, OccRow] = {}
        if not path.exists(): return db
        try:
            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    name = (r.get("seccion") or r.get("name") or "").strip()
                    content = (r.get("contenido") or r.get("content") or "").strip()
                    if name:
                        db[name] = OccRow(contenido=content, nombre=name)
        except Exception: pass
        return db

    def get_content(self, section_name: str) -> str:
        if self._db is None: self._db = self._load_data()
        row = self._db.get(section_name)
        return row.contenido if row else "Información académica sobre el modelo emocional OCC."

    def save_generated_section(self, name: str, text: str):
        words = len(text.split())
        self.report_sections.append(OccRow(contenido=text, nombre=name, word_count=words))

    def get_final_report_data(self) -> Dict[str, Any]:
        total_words = sum(s.word_count for s in self.report_sections)
        num_refs = 0
        for s in self.report_sections:
            if "Bibliografía" in s.nombre or "Referencias" in s.nombre:
                # Contamos líneas reales de referencias
                lineas = [l for l in s.contenido.split('\n') if len(l.strip()) > 10]
                num_refs = len(lineas)
        return {
            "sections_list": [{"name": s.nombre, "word_count": s.word_count} for s in self.report_sections],
            "total_words": total_words,
            "num_refs": num_refs,
            "num_sections": len(self.report_sections)
        }

DATA = OccDataStore(base_dir=Path(__file__).resolve().parent)

# --- 2. TOOLS ---

def generate_section(name: str, topic: str) -> Dict[str, Any]:
    """Paso (1): Recupera contenido base del almacén."""
    content = DATA.get_content(name)
    return {"name": name, "content": content}

def count_words(name: str, text: str) -> Dict[str, Any]:
    """Paso (3): Registra la sección redactada en el sistema."""
    DATA.save_generated_section(name, text)
    count = len(text.split())
    return {"status": f"Sección '{name}' registrada", "word_count": count}

def generate_pdf(title: str) -> Dict[str, Any]:
    """Paso (4): Crea el PDF usando las secciones registradas en DATA."""
    path = "output/informe.pdf"
    Path("output").mkdir(exist_ok=True)
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    
    elements = [Paragraph(f"<b>{title}</b>", styles["Title"]), Spacer(1, 0.2*inch)]
    
    for s in DATA.report_sections:
        elements.append(Paragraph(s.nombre, styles["Heading2"]))
        # El Desarrollo y demás secciones se pintan como párrafos normales
        for paragraph in s.contenido.split('\n'):
            if paragraph.strip():
                elements.append(Paragraph(paragraph.strip(), styles["Normal"]))
                elements.append(Spacer(1, 0.1*inch))
        elements.append(Spacer(1, 0.1*inch))
    
    doc.build(elements)
    return {"pdf_path": path}

def build_document(title: str, pdf_path: str) -> Dict[str, Any]:
    """
    Finaliza el proceso. Ahora num_sections y la lista de secciones 
    son totalmente dinámicas según lo que el agente decidió registrar.
    """
    report = DATA.get_final_report_data()
    
    # Comprobación de seguridad para el alumno: 
    # Si el agente ha sido perezoso y solo ha puesto 2 secciones, 
    # el JSON lo reflejará honestamente.
    return {
        "title": title,
        "sections": report["sections_list"],
        "total_words": report["total_words"],
        "num_sections": report["num_sections"],
        "num_references": report["num_refs"],
        "pdf_path": pdf_path
    }
# --- 3. AGENTE ---

root_agent = Agent(
    model=LiteLlm(
        model="openai/gpt-oss-120b", 
        api_base="https://api.poligpt.upv.es/", 
        api_key="sk-LFXs1kjaSxtEDgOMlPUOpA"
    ),
    name="document_agent",
    instruction=(
        
        "Eres un redactor de documentos académicos. Tu flujo de trabajo es estrictamente secuencial y basado en herramientas.\n\n"
        "POR CADA SECCIÓN (Introducción, 3 secciones independientes de Desarrollo, Conclusiones y Bibliografía):\n"
        "1. Llama a 'generate_section' para obtener la información base del CSV.\n"
        "2. Redacta el contenido formal basado en esa información.\n"
        "3. Llama a 'count_words' para registrar esa sección y sus palabras.\n\n"
        "REGLAS CRÍTICAS DE FINALIZACIÓN:\n"
        "- Una vez registradas las 6 secciones, debes llamar a 'generate_pdf' para crear el archivo.\n"
        "- Acto seguido, DEBES llamar a 'build_document' para consolidar el JSON final.\n\n"
        "CONFIRMACIÓN FINAL:\n"
        "- Al terminar todo el proceso técnico, avisa por el chat de que el documento está listo, "
        "confirmando que se ha generado el PDF y que todo ha quedado registrado correctamente. "
        "No hace falta que sea un mensaje rígido, usa un tono profesional y amable.\n\n"
        "ADVERTENCIA: No des la tarea por cerrada hasta haber ejecutado 'build_document'."
    ),
    tools=[generate_section, count_words, generate_pdf, build_document],
)