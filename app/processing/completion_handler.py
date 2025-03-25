# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
"""Handles creation of PDF completion report"""
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class CompletionHandler:

    def __init__(self, element_handler, matching_frames):
        self.element_handler = element_handler
        self.matching_frames = matching_frames
        self.video_name = element_handler.selected_file_path.split("/")[-1].split(".")[0]

    def generate_completion_report(self, report_path):
        pdf_canvas = self._setup_pdf(report_path)

        self._generate_pdf_content(pdf_canvas)

        self._save_pdf(pdf_canvas)

    def _setup_pdf(self, report_path):
        # Create a PDF canvas
        pdf_canvas = canvas.Canvas(f"{report_path}/completion_report_{self.video_name}.pdf", pagesize=A4)

        # Set the title of the PDF
        pdf_canvas.setTitle(f"Completion Report for {self.video_name}")

        # Set the font and size
        pdf_canvas.setFont("Helvetica", 12)

        return pdf_canvas

    def _generate_pdf_content(self, pdf_canvas):
        # Add matching frames and accompanying details
        for i, frame in enumerate(self.matching_frames):
            # Start a new page for each frame (except the first one which is already on a new page)
            if i > 0:
                pdf_canvas.showPage()

            # Add title and subtitle to each page
            pdf_canvas.setFont("Helvetica-Bold", 16)
            pdf_canvas.drawCentredString(A4[0] / 2, A4[1] - 50,
                                         f"Report for {self.video_name}")
            pdf_canvas.setFont("Helvetica", 14)
            pdf_canvas.drawCentredString(A4[0] / 2, A4[1] - 75,
                                         f"Search term: {self.element_handler.search_term}")

            # Start position below title and subtitle
            y_position = A4[1] - 100

            # Add frame details
            pdf_canvas.setFont("Helvetica", 12)
            pdf_canvas.drawString(50, y_position,
                                  f"Matching Frame: {frame['filename'].split('/')[-1]}")
            y_position -= 20

            # Get frame dimensions and scale to fit
            image = Image.open(frame["filename"])
            width, height = image.size
            max_width = A4[0] - 100
            max_height = 300
            scale = min(max_width / width, max_height / height)
            scaled_width = width * scale
            scaled_height = height * scale

            # Position image below in the centre
            x_position = (A4[0] - scaled_width) / 2

            # Draw the image
            pdf_canvas.drawInlineImage(frame["filename"], x=x_position,
                                       y=y_position - scaled_height,
                                       width=scaled_width, height=scaled_height)

            # Add table with caption and timestamp
            table_y = y_position - scaled_height - 5

            # Define table dimensions
            table_width = A4[0] - 100
            table_x = 50
            table_row_height = 20
            
            # Calculate caption wrapping, margin and chars per line
            caption = frame["caption"]
            caption_width = table_width / 2 - 20
            max_chars_per_line = int(caption_width / 5)
            
            # Split caption into words and create wrapped lines
            words = caption.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + " " + word) <= max_chars_per_line or not current_line:
                    current_line += (" " + word if current_line else word)
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Calculate required height for the caption area
            line_height = 12
            required_caption_height = len(lines) * line_height
            
            # Table row height
            caption_row_height = max(table_row_height, required_caption_height + 10)
            
            # Draw the table borders and dividers
            pdf_canvas.rect(table_x, table_y - caption_row_height - table_row_height,
                            table_width, table_row_height + caption_row_height)
            pdf_canvas.line(table_x + table_width * 0.5, table_y - caption_row_height - table_row_height,
                            table_x + table_width * 0.5, table_y)
            pdf_canvas.line(table_x + table_width * 0.75, table_y - caption_row_height - table_row_height,
                            table_x + table_width * 0.75, table_y)
            pdf_canvas.line(table_x, table_y - table_row_height,
                            table_x + table_width, table_y - table_row_height)
            
            # Draw headers
            pdf_canvas.setFont("Helvetica-Bold", 10)
            pdf_canvas.drawCentredString(table_x + table_width * 0.25, table_y - 15, "Caption")
            pdf_canvas.drawCentredString(table_x + table_width * 0.625, table_y - 15, "Timestamp")
            pdf_canvas.drawCentredString(table_x + table_width * 0.875, table_y - 15, "Frame Number")
            
            # Draw each line of the caption
            pdf_canvas.setFont("Helvetica", 9)
            caption_y = table_y - table_row_height - (caption_row_height / 2) + ((len(lines) - 1) * line_height / 2)
            
            # Left margin for the caption text
            caption_left_margin = table_x + 10  # 10 pixels from the left border of the cell
            
            for line in lines:
                pdf_canvas.drawString(caption_left_margin, caption_y, line)
                caption_y -= line_height
            
            # Format timestamp as MM:SS:MS
            timestamp_formatted = f"{int(frame["timestamp"] // 60):02d}:{int(frame["timestamp"] % 60):02d}:{int((frame["timestamp"] % 1) * 1000):03d}"
            
            # Draw the timestamp and frame number
            pdf_canvas.drawCentredString(table_x + table_width * 0.625,
                                        table_y - table_row_height - (caption_row_height / 2), timestamp_formatted)
            pdf_canvas.drawCentredString(table_x + table_width * 0.875,
                                        table_y - table_row_height - (caption_row_height / 2), str(frame["filename"].split("/")[-1].split("_")[0]))
            
            # Update position for next element
            y_position -= (scaled_height + 60 + (caption_row_height - table_row_height))

    @staticmethod
    def _save_pdf(pdf_canvas):
        # Save the PDF file
        pdf_canvas.save()
        print("PDF saved successfully.")