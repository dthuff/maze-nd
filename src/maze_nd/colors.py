def get_color_dictionary(theme: str) -> dict:
    if theme == "christmas":
        color_dict = {"wall": (19, 59, 26),
                      "passage": (80, 145, 82),
                      "highlight": [(24, 24, 184), (36, 211, 255), (255, 61, 18), (48, 235, 19)],
                      "border": (8, 8, 102)
                      }
    elif theme == "beachy":
        color_dict = {"wall": (179, 149, 20),
                      "passage": (252, 243, 220),
                      "highlight": (166, 130, 245),
                      "border": (215, 244, 250)
                      }
    elif theme == "woodsy":
        color_dict = {"wall": (55, 82, 66),
                      "passage": (116, 184, 146),
                      "highlight": (9, 99, 148),
                      "border": (43, 52, 69)
                      }
    elif theme == "kaboom":
        color_dict = {"wall": (40, 40, 40),
                      "passage": (128, 128, 128),
                      "highlight": [(43, 234, 255), (2, 131, 230), (2, 2, 230)],
                      "border": (0, 0, 0)
                      }
    else:
        color_dict = {"wall": (40, 40, 40),
                      "passage": (128, 128, 128),
                      "highlight": (200, 50, 50),
                      "border": (0, 0, 0)
                      }
    return color_dict
