# Enrichment

## Description
A brief description of your project.

## Setup Instructions

### Prerequisites
- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)
- Conda (optional, if using a Conda environment)

### Using Virtualenv

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ArmandOvanessians/Enrichment.git
    cd Enrichment
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On Linux/macOS:
      ```bash
      source venv/bin/activate
      ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

### Using Conda

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ArmandOvanessians/Enrichment.git
    cd Enrichment
    ```

2. **Create a Conda environment**:
    ```bash
    conda create --name targetome
    ```

3. **Activate the Conda environment**:
    ```bash
    conda activate targetome
    ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

1. Ensure your virtual environment or Conda environment is activated.
2. Run the main script:
    ```bash
    python enrichment_gui.py
