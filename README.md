# Nutri-Cart-Scanner
# Project Title: Nutri Cart - Your Smart Shopping Assistant

Team: Matrix 10
Team Lead: Bikram Kumar Reddy

---

# 1. Problem Statement

Modern consumers, especially those with health conditions, allergies, or specific dietary goals, face a significant challenge in the grocery store. It is time-consuming and often difficult to manually check every product for unsuitable ingredients, track nutritional information, and manage a budget. This can lead to unsafe food choices, abandoned health goals, and a frustrating shopping experience.

---

# 2. Our Solution: Nutri Cart

**Nutri Cart** is a real-time, Python-based smart shopping assistant that transforms a standard webcam into a powerful tool for making informed, healthy, and budget-conscious decisions.

By simply scanning a product's barcode, users get an instant, personalized dashboard of all the information they need, directly in their console. Our application, set in a virtual store called **"FreshMart"**, goes beyond simple scanning to provide a comprehensive and interactive shopping experience.

---

## 3. Key Features

 **Personalized Allergen Alerts:** Before shopping, the user inputs their specific allergies (e.g., "peanuts", "chia seeds"). Nutri Cart intelligently scans both the official allergen list and the **full ingredient list** of every product, providing an immediate and clear **"Safe for you"** or **"WARNING"** message.

 **Live Cart Value Tracking:** As items are scanned and approved, they are added to a virtual shopping cart. The application maintains and displays a live running total of the cart value, factoring in special **FreshMart discounts** to help users stay on budget.

 **Auto-Checkout for Budget Control:** To help users save money and stick to a plan, the app asks for a **maximum item limit** at the start. Once the cart reaches this limit, the session automatically ends and presents the final bill, preventing impulse purchases.

 **Real-time Nutrition Information:** For food items, the application instantly displays key nutritional data, such as **calories and protein content**, allowing health-conscious shoppers to track their intake    right from the aisle.

---

# 4. How to Run the Project

**Prerequisites:**
* Anaconda (or Miniconda) installed.
* A webcam connected to the computer.

**Setup Instructions:**

1.  **Create and activate a new conda environment.** This ensures all dependencies are clean.
    ```bash
    conda create --name nutricart-env python=3.10
    conda activate nutricart-env
    ```

2.  **Install the required libraries.** We use `pip` within the conda environment to get the `pyzbar-x` package, which is essential for Windows compatibility.
    ```bash
    pip install opencv-python pyzbar-x
    ```

3.  **Run the application.** Navigate to the project folder in your terminal and run the main script:
    ```bash
    python nutri.py
    ```
---

# 5. Technology Stack

* **Language:** Python
* **Core Libraries:**
    * **OpenCV (`cv2`):** For capturing the live video feed from the webcam and displaying the user interface.
    * **pyzbar-x:** A robust and reliable library for accurately detecting and decoding barcodes from video frames, with crucial fixes for Windows environments.
    * **os & time:** Standard libraries for clearing the console to create a dynamic display and managing scan cooldowns.
