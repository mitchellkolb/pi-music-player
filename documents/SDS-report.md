



# Software Design Document

## Project Title: *Raspberry Pi Music Player*  
**Author(s):** *Mitchell Kolb*  
**Date:** *September 2023 - December 2024*  

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Requirements](#2-requirements)
3. [System Design](#3-system-design)
4. [Implementation Details](#4-implementation-details)
5. [Testing Plan](#5-testing-plan)
6. [Deployment Plan](#6-deployment-plan)
7. [Future Work](#7-future-work)
8. [Glossary and References](#8-glossary-and-references)

---

## 1. Introduction

### 1.1 Project Overview
Provide a brief summary of the problem and the solution.  
*This project automates music playback through a Raspberry Pi touchscreen interface, simplifying background music management in a quiet environment.*

### 1.2 Objectives
List the goals of the project.  
- Ensure ease of use for users with minimal technical knowledge.  
- Maintain consistent playback reliability in kiosk mode.

### 1.3 Stakeholder Overview
Identify and describe the client and their expectations.  
*The client expects a simple setup and a system that can run unattended for extended periods.*

---

## 2. Requirements

### 2.1 Functional Requirements
- Users can play, pause, and skip tracks via the touchscreen interface.  
- Volume adjustment functionality is accessible through the UI.  
- The system should support basic music player controls like shuffle or repeat.  

### 2.2 Non-Functional Requirements
- System should reboot automatically in case of a crash.  
- Minimal latency for touchscreen inputs (response time < 100ms).  
- Compatibility with Raspberry Pi hardware and software ecosystem.  

### 2.3 Use Cases
- **Scenario 1:** User touches "Play" to start music playback.  
- **Scenario 2:** User skips a track using the "Next" button on the touchscreen.  

---

## 3. System Design

### 3.1 High-Level Architecture
Describe the overarching architecture of the system. Add UML diagrams here when needed.
*The system is divided into three main components: UI Layer, Automation Layer, and System Layer.*  
Provide a diagram illustrating the relationships (e.g., PyQt, Playwright, Raspberry Pi hardware)
- **Use Case Diagram**: [Include Diagram Here]
- **Component Diagram**: [Include Diagram Here]
.

### 3.2 Component Descriptions
- **UI Layer (PyQt):** Manages user interactions and sends commands to the Automation Layer.  
- **Automation Layer (Playwright):** Simulates user actions on the music website.  
- **System Layer:** Handles Raspberry Pi hardware configurations, including kiosk mode.  
- **Class Diagram**: [Include Diagram Here]
- **Sequence Diagram**: [Include Diagram Here]

### 3.3 Data Flow Diagram
Illustrate how data moves through the system, such as input events triggering actions.

---

## 4. Implementation Details

### 4.1 Class and Module Structure
- Detail the primary classes/modules and their responsibilities.  
*A `MusicPlayerUI` class handles button interactions.*  
- **Class Diagram (Expanded)**: [Include Diagram Here]

### 4.2 Integration Plan
- Explain how PyQt and Playwright interact.  
- Highlight error-handling measures for website disconnections.  
- **Sequence Diagram (Detailed)**: [Include Diagram Here]

### 4.3 Security Considerations
- Prevent unauthorized access to the kiosk.  
- Ensure system settings are locked to avoid tampering.

---

## 5. Testing Plan

### 5.1 Functional Testing
- Verify that each button on the touchscreen performs its expected function.

### 5.2 Non-Functional Testing
- Measure the responsiveness of the touchscreen inputs.  
- Test system stability under prolonged use in kiosk mode.

### 5.3 Edge Cases
- Handle scenarios where the music website is temporarily unavailable.

---

## 6. Deployment Plan

### 6.1 Installation Instructions
- Provide step-by-step guidance for setting up the software on the Raspberry Pi.  
- Include instructions for installing dependencies like PyQt and Playwright.

### 6.2 Kiosk Mode Configuration
- Detail how to set up the Raspberry Pi to run in kiosk mode, including any required scripts.

---

## 7. Future Work
- Add features like remote management or customizable playlists.  
- Explore options for integrating analytics to monitor playback usage.

---

## 8. Glossary and References

### 8.1 Glossary
- **PyQt:** A Python library for creating GUIs.  
- **Playwright:** A library for automating web interactions.  

### 8.2 References
- Link to documentation or tutorials for Playwright and PyQt.  
- Include any other resources consulted during development.
