# import a utility function for loading Roboflow models
from inference import get_roboflow_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2

# define the image url to use for inference
image_file = "photos/fridge-example.png"
image = cv2.imread(image_file)

# load a pre-trained yolov8n model
model = get_roboflow_model(model_id="group_work/2")

# run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
results = model.infer(image)
print(results)

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))

# create supervision annotators
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotate the image with our inference results
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)
print('\n')
best_guess = results[0].predictions[0].class_name
print(best_guess)

# display the image
#sv.plot_image(annotated_image)
