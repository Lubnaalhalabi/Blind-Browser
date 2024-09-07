from PIL import Image    
import numpy as np
import matplotlib.pyplot as plt
from sam2.build_sam import build_sam2
import os
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator

class Sam2:
    def __init__(self, image_path):
        """
        Initialize the Sam2 class with the path to the image to be processed.
        
        Parameters:
        image_path (str): The file path of the image to be processed.
        """
        self.image_path = image_path
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'results')

    
    def show_anns(self,anns, borders=True):
        """
        Display the segmented annotations on the image.

        Parameters:
        anns (list): A list of annotations where each annotation is a dictionary with 'segmentation' and 'area'.
        borders (bool): Whether to draw borders around the segmented areas.
        """
        if len(anns) == 0:
            return
        
        # Sort annotations by area in descending order
        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
        ax = plt.gca()
        ax.set_autoscale_on(False)

        # Create an empty image with an alpha channel for displaying segmentation
        img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
        img[:,:,3] = 0
        for ann in sorted_anns:
            m = ann['segmentation']
            color_mask = np.concatenate([np.random.random(3), [0.5]])
            img[m] = color_mask 
            if borders:
                import cv2
                # Find contours in the segmentation mask
                contours, _ = cv2.findContours(m.astype(np.uint8),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
                # Smooth contours
                contours = [cv2.approxPolyDP(contour, epsilon=0.01, closed=True) for contour in contours]
                # Draw contours on the image                
                cv2.drawContours(img, contours, -1, (0,0,1,0.4), thickness=1) 

        # Display the image with annotations
        ax.imshow(img)

    def segment(self): 
        """
        Perform image segmentation using the SAM2 model and save the results.
        """
        # Load and prepare the image for segmentation
        image = Image.open(self.image_path)
        image = np.array(image.convert("RGB"))

        # Define paths for model checkpoint and configuration
        sam2_checkpoint = "sam2_hiera_large.pt"
        model_cfg = "sam2_hiera_l.yaml"

        # Build and initialize the SAM2 model
        sam2 = build_sam2(model_cfg, sam2_checkpoint, device ='cpu', apply_postprocessing=False)

        # Create a mask generator for the SAM2 model
        mask_generator = SAM2AutomaticMaskGenerator(sam2)
        
        # Generate segmentation masks     
        masks = mask_generator.generate(image)
        
        # Define the path to save the segmented image
        saving_segmented_image_path = os.path.join(self.base_path, "sam_segmented_image.png")

        # Display the original image with segmentation overlays        
        plt.figure(figsize=(20,30))
        plt.imshow(image)
        self.show_anns(masks)
        plt.axis('off')
        
        # Save the segmented image
        plt.savefig(saving_segmented_image_path)
        plt.close()

