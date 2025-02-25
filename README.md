# Room Acoustics Simulation Models Implementation in Python

## Overview
This repository contains a **room acoustics simulation tool** that models **sound propagation and reflections** using the **image source method**. The tool calculates **impulse responses, RT60 reverberation time, and energy decay curves** for different room configurations.

## Features
- Implements the **image source method** to simulate room acoustics.
- Models impulse responses for **low, mid, and high frequencies**.
- Supports multiple room types with varying **acoustical treatments**.
- Computes **RT60 values** to evaluate reverberation time.
- Generates **energy decay curves** to analyze sound dissipation.
- Visualizes results using **matplotlib**.

## Directory Structure
```
.idea/
docs/
results/
src/
    ├── data/
    ├── main.py
    ├── acoustics.py
tests/
```

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `json`
  - `mpl_toolkits`
  - `scipy.signal`

## Setup Instructions
### 1. Clone the Repository
```sh
git clone [repository_link]
cd [repository_folder]
```
### 2. Install Dependencies
```sh
pip install numpy matplotlib scipy
```
### 3. Run the Simulation
```sh
python src/main.py
```

## Datasets (JSON)
The simulation uses **room configuration files** in the `data/` directory. These files define **room dimensions, sound source & receiver positions, and absorption coefficients**.

## Room Configurations
| Room Type            | Dimensions (L × W × H) | Example Spaces      | Acoustic Characteristics |
|----------------------|---------------------------|---------------------|--------------------------|
| **Furnished Room**   | 6 × 6 × 3                 | Bedroom, Office     | High absorption due to furniture. |
| **Empty Room**       | 6 × 6 × 3                 | Classroom, Hallway  | Low absorption, significant reflections. |
| **Treated Big Room** | 12 × 10 × 5               | Music Studio, Theater | Controlled acoustics with soundproofing. |
| **Untreated Big Room** | 12 × 10 × 5             | Gymnasium, Large Hall | Minimal absorption, strong reflections. |

## Results & Analysis
The simulation provides:
- **Impulse Response Analysis** (Peak Amplitude & Decay Time)
- **RT60 Reverberation Time Comparison**
- **Energy Decay Curve Analysis**

For detailed analysis, see the **report in the `docs/` folder**.

## Contributors
- [Your Name]
- [Your Email]

## License
This project is licensed under the **MIT License**. See `LICENSE` for details.

## Contact
For questions or contributions, reach out via email: [Your Email]

