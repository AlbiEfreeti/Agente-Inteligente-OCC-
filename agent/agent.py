"""
Agente Generador de Informes Académicos - Modelo OCC
Configurado para el flujo de evaluación de la Sesión 2 de ADK.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
import csv
import json

try:
    from google.adk.agents.llm_agent import Agent
except Exception:
    from google.adk.agents import Agent

from google.adk.models.lite_llm import LiteLlm 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# --- 1. ALMACÉN DE DATOS (Estructura CsvDataStore) ---
@dataclass(frozen=True)
class OccRow:
    contenido: str

class OccDataStore:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self._db: Optional[Dict[str, OccRow]] = None

    def _load_data(self) -> Dict[str, OccRow]:
        path = self.base_dir / "occ.csv"
        db: Dict[str, OccRow] = {}
        if not path.exists():
            return db
        try:
            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    name = (r.get("seccion") or r.get("name") or "").strip()
                    content = (r.get("contenido") or r.get("content") or "").strip()
                    if name:
                        db[name] = OccRow(contenido=content)
        except Exception:
            pass
        return db

    def get_content(self, section_name: str, topic: str = "modelo emocional OCC") -> str:
        if self._db is None:
            self._db = self._load_data()
        
        # 1. Intentamos obtener la sección del CSV
        row = self._db.get(section_name)
        if row:
            return row.contenido
            
        # 2. SI NO EXISTE (Igual que el default del ejemplo de Valencia)
        # Devolvemos tu texto base completo para que el agente siempre tenga qué escribir
        return """
        Ortony, Clore, y Collins (OCC) definen un modelo donde las emociones son 
        reacciones evaluativas ante eventos, agentes y objetos. Se clasifican en 
        22 emociones basadas en metas, normas y gustos. Es fundamental para la 
        IA emocional y la adaptabilidad de agentes inteligentes.
        """.strip()

# Instancia global de datos
DATA = OccDataStore(base_dir=Path(__file__).resolve().parent)

# --- 2. TOOLS ---

def generate_section(name: str, topic: str) -> Dict[str, Any]:
    """Obtiene el contenido de una sección desde el CSV o conocimiento base."""
    content = DATA.get_content(name, topic)
    return {"name": name, "content": content}

def count_words(text: str) -> Dict[str, Any]:
    """Audita la longitud de la sección para el JSON de salida"""
    return {"word_count": len(text.split())}

def generate_pdf(sections: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
    """Genera el documento PDF procesando subtítulos internos en el Desarrollo."""
    path = "output/informe.pdf"
    Path("output").mkdir(exist_ok=True)
    
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    
    # Personalizamos un poco los estilos para que se vean mejor
    style_title = styles["Title"]
    style_h2 = styles["Heading2"] # Para "Introducción", "Desarrollo", etc.
    style_h3 = styles["Heading3"] # Para los subtítulos internos del Desarrollo
    style_body = styles["Normal"]
    
    elements = [Paragraph(title, style_title), Spacer(1, 0.2*inch)]
    
    for s in sections:
        # 1. Añadimos el nombre de la sección principal
        elements.append(Paragraph(s["name"], style_h2))
        
        # 2. Procesamos el contenido
        content = s.get("content", "")
        
        if s["name"] == "Desarrollo":
            # Dividimos el contenido por líneas para detectar los subtítulos <b>
            lines = content.split('\n')
            for line in lines:
                clean_line = line.strip()
                if not clean_line:
                    continue
                
                # Si la línea contiene etiquetas de negrita, la tratamos como subtítulo H3
                if "<b>" in clean_line or "1." in clean_line[:3] or "2." in clean_line[:3]:
                    elements.append(Spacer(1, 0.1*inch))
                    elements.append(Paragraph(clean_line, style_h3))
                else:
                    elements.append(Paragraph(clean_line, style_body))
        else:
            # Para el resto de secciones, contenido normal
            elements.append(Paragraph(content, style_body))
            
        elements.append(Spacer(1, 0.15*inch))
    
    doc.build(elements)
    return {"pdf_path": path}

def build_document(sections: List[Dict[str, Any]], title: str, pdf_path: str) -> Dict[str, Any]:
    """Retorna la estructura necesaria para el evaluador."""
    total_words = sum(s.get("word_count", 0) for s in sections)
    
    # Cálculo de referencias buscando en la sección Bibliografía
    num_refs = 0
    for s in sections:
        if "Bibliografía" in s["name"]:
            # Contamos líneas no vacías como referencias
            num_refs = len([line for line in s.get("content", "").split('\n') if line.strip()])

    result = {
        "title": title,
        "sections": [{"name": s["name"], "word_count": s.get("word_count", 0)} for s in sections],
        "total_words": total_words,
        "num_sections": len(sections),
        "num_references": num_refs,
        "pdf_path": pdf_path,
        "status": "COMPLETED"
    }
    
    # IMPORTANTE: Retornamos el diccionario para el evaluador
    return result


# --- 3. ROOT AGENT ---

root_agent = Agent(
    model=LiteLlm(
        model="openai/gpt-oss-120b", 
        api_base="https://api.poligpt.upv.es/", 
        api_key="sk-LFXs1kjaSxtEDgOMlPUOpA"
    ),
    name="document_agent",
    description="Agente que genera informes de OCC siguiendo la trayectoria ADK[cite: 450].",
    instruction=(
        "Eres un experto en IA Emocional. Tu misión es generar un informe académico EXTENSO, original y "
        "profundamente estructurado sobre el modelo OCC, usando el CSV como base informativa.\n\n"
        "REGLA CRÍTICA DE FORMATO Y EXTENSIÓN:\n"
        "1. TÍTULO: Crea un título profesional de MÁXIMO 10 PALABRAS.\n"
        "2. EVITAR CUADRADOS NEGROS: Usa solo letras, números, puntos y comas. Prohibido usar  '•', '‑', o guiones largos.\n"
        "3. REDACCIÓN EXTENSA: No copies el CSV. Amplía cada sección con lenguaje técnico profundo para que el informe "
        "tenga una extensión académica real.\n\n"
        "FLUJO TÉCNICO ESTRICTAMENTE SECUENCIAL:\n"
        "1. TÍTULO: Define el título del informe.\n"
        "2. FASE DE OBTENCIÓN Y REDACCIÓN (Repite para: Introducción, Desarrollo, Conclusiones, Bibliografía):\n"
        "   a) Llama a 'generate_section' para obtener la base.\n"
        "   b) REDACCIÓN: Amplía el contenido. En el 'Desarrollo', separa subapartados con SALTO DE LÍNEA y usa este formato:\n"
        "      <b>1. Taxonomia y Estructura del Modelo OCC</b>\n"
        "      [Escribe aquí un análisis técnico extenso de los dominios y las 22 emociones]\n"
        "      <b>2. Procesos Cognitivos de Evaluacion</b>\n"
        "      [Escribe aquí un análisis técnico extenso sobre variables de intensidad y reglas lógicas]\n"
        "      <b>3. Aplicaciones y Casos de Uso en Sistemas Inteligentes</b>\n"
        "      [Escribe aquí ejemplos detallados en robótica, videojuegos y tutoría]\n"
        "   c) AUDITORÍA: Llama a 'count_words' sobre TU texto redactado.\n"
        "3. FASE DE PRODUCCIÓN:\n"
        "   a) Llama a 'generate_pdf' con el título corto y las secciones extendidas.\n"
        "   b) FINALIZACIÓN: Llama a 'build_document' con los datos finales.\n\n"
        "REGLA DE ORO: Tu única forma de trabajar es mediante herramientas. No escribas el informe en el chat. "
        "Al terminar, confirma en español que el PDF se generó con éxito en 'output' con el formato requerido."
    ),

    tools=[generate_section, count_words, generate_pdf, build_document],
)