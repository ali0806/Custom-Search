import os
import gradio as gr
from PIL import Image
from embedding_generation import get_image_embedding, get_text_embedding
from search import get_random_imageVectors_with_IDs, search_knn
from hybrid_search.hybrid_search_unsplash import hybrid_search_main

index_name = 'unsplash_knn_bulk_img_index_02'
image_dir ="../../../dataset/unsplash/unsplash_25k"

# Function to get image by its ID
def get_image_by_image_id(image_id, image_dir):
    # Construct the file path
    file_path = os.path.join(image_dir, f"{image_id}.jpg")
    # Open the image file
    image = Image.open(file_path)
    return image

def text_to_image_search(text_query, num_images):
    vector = get_text_embedding(text_query)
    response = search_knn(vector, index_name, num_images)
    image_ids = [hit['_source']['image_id'] for hit in response['hits']['hits']]

    images = []
    for i in range(len(image_ids)):
        images.append((get_image_by_image_id(image_ids[i], image_dir)))
    print(len(images))
    return images

def upload_image_to_image_search(query_image, num_images):
    image = Image.open(query_image)
    vector = get_image_embedding(query_image)
    response = search_knn(vector, index_name, num_images)
    image_ids = [hit['_source']['image_id'] for hit in response['hits']['hits']]
    
    images = []
    for i in range(len(image_ids)):
        images.append((get_image_by_image_id(image_ids[i], image_dir)))
    return image, images


def random_image_to_image_search(num_images):
    # Fetch random images and their IDs from OpenSearch
    image_id, vector =  get_random_imageVectors_with_IDs(index_name)
    input_image = get_image_by_image_id(image_id, image_dir)
    response = search_knn(vector, index_name, num_images)
    image_ids = [hit['_source']['image_id'] for hit in response['hits']['hits']]
    images = []
    for i in range(len(image_ids)):
        images.append((get_image_by_image_id(image_ids[i], image_dir)))
    return input_image, images

with gr.Blocks() as demo:

    with gr.Column():
        with gr.Row():
            textbox = gr.Textbox(label="Text Query For Hybrid Search")
            btn4 = gr.Button("Search", scale=0)
        
        with gr.Row():
            # Add input fields for vector and keyword search boost levels
            vector_boost = gr.Number(label="Vector Search Boost Level")
            bm25_boost = gr.Number(label="Keyword Search Boost Level")
        
        gallery4 = gr.Gallery(label="Similar images",
                             show_label=False,
                             elem_id="gallery",
                             columns=[6],
                             object_fit="cover",
                             height="1000px"
                             )

        
        # Include the new input fields in the button click function
        btn4.click(fn=hybrid_search_main,
                  inputs=[textbox, vector_boost, bm25_boost],
                  outputs=gallery4)
        
    with gr.Column():
        with gr.Row():
            textbox = gr.Textbox(label="Text Query for Multimodal Search")
            btn = gr.Button("Search", scale=0)

        image_number = gr.Number(label="Number of images to retrieve")

        gallery = gr.Gallery(label="Similar images",
                             show_label=False,
                             elem_id="gallery",
                             columns=[6],
                             object_fit="cover",
                             height="1000px"
                             )
        # Include the new input fields in the button click function
        btn.click(fn=text_to_image_search,
                  inputs=[textbox, image_number],
                  outputs=gallery)
        
    with gr.Column():
        with gr.Row():
            inp = gr.File(label="Multimodal Search for Uploaded Image")
            btn2 = gr.Button("Search", scale=0)

        image_number2 = gr.Number(label="Number of Images to Retrieve")
        image = gr.Image(height="300px", width="300px")
        gallery2 = gr.Gallery(label="Similar images",
                             show_label=False,
                             elem_id="gallery",
                             columns=[6],
                             object_fit="cover",
                             height="1000px"
                             )
        # Include the new input fields in the button click function
        btn2.click(fn=upload_image_to_image_search,
                  inputs=[inp, image_number2],
                  outputs=[image, gallery2])

    with gr.Column():

        with gr.Row():
            image_number3 = gr.Number(label="Number of Images to Retrieve")
            btn3 = gr.Button("Search", scale=0)

        image = gr.Image(height="300px", width="300px")
        gallery3 = gr.Gallery(label="Similar images",
                             show_label=False,
                             elem_id="gallery",
                             columns=[6],
                             object_fit="cover",
                             height="1000px"
                             )
        
        btn3.click(fn=random_image_to_image_search,
                   inputs = [image_number3],
                   outputs=[image, gallery3])
demo.launch()