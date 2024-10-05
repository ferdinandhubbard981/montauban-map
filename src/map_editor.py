import cv2


def run_interactive_map():
    img = cv2.imread('../content/new_map.png')  # Replace with your image path
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Coordinates: ({x}, {y})')
        # cv2.imshow('image', img)
