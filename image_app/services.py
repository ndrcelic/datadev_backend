def calculate_coordinates(x, y, w, h):
    x_point, y_point, width, height = x, y, w, h

    if w < 0 and h < 0:
        x_point = x + width
        y_point = y + height
        width = abs(w)
        height = abs(h)
    elif w < 0:
        x_point = x + width
        width = abs(w)
    elif h < 0:
        y_point = y + height
        height = abs(h)

    return x_point, y_point, width, height