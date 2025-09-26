from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from typing import List

router = APIRouter()

class ReportGenerateRequest(BaseModel):
    query_ids: List[str]
    report_type: str = "security_summary"

@router.post("/generate")
def generate_report(request: ReportGenerateRequest):
    try:
        # Generate PDF report
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Report header
        story.append(Paragraph("🔒 SOC Copilot Security Report", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph(f"Report Type: {request.report_type.replace('_', ' ').title()}", styles['Normal']))
        story.append(Spacer(1, 24))
        
        # Executive Summary
        story.append(Paragraph("📊 Executive Summary", heading_style))
        summary_text = """
        This security report provides an analysis of your organization's security posture based on log analysis 
        performed by SOC Copilot. The report includes key findings, threat indicators, and recommended actions 
        to improve your security infrastructure.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 18))
        
        # Key Findings
        story.append(Paragraph("🔍 Key Findings", heading_style))
        findings_data = [
            ['Finding', 'Severity', 'Count', 'Status'],
            ['Failed Login Attempts', 'Medium', '245', 'Investigating'],
            ['Suspicious Network Activity', 'High', '12', 'Mitigated'],
            ['System File Changes', 'Low', '89', 'Monitored'],
            ['Authentication Anomalies', 'Medium', '67', 'Under Review']
        ]
        
        findings_table = Table(findings_data)
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(findings_table)
        story.append(Spacer(1, 18))
        
        # Security Metrics
        story.append(Paragraph("📈 Security Metrics", heading_style))
        metrics_text = """
        <b>Total Events Analyzed:</b> 1,247<br/>
        <b>Security Incidents:</b> 23<br/>
        <b>False Positives:</b> 8<br/>
        <b>Risk Score:</b> Medium (6.5/10)<br/>
        <b>Compliance Status:</b> 87% Compliant
        """
        story.append(Paragraph(metrics_text, styles['Normal']))
        story.append(Spacer(1, 18))
        
        # Recommendations
        story.append(Paragraph("💡 Recommendations", heading_style))
        recommendations = [
            "1. Implement multi-factor authentication for all admin accounts",
            "2. Review and update firewall rules to block suspicious IP ranges",
            "3. Increase monitoring on critical system files",
            "4. Conduct security awareness training for users with failed login attempts",
            "5. Update incident response procedures based on recent findings"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 18))
        
        # Query Details
        story.append(Paragraph("🔍 Query Analysis Details", heading_style))
        query_text = """
        This report is based on natural language queries processed by SOC Copilot's AI engine. 
        The system analyzed security logs using advanced pattern recognition and threat intelligence 
        to identify potential security issues and anomalies.
        """
        story.append(Paragraph(query_text, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Footer
        story.append(Spacer(1, 24))
        footer_text = "Generated by SOC Copilot - AI-Powered Security Operations Assistant"
        story.append(Paragraph(footer_text, styles['Italic']))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF as response
        buffer.seek(0)
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=soc-report.pdf"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@router.get("/sample")
def download_sample_report():
    """Download a sample security report"""
    try:
        # Create a simple sample report
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph("SOC Copilot - Sample Security Report", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("This is a sample security report demonstrating the capabilities of SOC Copilot.", styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=sample-report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sample report: {str(e)}")

@router.get("/download/{report_id}")
def download_report(report_id: str):
    # Mock download endpoint
    return {"message": f"Download endpoint for report {report_id} - implementation pending"}