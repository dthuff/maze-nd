def get_color_dictionary(theme: str) -> dict:
    if theme == "default":
        color_dict = {"wall": (128, 128, 128),
                      "passage": (40, 40, 40),
                      "highlight": (200, 50, 50),
                      "border": (0, 0, 0)
                      }
    elif theme == "christmas":
        color_dict = {"wall": (80, 145, 82),
                      "passage": (19, 59, 26),
                      "highlight": (24, 24, 184),
                      "border": (8, 8, 102)
                      }
    else:
        color_dict = {"wall": (),
                      "passage": (),
                      "highlight": (),
                      "border": ()
                      }
    return color_dict
