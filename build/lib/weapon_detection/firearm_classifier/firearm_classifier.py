import numpy as np
import tensorflow as tf
import os
import cv2
import csv
import pandas as pd
PATH = 'C:/Users/ASUS/Desktop/stage/weapon_detection_classifers/packaging/'


class FirearmClassifier:

    def __init__(self, weight_file_path=PATH + 'weapon_detection/weapon_detection/firearm_classifier/retrained_graph_long_gun.pb',
                 label_file_path=PATH + 'weapon_detection/weapon_detection/firearm_classifier/retrained_labels_long_gun.txt'):

        # Get training labels
        self.label_lines = [line.rstrip() for line in tf.compat.v1.gfile.GFile(label_file_path)]

        # Import trained inception model
        with tf.compat.v1.gfile.FastGFile(weight_file_path, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.compat.v1.import_graph_def(graph_def, name='')

        self.sess = tf.compat.v1.Session()
        self.softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')

    def download(self):
        pass

    def predict(self, image_path, results_dir=PATH + 'weapon_detection/weapon_detection/firearm_classifier/results'):
        # create the result folder if not exist
        if not (os.path.isdir(results_dir)):
            os.mkdir(results_dir)
        # create the csv file
        base = os.path.basename(image_path)
        file_name = os.path.splitext(base)[0]
        with open(results_dir + '/out_' + file_name + '.csv', 'w', newline='') as file:
            writer = csv.writer(file, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',')
            writer.writerow(["class_firearm_classifier", "probability_firearm_classifier"])

        # Get images from directory and predict object using trained model
        img = cv2.imread(image_path)
        image_data = tf.compat.v1.gfile.FastGFile(image_path, 'rb').read()

        predictions = self.sess.run(self.softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        scores = []
        labels = []
        for node_id in top_k:
            human_string = self.label_lines[node_id]
            score = predictions[0][node_id]
            scores.append(score)
            if human_string == 'rifle':
                labels.append('firearm')
            else:
                labels.append('no_firearm')
            # print('%s (score = %5f)' % (human_string,score))
        class_ID = np.argmax(scores)
        # print("class = {} with prob {}".format(labels[class_ID], scores[class_ID]))
        with open(results_dir + '/out_' + file_name + '.csv', 'a', newline='') as file:
            writer = csv.writer(file, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',')
            writer.writerow([labels[class_ID], scores[class_ID]])
        cv2.putText(img, labels[class_ID], (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (40, 50, 155), 2)
        cv2.imwrite(results_dir + '/out_' + base, img)
        read_file = pd.read_csv(results_dir + '/out_' + file_name + '.csv')
        read_file.to_excel(results_dir + '/out_' + file_name + '.xlsx', index=None, header=True)
        os.remove(results_dir + '/out_' + file_name + '.csv')
        return read_file

    def train(self):
        pass





        




