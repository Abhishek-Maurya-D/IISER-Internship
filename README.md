# Quantum Network Simulation Internship Project

This repository contains the work completed during an internship at IISER, focusing on simulating quantum communication protocols and building a web-based interface for visualization and interaction.

## Project Structure

- **backend/**  
  Python scripts for simulating quantum key distribution (QKD) protocols:
  - `COW_netsquid.py`: Simulates the Coherent One-Way (COW) QKD protocol using NetSquid.
  - `DPS_netsquid.py`: Simulates the Differential Phase Shift (DPS) QKD protocol using NetSquid.
  - `QuNetSim.py`: Example quantum communication using the QuNetSim framework.
  - `server.py`: Flask backend API to run protocol simulations and serve results to the frontend.

- **frontend/week 1/**  
  Web interface for interacting with the backend and visualizing results:
  - `index.html`: Main web page.
  - `script.ts`: TypeScript for frontend logic and user interaction.
  - `styles.css`: Styling for the web interface.

- **docs/**  
  - `QuNetSim Theory.docx`: Theoretical background and documentation.

## Technologies Used

- **Python** (NetSquid, Flask, QuNetSim)
- **HTML/CSS/TypeScript** (Frontend UI)
- **Flask-CORS** (for backend/frontend communication)

## Setup & Usage

### Backend

1. Install Python dependencies:
   ```sh
   pip install flask flask-cors netsquid qunetsim matplotlib
   ```
2. Run the backend server:
   ```sh
   python backend/server.py
   ```

### Frontend

Open `frontend/week 1/index.html` in your browser.  
(For full functionality, ensure the backend server is running.)

## Features

- Simulate COW and DPS QKD protocols.
- Visualize quantum communication timelines.
- Interactive web interface for protocol selection and result display.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Acknowledgments

Thanks to IISER mentors and the open-source quantum simulation community.
