# Save the Crops Frontend

Welcome to the **Save the Crops** frontend repository. This project is part of our Data Science & Machine Learning Bootcamp final project, developed collaboratively by our team. The frontend application serves as the user interface for our backend machine learning API, designed to diagnose plant diseases and provide insights to help farmers protect their crops.

## Project Overview

  - **End Project**: Completed as part of the Machine Learning & Data Science bootcamp at Le Wagon, 2024 Q1.
  - **Built CNN model achieving 95%+ accuracy on 20,000+ plant disease images.**
  - **Implemented model deployment pipeline using FastAPI and Docker.**
  - **Stack**: TensorFlow, OpenCV, FastAPI, Docker.
  - **Features**: Real-time inference, model versioning, automated testing.
  - **Impact**: Potential 30% reduction in crop loss through early disease detection.

The **Save the Crops** project aims to assist farmers by providing an easy-to-use tool for diagnosing plant diseases using images of their crops. Users can upload images of plants, and the system will analyze the image to detect any diseases and provide recommendations.

This repository contains the frontend codebase, built with [Streamlit](https://streamlit.io/), which interacts with our backend API.

The backend project can be found here: [Save the Crops Backend](https://github.com/MahautHDL/save_the_crops). The backend is responsible for processing images, running them through a machine learning model, and returning the results to the frontend.

As part of this project, we also set up a virtual machine to run **MLflow** for tracking experiments and managing the machine learning lifecycle.

### Project Demonstration

- **PowerPoint Presentation**: [Save the Crops Presentation](https://docs.google.com/presentation/d/1TsgPMUv2OTvvGLQhH7S9eT69ftjWV3CQ/edit#slide=id.p1)
- **YouTube Demonstration**: [Save the Crops Demo Video](https://www.youtube.com/watch?v=KWvrcZ72Myw)

## Features

- **User Interface**: Simple and intuitive interface built with Streamlit.
- **Image Upload**: Users can upload images of their crops.
- **Disease Detection**: The frontend sends the image to the backend API, which returns the disease diagnosis.
- **Results Display**: The diagnosis is displayed to the user, with any relevant information.

## Installation

To run the frontend application locally, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/save_the_crops_frontend.git
   cd save_the_crops_frontend
   ```

2. **Install Requirements**

   It's recommended to use a virtual environment.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configure the Application**

   Create a `secrets.toml` file in the `.streamlit` directory to store your API keys and configurations. You can use `.streamlit/secrets.toml.sample` as a template.

   ```toml
   # .streamlit/secrets.toml
   API_URL = "https://your-backend-api-url.com/predict"
   API_OPENAI = "your-openai-api-key"
   ```

4. **Run the Application**

   ```bash
   streamlit run app.py
   ```

## Usage

- Open the application in your browser.
- Select the type of plant from the options provided (Cashew, Cassava, Maize, Tomato).
- Upload an image of the plant.
- The application will display the diagnosis and any relevant information.

## Project Structure

- `app.py`: Main Streamlit application.
- `requirements.txt`: List of dependencies.
- `.streamlit/`: Streamlit configuration files.
  - `config.toml`: Visual theming for the application.
  - `secrets.toml.sample`: Sample secrets file for configuration.
- `media/`: Directory containing media assets like images.
- `Makefile`: Includes commands for installation and running the application.

## Dependencies

Major dependencies include:

- `streamlit`
- `pandas`
- `requests`
- `openai`
- `streamlit_chat`
- `requests_toolbelt`

See `requirements.txt` for the full list.

## Backend Repository

For more details on the backend API, including the machine learning models and API endpoints, please refer to the [Save the Crops Backend Repository](https://github.com/MahautHDL/save_the_crops).

## MLflow Integration

As part of this project, we set up a virtual machine to run **MLflow** for experiment tracking and model management. This allowed us to monitor our model performance and maintain version control over our machine learning models.

## Acknowledgements

This project was developed as part of the Data Science & Machine Learning Bootcamp. We collaborated as a team to design and implement both the frontend and backend components.

Special thanks to all team members for their contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or questions, => [click here to get in touch with me](https://www.linkedin.com/in/victordecoster/).
