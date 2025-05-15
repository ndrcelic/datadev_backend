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

def from_json_to_coco(json_data):
    coco_dataset = {
        "image": {"id": json_data["id"], "path": json_data["url"]},
        "boxes": [],
        "polygons": [],
        "points": []
    }


    for box in json_data["boxes"]:
        coco_dataset["boxes"].append({
            "id": box["id"],
            "image_id": box["image_id"],
            "x_point": box["x_point"],
            "y_point": box["y_point"],
            "width": box["width"],
            "height": box["height"],
            "description": box["description"],
        })

    for polygon in json_data["polygons"]:
        coco_dataset["polygons"].append({
            "id": polygon["id"],
            "image_id": polygon["image_id"],
            "description": polygon["description"],
        })


    for polygon in json_data["polygons"]:
        for point in polygon["points"]:
            coco_dataset["points"].append({
                "id": point["id"],
                "image_id": polygon["image_id"],
                "polygon_id": point["polygon_id"],
                "x_point": point["x_point"],
                "y_point": point["y_point"],
                "ordinal": point["ordinal"],
            })

    from pprint import pprint

    return coco_dataset