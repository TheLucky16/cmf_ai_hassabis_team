import json, re
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)





def recommendations_json_to_md(json_path: str, md_path: str) -> None:
    """
    Convert recommendations JSON into a Markdown report.

    Parameters
    ----------
    json_path : str
        Path to recommendations JSON file.
    md_path : str
        Path where the Markdown file should be saved.
    """

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md = "# Personalized Learning Recommendations\n\n"

    for user in data.get("users", []):

        md += f"## {user.get('name', 'Unknown User')}\n\n"

        recommendations = user.get("recommendations", [])

        if not recommendations:
            md += "No recommendations available.\n\n"
            md += "---\n\n"
            continue

        for rec in recommendations:

            md += f"### {rec.get('lesson_title', 'Untitled Lesson')}\n\n"

            if "score" in rec:
                md += f"**Score:** {rec['score']}/100\n\n"

            if rec.get("matched_topics"):
                md += "**Matched Topics:**\n"
                for topic in rec["matched_topics"]:
                    md += f"- {topic}\n"
                md += "\n"

            if rec.get("existing_strengths"):
                md += "**Existing Strengths:**\n"
                for strength in rec["existing_strengths"]:
                    md += f"- {strength}\n"
                md += "\n"

            if rec.get("knowledge_gaps"):
                md += "**Knowledge Gaps:**\n"
                for gap in rec["knowledge_gaps"]:
                    md += f"- {gap}\n"
                md += "\n"

            if rec.get("recommendation_reason"):
                md += f"**Reason:** {rec['recommendation_reason']}\n\n"

        md += "---\n\n"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)



def md_to_pdf(md_path: str, pdf_path: str) -> None:
    """
    Convert a markdown file to a PDF.

    Parameters
    ----------
    md_path : str
        Path to markdown file.
    pdf_path : str
        Path where PDF should be saved.
    """

    def md_to_html(text: str) -> str:
        # bold
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

        # italic
        text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)

        return text

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()

    elements = []

    for line in lines:
        line = line.strip()

        if not line:
            elements.append(Spacer(1, 6))
            continue

        # horizontal rule
        if line == "---":
            elements.append(Spacer(1, 12))
            continue

        # headings
        if line.startswith("# "):
            elements.append(
                Paragraph(
                    md_to_html(line[2:]),
                    styles["Title"]
                )
            )

        elif line.startswith("## "):
            elements.append(
                Paragraph(
                    md_to_html(line[3:]),
                    styles["Heading1"]
                )
            )

        elif line.startswith("### "):
            elements.append(
                Paragraph(
                    md_to_html(line[4:]),
                    styles["Heading2"]
                )
            )

        # bullet points
        elif line.startswith("- "):
            elements.append(
                Paragraph(
                    f"• {md_to_html(line[2:])}",
                    styles["BodyText"]
                )
            )

        # normal text
        else:
            elements.append(
                Paragraph(
                    md_to_html(line),
                    styles["BodyText"]
                )
            )

    doc.build(elements)



def repair_recommendations_json(input_path: str, output_path: str) -> None:
    """
    Repairs common JSON formatting errors in recommendation files
    and writes a valid JSON file.

    Currently fixes:
    - Missing quote before colon in keys, e.g.
      "score:68  ->  "score":68
    """

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Fix malformed keys such as:
    # "score:68
    # "name:value
    text = re.sub(
        r'"([A-Za-z_][A-Za-z0-9_]*)\:([^"])',
        r'"\1":\2',
        text
    )

    # Validate JSON
    data = json.loads(text)

    # Write pretty formatted JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)