import cv2
import numpy as np
import pygame

from code.modules import constants


def predict_img(model, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converts into the correct colorspace (GRAY)
    img = cv2.resize(img, (160, 180))  # Reduce image size so training can be faster

    pred_img = np.array(img, dtype="uint8")

    return model.predict(np.array([pred_img]))


def use_webcam(left_model, right_model, cam):
    ret, img = cam.read()

    if not ret:
        return None

    # Make array out of cropped webcam
    left_img = np.array(img[0:img.shape[0], img.shape[1] // 2:img.shape[1]], dtype="uint8")
    right_img = np.array(img[0:img.shape[0], 0:img.shape[1] // 2], dtype="uint8")

    # Predict from images
    left_pred = predict_img(left_model, left_img)
    right_pred = predict_img(right_model, right_img)

    # Flip Images To Look natural (not working because of pygame doing weird things...)
    left_img = cv2.flip(left_img, 0)
    right_img = cv2.flip(right_img, 0)

    left_img = np.rot90(left_img)
    right_img = np.rot90(right_img)

    left_img = cv2.cvtColor(left_img, cv2.COLOR_BGR2RGB)
    right_img = cv2.cvtColor(right_img, cv2.COLOR_BGR2RGB)

    return ((pygame.surfarray.make_surface(left_img), pygame.surfarray.make_surface(right_img)),  # Webcam Surface
            (np.argmax(left_pred), np.argmax(right_pred)),  # Prediction index
            (np.max(left_pred), np.max(right_pred)))  # Prediction Confidence


def get_webcam_data(left_model, right_model):
    while not constants.game_stopped:
        hand_images = use_webcam(left_model, right_model, constants.cam)
        if hand_images:
            webcam_left = pygame.transform.scale(hand_images[0][0], (int(hand_images[0][0].get_width() * (constants.height // 6) / hand_images[0][0].get_height()), int(constants.height // 6)))
            webcam_right = pygame.transform.scale(hand_images[0][1], (int(hand_images[0][1].get_width() * (constants.height // 6) / hand_images[0][1].get_height()), int(constants.height // 6)))
            constants.webcam_data = (webcam_left, webcam_right), hand_images[1], hand_images[2]
