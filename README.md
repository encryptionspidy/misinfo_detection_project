
## Overview

Our Misinformation Detection System is designed to identify and flag misleading information in real-time. By leveraging continuous data ingestion and active AI training, we ensure accurate and up-to-date detection capabilities.

## Features

- **Real-Time Data Ingestion**: Continuously fetches live data from various sources, ensuring the system analyzes the most current information.
- **Active AI Training**: Regularly updates the AI model with new data, enhancing its ability to detect misinformation accurately.
- **Comprehensive Flagging System**: Categorizes content into specific labels for precise identification.

## Flagging Categories

- **"hoax"**: Detected misinformation or dubious claims.
- **"truth"**: Verified accurate information.
- **"opinion"**: Subjective statements without factual basis.
- **"uncertain"**: Insufficient evidence to classify.
- **"verified"**: Strongly supported by credible sources.
- **"fake"**: Identified deliberate falsehoods.
- **"satire"**: Content intended for humor or parody but often mistaken for misinformation.
- **"biased"**: Information that may contain factual elements but is presented with a strong bias.
- **"misleading"**: Information that is partially true but framed to create a false impression.
- **"spam"**: Unsolicited or irrelevant information, which may dilute factual analysis.
- **"incomplete"**: Statements that lack enough context to draw an accurate conclusion.

Note: Due to hardware and resource limitations, training large datasets and models may not be feasible .
## System Architecture

```mermaid
%%{init: {'theme': 'neutral'}}%%
flowchart TD
    %% === Data Ingestion === %%
    subgraph "1️⃣ Data Universe"
        A1[Live Social Feeds] -->|Ingest| A2[Stream Ingestion]
        A3[News APIs] -->|Ingest| A2
        A4[Broadcast Feeds] -->|Ingest| A2
        A5[User Reports] -->|Ingest| A2
        A2 --> A6[Kafka Stream Processor]
    end

    %% === Real-Time Preprocessing === %%
    subgraph "2️⃣ Real-Time Preprocessing"
        B1[Multi-Modal Analyzer] --> B2[Video Frame Sampling]
        B1 --> B3[Image OCR]
        B1 --> B4[Text Normalization]
        B2 & B3 & B4 --> B5[Contextual Enrichment]
        B5 --> B6[Graph Neural Network]
    end

    %% === AI Core Processing === %%
    subgraph "3️⃣ AI Core"
        C1[Hybrid Detector] --> C2[Propagation Pattern Analysis]
        C2 --> C3[Anomaly Detection] --> C4[Trained Model]
        C1 --> C5[Knowledge Graph Verification]
        C1 --> C6[Cross-Modal Consistency Check]
        C1 --> C7[LLM Semantic Analysis]
    end

    %% === Misinformation Detection Modules === %%
    subgraph "4️⃣ Misinformation Detection"
        subgraph "4A. Factual Verification"
            D1[Fact Extraction] --> D2[Cross-Check Trusted Sources]
            D1 --> D3[Match with Knowledge Base]
            D2 --> D4[Real-Time Fact Update]
            D3 --> D4
            D4 --> D5[Factual Consistency Analyzer]
            D5 --> D6[Updated Factual Model]
        end

        subgraph "4B. Malicious URL Detection"
            E1[URL Extractor] --> E2[Phishing Heuristic Analysis]
            E1 --> E3[Blacklist Check]
            E2 --> E4[Malicious URL Classifier]
            E3 --> E4
            E4 --> E5[Threat Intelligence Database]
            E5 --> E6[Trained Malicious URL Model]
        end
    end

    %% === Continuous Learning === %%
    subgraph "5️⃣ Continuous Learning"
        F1[Active Learning Loop] --> F2[Human-in-the-Loop Validation]
        F2 --> F3[Confidence Weighted Training]
        F3 --> F4[Delta Model Updates]
        F4 --> F5[Model Orchestrator]
    end

    %% === User Interface === %%
    subgraph "6️⃣ User Interface (Flutter)"
        G1[Live Dashboard] --> G2[Factual Verification Insights]
        G1 --> G3[Malicious URL Insights]
        G2 --> G4[Real-Time Fact Updates]
        G2 --> G5[Fact-Check Results Display]
        G3 --> G6[URL Source Attribution]
        G3 --> G7[Threat Level Visualization]
        G3 --> G8[Historical Context]
        G1 --> G9[Fetch Data from Trained Model]
        G9 --> G10[Cross-Platform Consistency]
        G9 --> G11[Creative Evidence Display]
        G9 --> G12[Source Attribution Map]
        G9 --> G13[Real-Time Confidence Scores]
    end

    %% === Data Flow Connections === %%
    A6 -->|Streaming Data| B1
    A6 -->|Streaming Data| D1
    A6 -->|Streaming Data| E1
    B6 --> C1
    C4 --> F1
    C4 --> G1
    D6 & E6 --> F1
    F5 --> D6 & E6
    D6 --> G2
    E6 --> G3
