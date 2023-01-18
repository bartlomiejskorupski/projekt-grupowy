from guizero import Box

def addPadding(box: Box, padding: int = 10, debug_border: bool = False):
  border = debug_border if 2 else None
  Box(box, align='top', width='fill', height=padding, border=border)
  Box(box, align='bottom', width='fill', height=padding, border=border)
  Box(box, align='left', height='fill', width=padding, border=border)
  Box(box, align='right', height='fill', width=padding, border=border)
