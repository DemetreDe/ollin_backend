from flask import Flask, request

import OllinRuntimeMethods

app = Flask(__name__)


@app.route("/")
def test():
    return "Working"

@app.route("/ollin", methods=["POST"])
def runOllin():
    if request.method == "POST":
        image = request.files["image"]

        fileName = OllinRuntimeMethods.API_tools.store(image)
        imageForProcessing = OllinRuntimeMethods.API_tools.pullFromDB(fileName)

        split_image = OllinRuntimeMethods.ollin_object_detection.splitter(imageForProcessing)
        left_obj_list = OllinRuntimeMethods.ollin_object_detection.scanner(split_image, True, False)
        right_obj_list = OllinRuntimeMethods.ollin_object_detection.scanner(split_image, False, True)
        overall_obj_list = OllinRuntimeMethods.ollin_object_detection.scanner(imageForProcessing, False, False)

        left_data = OllinRuntimeMethods.ollin_object_detection.string_builder(left_obj_list, True, False)
        right_data = OllinRuntimeMethods.ollin_object_detection.string_builder(right_obj_list, False, True)

        blocked_flag = OllinRuntimeMethods.ollin_object_detection.path_blocked(left_obj_list,right_obj_list,overall_obj_list)

        if blocked_flag:
            blocked_alert = "detected obstacle in your path"
        else:
            blocked_alert = ""
        return {
                "LeftData": left_data,
                "RightData": right_data,
                "BlockedPath": blocked_alert
                }

if __name__ == '__main__':
    app.run(debug=True)
