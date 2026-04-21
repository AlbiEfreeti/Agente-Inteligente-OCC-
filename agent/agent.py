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
    result = {
        "title": title,
        "sections": report["sections_list"],
        "total_words": report["total_words"],
        "num_sections": report["num_sections"],
        "num_references": report["num_refs"],
        "pdf_path": pdf_path
    }

    return result

# --- 3. AGENTE ---

root_agent = Agent(
    model=LiteLlm(
        model="openai/gpt-oss-120b", 
        api_base="https://api.poligpt.upv.es/", 
        api_key="sk-LFXs1kjaSxtEDgOMlPUOpA"
    ),
    name="document_agent",
    instruction=(
        "Eres un analista académico experto en el Modelo OCC. Tu objetivo es generar un Documento Académico "
        "con una cohesión interna total y una profundidad técnica elevada.\n\n"
        "PROCESO DE PLANIFICACIÓN (Pensamiento previo):\n"
        "1. Selecciona 3 claves técnicas del CSV para el Desarrollo (ej. 'Taxonomia_22', 'Formula_Intensidad', 'Proceso_Appraisal').\n"
        "2. Identifica los autores y temas clave de esas secciones para asegurar que la Introducción, las Conclusiones "
        "y la Bibliografía giren en torno a esa elección. \n\n"
        "ESTRUCTURA Y REDACCIÓN:\n"
        "1. INTRODUCCIÓN LIBRE Y EXTENSA: Tienes libertad para elegir las claves del CSV que desees (como 'Introduccion' "
        "o 'Origen_Historico') y combinarlas con tu conocimiento. Debe presentar los temas específicos que se tratarán después.\n\n"
        "2. DESARROLLO (3 SECCIONES INDEPENDIENTES): Redacta cada una de las 3 claves elegidas con lenguaje formal y denso. "
        "No te limites a copiar; expande la lógica computacional y las implicaciones de cada concepto.\n\n"
        "3. CONCLUSIONES COHERENTES: Realiza una síntesis final que conecte directamente con los 3 temas del desarrollo, "
        "analizando su relevancia y limitaciones de forma crítica.\n\n"
        "4. BIBLIOGRAFÍA FILTRADA: Incluye exclusivamente las referencias (claves 'Ref_') que den soporte a los "
        "autores y temas que realmente has incluido en el documento.\n\n"
        "- Cada sección debe existir EXACTAMENTE UNA vez en todo el pdf. Tras ejecutar 'generate_pdf', verifica que esten las secciones unicas. \n"
        "PASOS TÉCNICOS OBLIGATORIOS:\n"
        "- Obtén los datos con 'generate_section' para cada bloque.\n"
        "- Registra CADA sección de forma individual con 'count_words' para asegurar la trazabilidad.\n"
        "- IMPORTANTE: Tras registrar todo, ejecuta 'generate_pdf' y 'build_document'. El pdf creado sera siempre 'informe.pdf'. El proceso NO es válido sin este último paso.\n\n"
        "AVISO FINAL: Al terminar, confirma de forma amable que el documento está listo, el PDF generado y el JSON consolidado."
    ),
    tools=[generate_section, count_words, generate_pdf, build_document],
)