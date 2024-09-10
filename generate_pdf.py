'''Lay out SVG images in grid and generate PDF.'''
import os
import calendar
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import draw_routes


def draw_calendar_with_routes(pdf_output, files_grouped):
    '''Draw calendar grid with SVGs'''
    # set up canvas
    c = canvas.Canvas(pdf_output, pagesize=letter)
    c.setPageSize((11 * inch, 17 * inch))

    # set margins and grid dimensions
    margin = 0.5 * inch
    cell_width = 1.5 * inch
    cell_height = 1.5 * inch

    # determine year based on earliest file
    year = min(grouped_files.keys()).year

    # find first day of year
    for week_num in range(1, 53):
        for day_of_week in range(7):  # Sun = 0, Sat = 6
            week_start = datetime.strptime(
                f"{year} {week_num} {day_of_week}", "%Y %W %w").date()
            if week_start in grouped_files:
                svg_files = grouped_files[week_start]
                x = margin + day_of_week * cell_width
                y = 17 * inch - margin - week_num * cell_height

                for svg_fie in svg_files:
                    drawing = svg2rlg(svg_fie)
                    renderPDF.draw(drawing, c, x, y)

    # draw grid
    draw_grid(c, margin, cell_width, cell_height)

    # save PDF
    c.save()


def draw_grid(c, margin, cell_width, cell_height):
    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    # draw column labels
    for i, day in enumerate(days_of_week):
        x = margin + i * cell_width + 0.5 * cell_width
        y = 17 * inch - margin + 0.2 * inch
        c.drawCentredString(x, y, day)

    # draw grid lines for each week and day
    for row in range(52):
        y = 17 * inch - margin - row * cell_height
        for col in range(7):
            x = margin + col * cell_width
            c.rect(x, y, cell_width, cell_height, stroke=1, fill=0)


# LAUNCH CODES
grouped_files = draw_routes.group_gpx_files_by_date('data/activities_gpx')

output_pdf = 'route-calendar.pdf'
draw_calendar_with_routes(output_pdf, grouped_files)
