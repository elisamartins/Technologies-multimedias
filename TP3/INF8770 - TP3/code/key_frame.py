import numpy as np
import cv2
import math
import csv
from matplotlib import pyplot as plt 
from histograms import get_edge_histogram, get_euclidean_distance

THRESHOLD = 10000
VIDEO_FPS = 29.97
SEUIL = 7000

class Frame:
  def __init__(self, time, hist):
      self.time = time
      self.hist = hist

class KeyFrameGroup:
    def __init__(self, center_mass, frames):
      self.center_mass = center_mass
      self.frames = frames

def update_groups(frame, groups):

    # Si groups est vide, on ajoute directement un groupe
    if (len(groups) == 0):
      groups.append(KeyFrameGroup(frame.hist, [frame]))
      return groups

    for i in range(len(groups)):
            dist = get_euclidean_distance(frame.hist, groups[i].center_mass)
            #print(dist)
            if(dist < THRESHOLD):

                # Update centre de masse
                groups[i].center_mass = np.multiply(groups[i].center_mass, 0.75) + np.multiply(frame.hist, 0.25)
                # Ajout du frame dans le groupe 
                groups[i].frames.append(frame)
                return groups
            
    # Sinon on créé un nouveau groupe
    groups.append(KeyFrameGroup(frame.hist, [frame]))
    return groups
  
def get_closest_frame_to_centre_masse(group):
  closest_frame = group.frames[0]
  smallest_dist = get_euclidean_distance(closest_frame.hist, group.center_mass)
  for i in range(1, len(group.frames)):
    dist = get_euclidean_distance(group.frames[i].hist, group.center_mass)
    if dist < smallest_dist:
      smallest_dist = dist
      closest_frame = group.frames[i]
  
  return closest_frame

def get_key_frames(video_number):
    cap = cv2.VideoCapture('../data/video/v' + str(video_number).zfill(2) + '.mp4')
    groups = []

    frame_number = 0
    while (cap.isOpened()):
      ret, frame = cap.read()
      
      if ret == True:
        #h = get_color_histogram(frame)
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h = get_edge_histogram(frame)
        frame_number += 1
        groups = update_groups(Frame(frame_number/VIDEO_FPS, h), groups)

      else:
          break

    print("Number of groups " + str(len(groups)))
    cap.release()

    # Pour chaque groupe, on garde l'histogramme du frame le plus proche du centre de masse
    results = []
    for group in groups:
      results.append(get_closest_frame_to_centre_masse(group))

    return results

def generate_indexation_file(video_number):
  f = open('../data/q3_edge_histograms.csv', 'a', newline='')
  f_writer = csv.writer(f)
  
  key_frames = get_key_frames(video_number)
  for frame in key_frames:
    f_writer.writerow([video_number, frame.time, list(frame.hist)])

def generate_indexation_files():
  f = open('../data/q3_edge_histograms.csv', 'w', newline='')
  f_writer = csv.writer(f)
  f_writer.writerow(["video number", "time in s", "histogram"])
  f.close()
  for i in range(1, 51):
    print(i)
    generate_indexation_file(i)

def get_video(image):
  #img_hist = get_color_histogram(image)
  img_hist = get_edge_histogram(image)

  smallest_dist = SEUIL
  video_number = "out"
  time = ""
  f = open('../data/q3_edge_histograms.csv', 'r')
  f_reader = csv.reader(f, delimiter=',')
  f.readline()
  for row in f_reader:
    current_dist = get_euclidean_distance(eval(row[2]), img_hist)
    if current_dist < smallest_dist:
       smallest_dist = current_dist
       video_number = "v" + str(row[0]).zfill(2)
       time = row[1]
  
  return video_number, time, smallest_dist

def get_solution(ext):
  f_writer = csv.writer(open('../data/q3_solution_' + ext + '.csv', 'w', newline=''))
  f_writer.writerow(["image", "video", "minutage"])
  f_writer = csv.writer(open('../data/q3_solution_' + ext + '.csv', 'a', newline=''))
  for i in range(1, 201):
    result = get_video(cv2.imread('../data/' + ext + '/i' + str(i).zfill(3) + '.' + ext, cv2.IMREAD_GRAYSCALE))
    f_writer.writerow(["i"+ str(i).zfill(3), result[0], result[1], result[2]])

#generate_indexation_files()
#get_solution()
# image_name = '../../data/png/i010.png'

# image_rgb = cv2.imread(image_name)

# image_gray = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)
# color_hist = get_color_histogram(image_rgb)
# edge_hist = get_edge_histogram(image_gray)
# print("Color histogram:")
# print(color_hist)
# print(len(color_hist))
# print("Edge histogram:")
# print(edge_hist[1])
# print(len(edge_hist[1]))