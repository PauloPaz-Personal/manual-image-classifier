import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import sys
import os
import csv

CLASSIFICATIONS = [	
    '1',	
    '2',	
    '3',	
    '4',	
    '5',	
    '6',	
    '7',	
    '8',	
    '9',	
    '10',	
    '11',	
]	

# read dataset from csv file
try:
    with open('classifications.csv', 'r') as f:
        reader = csv.reader(f)
        dataset = list(reader)
        # remove empty rows
        dataset = [row for row in dataset if row]
except FileNotFoundError:
    print('Classifications file not found. Creating new file.')
    dataset = [['Image', 'Class']]
    with open('classifications.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(dataset)

# check if images folder exists	
if not os.path.exists('images'):	
    os.makedirs('images')	
    print('Created images folder, please add images to it.')	
    sys.exit()	
    
# get all images in the images folder
images = [f for f in os.listdir('images')]
# check if list if images is empty
if len(images) == 0:
    print('No images found in images folder. Please add images to the folder.')
    sys.exit()


class GUI(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # set up the GUI
        self.setGeometry(100, 100, 800, 600)

        # set central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # set up the layout
        self.layout: QtWidgets.QGridLayout = QtWidgets.QGridLayout(
            self.central_widget)

        # add image label
        self.image_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.image_label, 0, 0, 1,
                              2, QtCore.Qt.AlignmentFlag.AlignCenter)
        # set max width of image label to fit the window
        self.image_label.setMaximumWidth(self.width() - 100)
        self.image_label.setMaximumHeight(self.height() - 100)

        # add classification layout
        self.classification_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.classification_layout, 1, 0, 1, 2)

        # add buttons to classification layout
        self.classification_buttons = []
        for i, classification in enumerate(CLASSIFICATIONS):
            button = QtWidgets.QPushButton(classification, self)
            button.clicked.connect(self.classification_clicked)
            self.classification_buttons.append(button)
            self.classification_layout.addWidget(button)
            # if i is in range 0-8, add bind to keyboard
            if i in range(9):
                button.setShortcut(QtGui.QKeySequence(str(i+1)))
            elif i == 9:
                button.setShortcut(QtGui.QKeySequence('0'))

        # add arrows to move through the images
        self.left_arrow = QtWidgets.QPushButton('<')
        self.left_arrow.clicked.connect(self.left_arrow_clicked)
        # bind left arrow to left key
        self.left_arrow.setShortcut('Left')
        self.right_arrow = QtWidgets.QPushButton('>')
        self.right_arrow.clicked.connect(self.right_arrow_clicked)
        # bind right arrow to right key
        self.right_arrow.setShortcut('Right')

        self.layout.addWidget(self.left_arrow, 2, 0)
        self.layout.addWidget(self.right_arrow, 2, 1)

        # if all images are classified, mark this variable as true
        self.classified = False

        # find index of first unclassified image
        for image in images:
            for data in dataset:
                if data[0] == image:
                    break
            else:
                self.image_index = images.index(image)
                break
        else:
            self.image_index = 0
            # show message box
            QtWidgets.QMessageBox.information(self, 'All images classified',
                                              'All images are already classified.')
            self.classified = True

        self.update_image()

    def left_arrow_clicked(self):
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(images) - 1
        self.update_image()

    def right_arrow_clicked(self):
        self.update_image()
        if self.image_index >= len(images):
            self.image_index = 0
            # show message box when all images are classified
            if not self.classified:
                QtWidgets.QMessageBox.information(self, 'All images classified',
                                                  'All images have been classified.')
                self.classified = True
        self.image_index += 1
        
    def update_image(self):
        self.image_label.setPixmap(QtGui.QPixmap(
            'images/' + images[self.image_index]))
        self.image_label.setScaledContents(True)
        self.image_label.show()

        # get image name
        name = images[self.image_index]
        # show image name
        self.setWindowTitle(f'{name} - {self.image_index+1}/{len(images)}')

        # reset buttons style
        for button in self.classification_buttons:
            button.setStyleSheet('')

        # check if image is already in the dataset
        for data in dataset:
            if data[0] == name:
                # set classification button style
                self.classification_buttons[CLASSIFICATIONS.index(
                    data[1])].setStyleSheet('font-weight: bold;')
                break

    def classification_clicked(self):
        # get classification
        classification = self.sender().text()
        # get image name
        name = images[self.image_index]
        # check if image is already in the dataset
        for data in dataset:
            if data[0] == name:
                # update classification
                data[1] = classification
                break
        else:
            # add image and classification to dataset
            dataset.append([name, classification])
        # write dataset to csv file
        with open('classifications.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(dataset)
        # update image
        self.right_arrow_clicked()


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
