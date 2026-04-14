from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path

try:
    from google.adk.agents.llm_agent import Agent
except Exception:
    from google.adk.agents import Agent

from google.adk.models.lite_llm import LiteLlm

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

#PREGUNTAS LAB: Documento salida txt o pdf? 

def generate_section(name: str, topic: str) -> Dict[str, Any]:
    content = f"""
{name}

Ortony, Clore, y Collins (OCC) enunciaron un modelo psicológico según el cual las emociones se pueden explicar por la interrelación de los valores de 11 dimensiones definidas como 22 emociones. Este modelo, se ha utilizado para incorporar emociones en la definición del comportamiento de sistemas de IA en general, y de agentes en particular. 

El modelo OCC (Ortony, Clore y Collins) constituye una de las aproximaciones más relevantes en el estudio de las emociones en sistemas artificiales. En el contexto de {topic}, este modelo permite estructurar las emociones en función de evaluaciones cognitivas relacionadas con eventos, agentes y objetos. Estas evaluaciones se clasifican en diferentes categorías que facilitan la representación de emociones como alegría, tristeza, orgullo o culpa dentro de sistemas computacionales.

En particular, el modelo distingue entre emociones derivadas de consecuencias de eventos, acciones de agentes y características de objetos. Esta diferencia resulta fundamental para su implementación en agentes inteligentes, ya que permite explorar estados del entorno a respuestas emocionales coherentes y explicables. En el ámbito de {topic}, este enfoque permite mejorar la toma de decisiones y la adaptabilidad de los sistemas.
Cuando hablamos de evaluar a otra persona antes de votar por ella, negociar o incluso considerar un compromiso personal, lo más relevante no son únicamente sus palabras, su apariencia o sus acciones aisladas, sino sus valores, prioridades y lo que realmente le importa. Lo que mueve a alguien se refleja en sus emociones, porque las emociones son reacciones evaluativas ante situaciones significativas, y nos dicen qué considera bueno o malo, justo o injusto, agradable o desagradable.

1. Las emociones como ventana a los valores y prioridades
Las emociones no son simples reflejos automáticos, ni se pueden reducir a un patrón fijo de reacciones corporales, faciales o cognitivas. Según la perspectiva constructivista y el modelo OCC (Ortony, Clore y Collins), las emociones emergen cuando múltiples representaciones de una situación significativa ocurren simultáneamente: pensamientos, sentimientos, expresiones faciales, reacciones corporales e inclinaciones a actuar. Por ejemplo:
El miedo no es solo un corazón acelerado o los ojos abiertos; es la co-ocurrencia de percepciones de amenaza en el pensamiento, sensaciones físicas, expresiones y motivaciones a actuar.
La ira surge cuando percibimos un resultado negativo y al mismo tiempo juzgamos la acción de alguien como culpable o inadecuada.

Esto significa que, para entender a una persona, no basta con observar cómo se comporta en un momento concreto. Es necesario comprender qué situaciones provocan reacciones emocionales en ella, cómo estas reacciones se combinan y qué valores subyacen a esas respuestas.

2. Tipos de evaluaciones y situaciones
El modelo OCC clasifica las emociones en tres grandes focos de evaluación:
	1.	Eventos: Se evalúa el resultado de un suceso según si favorece o perjudica nuestros objetivos. Por ejemplo, sentir tristeza por una injusticia o satisfacción por un logro propio o ajeno.
	2.	Acciones: Se evalúa la moralidad o idoneidad de una acción según estándares personales, sociales o culturales. Por ejemplo, sentir orgullo por un acto propio digno o reproche hacia alguien que actúa mal.
	3.	Objetos: Se evalúan las propiedades de personas, ideas o cosas según nuestros gustos o actitudes. Por ejemplo, sentir amor o disgusto hacia algo que percibimos como agradable o repulsivo.

Cada uno de estos focos da lugar a distintas emociones, y la combinación de evaluaciones puede generar emociones complejas. Por ejemplo, ver que alguien ha sufrido un daño injusto (evento negativo) y a la vez juzgar al culpable como moralmente reprochable puede generar ira más que simple tristeza.

3. La importancia de la situación y el contexto
Una misma emoción no se manifiesta igual en todas las situaciones. Por ejemplo:
El miedo ante un oso en el bosque requiere acción inmediata y cambios fisiológicos intensos.
El miedo ante un despido potencial genera preocupación, tensión y planificación, pero no necesariamente cambios fisiológicos inmediatos.

Esto muestra que las emociones son situadas: dependen de las circunstancias, del contexto social y de la interpretación que la persona haga de la situación. Por eso, entender a alguien implica observar cómo reacciona en distintos contextos y qué importancia asigna a cada situación.

4. Las emociones y la cognición
Las emociones no son solo reacciones biológicas, sino que están profundamente ligadas a la cognición: pensamientos, expectativas, recuerdos y simulaciones mentales. Los humanos somos capaces de vivir en mundos “como si”: anticipamos resultados, imaginamos escenarios y recordamos experiencias. Esto significa que una persona puede sentir miedo, alegría o frustración no solo por eventos reales, sino por lo que imagina o anticipa. Conocer cómo alguien interpreta y anticipa los eventos nos permite entender mejor sus motivaciones y sus decisiones futuras.

5. Emociones, lenguaje y conceptos compartidos
El lenguaje juega un papel fundamental para identificar emociones y comprender a otros. Las palabras como “miedo”, “ira” o “tristeza” no son la emoción en sí, pero nos permiten estructurar y comunicar experiencias afectivas. Cada persona tiene esquemas compartidos de lo que significan ciertas emociones, y estos esquemas guían tanto lo que siente como lo que dice. Esto hace que, al preguntar a alguien sobre sus sentimientos o al observar cómo los describe, podamos inferir qué valora y cómo organiza sus experiencias emocionales.

6. Implicaciones prácticas
Si quisiéramos evaluar a alguien antes de votar, negociar o casarnos, un enfoque práctico sería:
Observar sus reacciones emocionales frente a distintos tipos de situaciones: logros, injusticias, conflictos, dilemas morales, situaciones sociales.
Preguntar sobre sus prioridades y metas: cómo decide qué es importante, cómo maneja las frustraciones y los logros.
Prestar atención a cómo interpreta los eventos: no solo lo que siente, sino qué significado asigna a lo que le ocurre.
Analizar patrones consistentes: no basta un comportamiento aislado; necesitamos ver cómo se repite o varía su evaluación emocional según el contexto.
Escuchar cómo usa el lenguaje emocional: las palabras que elige reflejan sus esquemas y valores, y ayudan a identificar qué le importa.

Además, la incorporación del modelo OCC en agentes inteligentes contribuye significativamente a mejorar la interacción humano-máquina. Los sistemas pueden simular comportamientos más naturales, mostrando respuestas emocionales contextualizadas que incrementan la aceptación por parte de los usuarios. Esto es especialmente útil en entornos como educación, simulaciones o sistemas multiagente.

Por otro lado, existen desafíos asociados a la implementación del modelo, como la complejidad en la definición de reglas cognitivas y el coste computacional. Sin embargo, a pesar de estas limitaciones, el modelo OCC sigue siendo una base sólida para el desarrollo de agentes emocionales avanzados en el contexto de {topic}.
"""
    return {
        "name": name,
        "content": content.strip()
    }


