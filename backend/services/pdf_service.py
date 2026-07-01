import io
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from backend.services.student_services import get_student
from backend.services.assessment import get_assessment_scores
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from reportlab.platypus import Image

def create_scores_chart(scores: dict) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.barh(list(scores.keys()), list(scores.values()), color='#4F8BF9')
    ax.set_xlim(0, 1)
    ax.set_xlabel('Score')
    ax.set_title('Interest Profile')
    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150)
    plt.close()
    img_buffer.seek(0)
    return img_buffer

def generate_report(student_id: int) -> io.BytesIO:
    """
    Generates a personalised PDF career report for a student.
    Args:
        student_id (int): The student's unique identifier
    Returns:
        io.BytesIO: PDF file as a bytes buffer
    """
    student_data = get_student(student_id)
    scores = get_assessment_scores(student_id)

    print("=" * 80)
    print("Requested student_id:", student_id)
    print("Student data:", student_data)
    print("Index 3:", repr(student_data[3]))
    print("Index 5:", repr(student_data[5]))
    print("=" * 80)

    name = student_data[1]
    city = student_data[2]
    stream_preference = student_data[3] or "Not specified"
    interests = student_data[4] or ""
    academic_level = student_data[5] or "Not specified"
    recommended_stream = student_data[7] or "Pending"
    degrees_json = student_data[8]
    justification = student_data[9] or "Not yet generated."
    roadmap_json = student_data[10]

    degrees = json.loads(degrees_json)['degrees'][:3] if degrees_json else []
    roadmap = json.loads(roadmap_json) if roadmap_json else {}

    # Set up PDF buffer and document
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
        fontSize=22, textColor=colors.HexColor('#1a1a2e'), spaceAfter=4)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
        fontSize=11, textColor=colors.HexColor('#555555'), spaceAfter=2)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading1'],
        fontSize=13, textColor=colors.HexColor('#4F8BF9'), spaceAfter=6, spaceBefore=12)
    subheading_style = ParagraphStyle('CustomSubHeading', parent=styles['Heading2'],
        fontSize=11, textColor=colors.HexColor('#333333'), spaceAfter=4, spaceBefore=8)
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#444444'), spaceAfter=4, leading=14)
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'],
        fontSize=8, textColor=colors.grey)

    def divider():
        return Table([['']], colWidths=[6.5*inch], rowHeights=[2],
                     style=TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#4F8BF9'))]))

    story = []

    # ── PAGE 1: HEADER & STUDENT PROFILE ──────────────────────────────────────

    story.append(Paragraph("NextGen Forge Technologies", title_style))
    story.append(Paragraph("AI Career Guidance & Admission Intelligence Platform", subtitle_style))
    story.append(Paragraph(f"Personalised Career Report — {name}", subtitle_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y')}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(divider())
    story.append(Spacer(1, 14))

    # Student Profile
    story.append(Paragraph("Student Profile", heading_style))
    profile_data = [
        ['Name', name],
        ['City', city],
        ['Stream Preference', stream_preference],
        ['Academic Level', f"{academic_level}%"],
        ['Interests', interests],
        ['Recommended Stream', recommended_stream],
    ]
    profile_table = Table(profile_data, colWidths=[2*inch, 4.5*inch])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EEF2FF')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a1a2e')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9FF')]),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 16))

    # Interest Profile Scores
    story.append(Paragraph("Interest Profile Scores", heading_style))
    story.append(Paragraph(
        "Your interest scores across domains based on the 20-question assessment:",
        body_style))
    story.append(Spacer(1, 8))

    if scores:
        score_data = [['Domain', 'Score (0–1)', 'Level']]
        for domain, score in scores.items():
            level = 'High' if score >= 0.7 else 'Medium' if score >= 0.4 else 'Low'
            score_data.append([domain, f"{score:.2f}", level])
        score_table = Table(score_data, colWidths=[3*inch, 1.75*inch, 1.75*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F8BF9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9FF')]),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ]))
        chart_buffer = create_scores_chart(scores)
        story.append(Image(chart_buffer, width=5*inch, height=2.5*inch))

    story.append(PageBreak())

    # ── PAGE 2: STREAM RECOMMENDATION & DEGREES ───────────────────────────────

    story.append(Paragraph("Stream Recommendation", heading_style))
    story.append(Paragraph(f"<b>Recommended Stream:</b> {recommended_stream}", body_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Justification:</b>", body_style))
    story.append(Paragraph(justification, body_style))
    story.append(Spacer(1, 16))

    story.append(divider())
    story.append(Spacer(1, 14))

    story.append(Paragraph("Top 3 Recommended Degree Pathways", heading_style))
    story.append(Paragraph(
        "Based on your interest profile and recommended stream, the following degree programmes are most suited for you:",
        body_style))
    story.append(Spacer(1, 10))

    if degrees:
        for i, degree in enumerate(degrees, 1):
            story.append(Paragraph(f"{i}. {degree.get('degree_name', 'N/A')}", subheading_style))
            story.append(Paragraph(degree.get('description', ''), body_style))
            career_paths = ', '.join(degree.get('career_pathways', []))
            story.append(Paragraph(f"<b>Career Pathways:</b> {career_paths}", body_style))
            exams = ', '.join(degree.get('entrance_exams', []))
            story.append(Paragraph(f"<b>Entrance Exams:</b> {exams}", body_style))
            story.append(Paragraph(f"<b>Timeline:</b> {degree.get('timeline', 'N/A')}", body_style))
            story.append(Spacer(1, 10))
    else:
        story.append(Paragraph("Degree recommendations not yet generated.", body_style))

    story.append(PageBreak())

    # ── PAGE 3: CAREER ROADMAP ─────────────────────────────────────────────────

    story.append(Paragraph("AI-Generated Career Roadmap", heading_style))
    story.append(Spacer(1, 8))

    if roadmap:
        story.append(Paragraph("Class 11–12 Preparation", subheading_style))
        story.append(Paragraph(roadmap.get('class_11_12_preparation', ''), body_style))
        story.append(Spacer(1, 8))

        story.append(Paragraph("Entrance Exam Timeline", subheading_style))
        for exam in roadmap.get('entrance_exam_timeline', []):
            story.append(Paragraph(
                f"<b>{exam.get('exam', '')}:</b> {exam.get('when', '')} — {exam.get('preparation_tip', '')}",
                body_style))
        story.append(Spacer(1, 8))

        story.append(Paragraph("Undergraduate Milestones", subheading_style))
        for milestone in roadmap.get('undergraduate_milestones', []):
            story.append(Paragraph(
                f"<b>{milestone.get('year', '')}:</b> {milestone.get('focus', '')}. {milestone.get('goals', '')}",
                body_style))
        story.append(Spacer(1, 8))

        story.append(Paragraph("Key Skills to Develop", subheading_style))
        skills = ', '.join(roadmap.get('skill_development', []))
        story.append(Paragraph(skills, body_style))
        story.append(Spacer(1, 8))

        story.append(Paragraph("Internship Milestones", subheading_style))
        story.append(Paragraph(roadmap.get('internship_milestones', ''), body_style))
        story.append(Spacer(1, 8))

        story.append(Paragraph("Industry Entry Pathway", subheading_style))
        story.append(Paragraph(roadmap.get('industry_entry_pathway', ''), body_style))
    else:
        story.append(Paragraph("Career roadmap not yet generated. Please complete the roadmap step first.", body_style))

    story.append(PageBreak())

    # ── PAGE 4: NEXT STEPS ACTION PLAN ────────────────────────────────────────

    story.append(Paragraph("Personalised Next Steps Action Plan", heading_style))
    story.append(Spacer(1, 8))

    interests_list = interests.split(', ') if interests else []
    action_items = [
        f"Confirm your stream choice as <b>{recommended_stream}</b> and discuss with your school counsellor.",
        "Begin preparing for the relevant entrance examinations based on your top degree choices.",
        f"Strengthen your core subjects: {', '.join(interests_list[:3]) if interests_list else 'your chosen subjects'}.",
        "Research the top colleges for your chosen stream and note their application deadlines.",
        "Build foundational skills aligned with your career aspirations through online courses and projects.",
        "Speak with professionals in your areas of interest to gain real-world perspective.",
        "Revisit this platform regularly to update your profile and get refined recommendations.",
    ]

    for item in action_items:
        story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 24))
    story.append(divider())
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f"This report was generated by the NextGen Forge AI Career Guidance Platform on {datetime.now().strftime('%d %B %Y')}. "
        "For support, contact hr@nextgenforgetechnologies.com | Ref: NFGT/HR/INT/2026/160",
        footer_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer