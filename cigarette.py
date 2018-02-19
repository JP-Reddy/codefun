import os
# Initial Setup
os.system("initialSetup.bat")
os.system("initialSetup2.bat")

import numpy as np

import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import os

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import cv2
from utils import label_map_util
from utils import visualization_utils as vis_util

INPUT_VIDEO = '../../Github Repo/codefun/nodeapp/video/inputfile.mp4'
TEMP_VIDEO = 'videos/temp.avi'
OUTPUT_VIDEO = 'videos/Final_Output.mp4'
# This is needed to display the images.
# get_ipython().magic('matplotlib inline')
# webcam
# cap=cv.VideoCapture(0)

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# What model to download.
MODEL_NAME = 'mods/faster_rcnn_resnet101_coco_11_06_2017/exported_graph'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('data', 'label_map.pbtxt')

NUM_CLASSES = 1

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

# In[9]:

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# ## Helper code

# In[10]:

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# # Detection

# In[11]:

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)



time_score = []
videoSize = 0
VH = 720
VW = 1280
FPS = 30

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:

    cap=cv2.VideoCapture(INPUT_VIDEO)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    print("FPS: " + str(FPS))
    i = 0
    ret = True

    # Array to store frame number and max % of cigarette


    while ret == True:
    # for image_path in TEST_IMAGE_PATHS:
      # image = Image.open(image_path)
      # ret,image_np=cap.read()
      ret, image_np = cap.read()

      if i == 1:
        VW = image_np.shape[1]
        VH = image_np.shape[0]

      if i % 15 != 0:
        time_score.append(0)
        i+=1
        continue;

      # greyscale
      #image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
      # image_np = load_image_into_numpy_array(image)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)
      # plt.figure(figsize=IMAGE_SIZE)
      # plt.imshow(image_np)
      #out.write(image_np)
      #cv2.imshow("Detect me",cv2.resize(image_np,(800,600)))
      cv2.imwrite("frames/image" + str(i) + ".jpg", image_np)

      s=np.squeeze(scores)

      # If cigarette % > 95% set value to 1

      s = [score for score in np.squeeze(scores) if score>0.95]

      if not s:
        time_score.append(0)
      else:
        time_score.append(1)

      i += 1
      if cv2.waitKey(25) & 0xFF==ord('q'):
        cv2.destroyAllWindows()
        break

    videoSize = i
    cap.release()

# Process time_score to determine where text should be added
addText = {}

for j in range(0, 45):
  addText[j] = 0

i = 45
while videoSize - i >= 50:

  numOnes = time_score[i-45:i+46].count(1)

  if numOnes > 2:
    for j in range(i, i+30):
      addText[j] = 1
  else:
    for j in range(i, i+30):
      addText[j] = 0

  i += 30

for j in range(i, videoSize):
  addText[j] = 0

# Create the output video
cap=cv2.VideoCapture(INPUT_VIDEO)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('videos/output.avi',fourcc, 25.0, (640,480))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(TEMP_VIDEO, fourcc, FPS, (VW,VH))


i = 0
while(cap.isOpened()):

    ret, frame = cap.read()
    if ret==True:
        #print("Entered")
        #cv2.imshow("Detect me",cv2.resize(frame,(800,600)))

        if addText[i] == 1:
            cv2.putText(frame, "SMOKING IS HAZARDOUS TO HEALTH", ( int(frame.shape[1] / 2 - 250), int(frame.shape[0] - 50) ), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255))

        #cv2.imwrite("frames/image" + str(i) + ".jpg", frame)

        out.write(frame)
        i = i+1
        # print(i)
        #cv2.imshow('frame',frame)

    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()

# Extract original audio
os.system("ffmpeg -i " + INPUT_VIDEO + " -vn -acodec copy audio.aac")
# Combine audio and new video
os.system("ffmpeg -i " + TEMP_VIDEO + " -i audio.aac -c copy " + OUTPUT_VIDEO)
# Delete temp file
os.system("del " + TEMP_VIDEO)
