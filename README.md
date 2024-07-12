# Custom Search Engine

This project is a custom search engine capable of searching both images and text within personal data. It also performs hybrid searches that combine image and text queries. Users can upload their image and text data into the database. The data is stored in OpenSearch as vector data, and we use the CLIP model for embedding both image and text data. OpenSearch and the CLIP model embeddings are used for searching.

## Features

- **Text Search**: Search text data using CLIP model embeddings.
- **Image Search**: Search image data using CLIP model embeddings.
- **Hybrid Search**: Combine image and text queries for more comprehensive search results.

## Technologies Used

- **OpenSearch**: For storing and searching vector data.
- **CLIP Model**: For embedding both image and text data.
- **Docker**: containerized applications.



## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