def count_words(text: str) -> Dict[str, Any]:
    return {"word_count": len(text.split())}


def generate_pdf(sections: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
    path = "output/informe.pdf"
    Path("output").mkdir(exist_ok=True)

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph(title, styles["Title"]))

    for s in sections:
        elements.append(Paragraph(s["name"], styles["Heading2"]))
        elements.append(Paragraph(s["content"], styles["Normal"]))

    doc.build(elements)
    return {"pdf_path": path}


def build_document(sections: List[Dict[str, Any]], title: str, pdf_path: str) -> Dict[str, Any]:
    total_words = sum(s["word_count"] for s in sections)

    return {
        "title": title,
        "sections": [{"name": s["name"], "word_count": s["word_count"]} for s in sections],
        "total_words": total_words,
        "num_sections": len(sections),
        "num_references": 5,
        "pdf_path": pdf_path
    }


root_agent = Agent(
    model=LiteLlm(
        model="openai/gpt-oss-120b",
        api_base="https://api.poligpt.upv.es/",
        api_key="YOUR_API_KEY"
    ),
    name="document_agent",
    description="Genera documentos estructurados sobre modelos emocionales OCC en agentes inteligentes",
    instruction=(
        "Debes generar un documento académico siguiendo estos pasos:\n"
        "1) Crear un título sobre el tema\n"
        "2) Generar las siguientes secciones obligatorias:\n"
        "   - Introducción\n"
        "   - Estado del arte\n"
        "   - Desarrollo\n"
        "   - Conclusiones\n"
        "   - Bibliografía\n"
        "3) Para cada sección usar la tool generate_section\n"
        "4) Para cada contenido usar count_words\n"
        "5) Cada sección debe tener al menos 150 palabras\n"
        "6) El documento completo debe tener al menos 450 palabras\n"
        "7) Generar PDF con generate_pdf\n"
        "8) Construir JSON final con build_document\n"
        "9) Es obligatorio cumplir estructura y longitudes"
    ),
    tools=[generate_section, count_words, generate_pdf, build_document],
)