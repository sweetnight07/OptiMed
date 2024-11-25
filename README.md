## OptiMed

OptiMed is a **Multi-Agent System** designed to replicate the workflow of a healthcare setting using **LangChain**. This system streamlines patient interactions by performing the following tasks:

1. **Patient Interaction**: Engages with patients to collect relevant information.
2. **Diagnosis**: Analyzes symptoms and provides a preliminary diagnosis.
3. **Treatment Recommendations**: Suggests treatments or actionable recommendations.
4. **Appointment Scheduling**: Facilitates scheduling follow-up appointments seamlessly.

### Key Features
---
Before diving into the code, here are some **key features** to note:

- **Customizable and Flexible Agent Creation**  
- **Integratable Tools for Various Agents**  
- **Reasoning Capabilities** (CoT, ReAct)  
- **Multi-Agent Collaboration** - *LangGraph* 
- **Hub and Spoke Model** 
- **Search Engine**  
- **Vector Database**  
- **Web Scraping**  
- **Google Calendar Scheduling**

### Workflow
---
Here is the workflow between agents using the Hub and Spoke Model

![alt text](/images/workflow.png)

### Agent and Tools
---
- **Master Agent**: Facilitates and delegates tasks
    - **Respond Tool** (Needed for Verbose Reasoning)

- **Nurse Agent**: Interacts with the user to gather patient information and appointment details
    - **User Interaction Tool**

- **Diagnosis Agent**: Diagnoses the patient based on the patient information
    - **Search Database**
    - **Search Engine**

- **Recommendation Agent**: Provides treatment suggestions
    - **CDC Web Scraper**

- **Reception Agent**: Sets up appointments
    - **Parse Appointment**
    - **Schedule Appointment**

### Prompting
---
Here is the prompting technique employed by each agents:
![alt text](/images/prompting.png)

### Worked Example
---
1. **Passes In Empty Template**

![alt text](/images/image-1.png)

2. **Extract Patient Information**

![alt text](/images/image-2.png)

<img src="images/image-3.png" alt="alt text" width="760" height="100">

<img src="images/image-4.png" alt="alt text" width="760" height="100">

3. **Finds Diagnosis Using Tools**

<img src="images/image-5.png" alt="alt text" width="760" height="150">

___

<img src="images/image-6.png" alt="alt text" width="760" height="150">

4. **Searches CDC Online**

<img src="images/image-8.png" alt="alt text" width="760" height="150">

___

<img src="images/image-9.png" alt="alt text" width="760" height="120">

___

<img src="images/image-10.png" alt="alt text" width="760" height="120">

5. **Sets Up An Appointment**

<img src="images/image-11.png" alt="alt text" width="760" height="150">

___

<img src="images/image-12.png" alt="alt text" width="760" height="120">

___

<img src="images/image-13.png" alt="alt text" width="760" height="120">

6. **Book An Appointment**

<img src="images/image-14.png" alt="alt text" width="760" height="150">

<img src="images/image-15.png" alt="alt text" width="760" height="150">

### Further Implementation
---
- **Subgraph in Diagnosis**: Extend the Diagnosis Agent to act as a subgraph, incorporating multiple specialist agents to provide more detailed and specialized diagnoses.

- **Efficient Vector Database Searching**: Add a tool that extracts metadata from PDFs, allowing query lookups by 'source'. This approach will enable flexible filtering without the need for database recreation.

- **Expand Data**: Create separate folders for different disciplines, each with its own dedicated vector database, to better organize and manage diverse healthcare data.

- **Deterministic Outputs**: Implement **Few-Shot Learning (FSL)** to ensure consistent and reliable results across similar queries, reducing the need for retraining.

- **Efficient Searching**: Implement a caching system to improve search speeds. Additionally, explore switching to Google’s Search API, considering its costs and balancing efficiency with budget.

- **PageRank for Better Relevance**: Integrate a PageRank-like algorithm to prioritize and rank search results, improving the relevance of returned information.

- **Robust Testing**: Finetune the prompts
