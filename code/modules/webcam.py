import os
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

    # # Add text to left img
    # cv2.putText(left_img, constants.left_labels_key[np.argmax(left_pred)], (0, 100), cv2.FONT_HERSHEY_PLAIN,
    #             5, (255, 255, 255), 3)
    # cv2.putText(left_img, str(np.max(left_pred)), (0, 200), cv2.FONT_HERSHEY_PLAIN,
    #             5, (255, 255, 255), 3)
    #
    # # Add text to right img
    # cv2.putText(right_img, constants.right_labels_key[np.argmax(right_pred)], (0, 100), cv2.FONT_HERSHEY_PLAIN,
    #             5, (255, 255, 255), 3)
    # cv2.putText(right_img, str(np.max(right_pred)), (0, 200), cv2.FONT_HERSHEY_PLAIN,
    #             5, (255, 255, 255), 3)

    return ((pygame.surfarray.make_surface(left_img), pygame.surfarray.make_surface(right_img)),  # Webcam Surface
            (str(np.argmax(left_pred)), str(np.argmax(right_pred))),  # Prediction index
            (np.max(left_pred), np.max(right_pred)))  # Prediction Confidence

    # cv2.imshow("Left", left_img)
    # cv2.imshow("Right", right_img)
    # cv2.waitKey(1)


def get_webcam_data(left_model, right_model):
    while not constants.game_stopped:
        hand_images = use_webcam(left_model, right_model, constants.cam)
        if hand_images:
            webcam_left = pygame.transform.scale(hand_images[0][0], (int(hand_images[0][0].get_width() * (constants.height // 6) / hand_images[0][0].get_height()), int(constants.height // 6)))
            webcam_right = pygame.transform.scale(hand_images[0][1], (int(hand_images[0][1].get_width() * (constants.height // 6) / hand_images[0][1].get_height()), int(constants.height // 6)))
            constants.webcam_data = (webcam_left, webcam_right), hand_images[1], hand_images[2]


def get_training_data(foldername, length, label, delay=100):
    os.mkdir(f"RawData/{foldername}")

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Record")

    delay_counter = 0
    while delay_counter < 500:
        ret, frame = cam.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converts into the corret colorspace (GRAY)
        frame = frame[0:frame.shape[0], frame.shape[1] // 2:frame.shape[1]]
        frame = cv2.resize(frame, (160, 180))

        cv2.putText(frame, f"{500 - delay_counter} ticks left", (0, 20), cv2.FONT_HERSHEY_PLAIN,
                    1.5, (255, 255, 255), 3)

        cv2.imshow("Record", frame)
        cv2.waitKey(1)
        delay_counter += 1

    frame_counter = 0
    while frame_counter < length:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        img_name = f"RawData/{foldername}/{frame_counter}_{label}.png"

        frame = frame[0:frame.shape[0], frame.shape[1] // 2:frame.shape[1]]
        frame = cv2.resize(frame, (160, 180))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converts into the correct colorspace (GRAY)

        cv2.imwrite(img_name, frame)

        cv2.putText(frame, f"Frame {frame_counter + 1}", (0, 20), cv2.FONT_HERSHEY_PLAIN,
                    1.5, (255, 255, 255), 3)

        cv2.imshow("Record", frame)
        cv2.waitKey(delay)

        print(f"Frame {frame_counter} written!")
        frame_counter += 1

    cam.release()

    cv2.destroyAllWindows()


# get_training_data("Left/open_n_4", 250, "2")
