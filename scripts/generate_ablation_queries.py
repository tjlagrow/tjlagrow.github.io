import json

queries = [
    # --- TEACHING (12 queries) ---
    {
        "query": "what courses does TJ teach?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Teaching", "Scaling ML Education: Ops, Pedagogy, and Teaching 1,200 Students"],
        "ground_truth_answer": "TJ is the Lead Instructor for CS 7641 (Machine Learning) in Georgia Tech's OMSCS program and has supported CS 7642 (Reinforcement Learning)."
    },
    {
        "query": "what is Markov Decision Processes?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Mastering Markov Decision Processes: A Practical RL Journey with OpenAI Gym"],
        "ground_truth_answer": "A Markov Decision Process (MDP) is a mathematical framework for modeling decision-making in environments where outcomes are partly random and partly under the control of a decision maker."
    },
    {
        "query": "how to evaluate features after dimension?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["How to Evaluate Features after Dimensionality Reduction?"],
        "ground_truth_answer": "Feature evaluation after dimensionality reduction involves analyzing variance ratios, reconstruction errors, clustering efficiency, and model performance on downstream tasks."
    },
    {
        "query": "tell me about exploratory data analysis guide",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Beginner’s Guide to Exploratory Data Analysis"],
        "ground_truth_answer": "Exploratory Data Analysis (EDA) is an approach to analyzing datasets to summarize their main characteristics, often using visual methods."
    },
    {
        "query": "what is reinforcement learning?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Teaching", "Mastering Markov Decision Processes: A Practical RL Journey with OpenAI Gym"],
        "ground_truth_answer": "Reinforcement learning is a branch of machine learning where an agent learns to make decisions by performing actions and receiving rewards."
    },
    {
        "query": "what machine learning courses are discussed in the blog?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Hello, World! OMSCS Machine Learning Blog Series", "Teaching"],
        "ground_truth_answer": "The blog series covers Georgia Tech's OMSCS CS 7641 Machine Learning course."
    },
    {
        "query": "how does TJ manage teaching 1200 students?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Scaling ML Education: Ops, Pedagogy, and Teaching 1,200 Students"],
        "ground_truth_answer": "TJ scales education using operations, structured pedagogy, specialized infrastructure, and an active teaching team."
    },
    {
        "query": "what is the OMSCS program at Georgia Tech?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Teaching", "Hello, World! OMSCS Machine Learning Blog Series"],
        "ground_truth_answer": "The Online Master of Science in Computer Science (OMSCS) is an online degree program at Georgia Tech."
    },
    {
        "query": "tell me about CS 7641 machine learning",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Teaching", "Hello, World! OMSCS Machine Learning Blog Series"],
        "ground_truth_answer": "CS 7641 is the graduate machine learning course in Georgia Tech's OMSCS program."
    },
    {
        "query": "what is OpenAI Gym in RL?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Mastering Markov Decision Processes: A Practical RL Journey with OpenAI Gym"],
        "ground_truth_answer": "OpenAI Gym is a toolkit for developing and comparing reinforcement learning algorithms."
    },
    {
        "query": "how to learn data science for beginners?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Beginner’s Guide to Exploratory Data Analysis"],
        "ground_truth_answer": "Beginners can start with Exploratory Data Analysis (EDA) to understand basic dataset characteristics, statistics, and visualization techniques."
    },
    {
        "query": "who supports CS 7642 Reinforcement Learning?",
        "intent": "Teaching",
        "ground_truth_document_titles": ["Teaching"],
        "ground_truth_answer": "Theodore J. LaGrow (TJ) has supported the instruction of CS 7642 (Reinforcement Learning) course."
    },

    # --- RESEARCH (18 queries) ---
    {
        "query": "tell me about Quasi-Periodic Patterns in Alzheimer's",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Beyond Static Connectivity: The Role of Quasi-Periodic Patterns in Alzheimer's",
            "Tracing Alzheimer's Through Spatiotemporal Brain Patterns",
            "Widespread Spatiotemporal Patterns of Functional Brain Networks in Longitudinal Progression of Alzheimer's Disease"
        ],
        "ground_truth_answer": "Quasi-Periodic Patterns (QPPs) are recurring spatiotemporal patterns of BOLD fluctuations that track progressive disconnectivity across the Alzheimer's spectrum."
    },
    {
        "query": "what is the role of resting-state fMRI in brain dynamics?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Fidelity of Spatiotemporal Patterns of Brain Activity Across Sampling Rate, Scan Duration, and Frequency Content",
            "Exploration of Spatiotemporal Dynamics in Neurodegenerative Functional Brain Networks",
            "PhD Proposal: Spatiotemporal Dynamics in Brain Networks"
        ],
        "ground_truth_answer": "Resting-state fMRI tracks infraslow fluctuations to reveal spatiotemporal dynamics, functional connectivity networks, and clinical biomarkers."
    },
    {
        "query": "tell me about cross-species functional connectivity",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Cross-Species Functional Connectivity: The Translational Bridge",
            "Functional connectivity of the brain across rodents and humans"
        ],
        "ground_truth_answer": "Cross-species functional connectivity maps connections across species (e.g. rodents and humans) to provide translational models of brain networks."
    },
    {
        "query": "what is PhD Proposal of TJ LaGrow?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "PhD Proposal: Spatiotemporal Dynamics in Brain Networks",
            "Exploration of Spatiotemporal Dynamics in Neurodegenerative Functional Brain Networks"
        ],
        "ground_truth_answer": "TJ LaGrow's PhD proposal focuses on using spatiotemporal dynamics (QPPs and cPCA) to map neurodegenerative diseases like Alzheimer's."
    },
    {
        "query": "what is complex PCA in fMRI analysis?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Fidelity of Spatiotemporal Patterns of Brain Activity Across Sampling Rate, Scan Duration, and Frequency Content",
            "Exploration of Spatiotemporal Dynamics in Neurodegenerative Functional Brain Networks"
        ],
        "ground_truth_answer": "Complex PCA (cPCA) captures phase-shifted, traveling spatiotemporal wave dynamics in resting-state fMRI BOLD signals."
    },
    {
        "query": "how is white matter functional connectivity evaluated?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Investigating White Matter Functional Network Connectivity Across the Alzheimers Disease Spectrum Using Resting-State fMRI",
            "Functional network connectivity in white matter: A spatially-guided ICA-based network approach"
        ],
        "ground_truth_answer": "White matter connectivity is analyzed using resting-state fMRI and spatially-guided ICA templates, tracking subcortical and cortical pathways."
    },
    {
        "query": "what is the QPPLab software package?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "QPPLab: A generally applicable software package for detecting, analyzing, and visualizing large-scale quasiperiodic spatiotemporal patterns (QPPs) of brain activity"
        ],
        "ground_truth_answer": "QPPLab is a MATLAB toolbox designed to detect, analyze, and visualize spatiotemporal Quasi-Periodic Patterns (QPPs) in fMRI data."
    },
    {
        "query": "what are sparse recovery methods in cell detection?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Sparse Recovery Methods for Cell Detection and Layer Estimation",
            "Approximating Cellular Densities from High-Resolution Neuroanatomical Imaging Data"
        ],
        "ground_truth_answer": "Sparse recovery uses patch-wise estimators and total-variation regularization to estimate cell density and locate cortical layers."
    },
    {
        "query": "how does scan duration affect spatiotemporal patterns?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Fidelity of Spatiotemporal Patterns of Brain Activity Across Sampling Rate, Scan Duration, and Frequency Content"
        ],
        "ground_truth_answer": "Longer scans improve the reliability of complex PCA waves, while QPP detection remains stable even with shorter scan durations."
    },
    {
        "query": "what patent did A. C. Enten and TJ LaGrow file?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Capturing diagnosable video content using a client device"
        ],
        "ground_truth_answer": "They patented a method and system for capturing high-quality diagnosable video content on a mobile client device to aid remote diagnoses."
    },
    {
        "query": "how do brain state distributions of QPPs vary?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Variation in the distribution of large-scale spatiotemporal patterns of activity across brain states"
        ],
        "ground_truth_answer": "The spatial and temporal characteristics of QPPs adapt dynamically depending on the subject's state, such as sleep, anesthesia, or task engagement."
    },
    {
        "query": "what did TJ write about scientific literature NLP?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Do You Know Where Your Research Is Being Used? An Exploration of Scientific Literature Using Natural Language Processing"
        ],
        "ground_truth_answer": "He designed an NLP pipeline to extract software and algorithm names from arXiv articles to map technology adoption trends."
    },
    {
        "query": "tell me about default mode network in musicians",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Creative tempo: Spatiotemporal dynamics of the default mode network in improvisational musicians"
        ],
        "ground_truth_answer": "This research analyzes how DMN dynamics and infraslow oscillations adapt in improvisational musicians during creative tasks."
    },
    {
        "query": "how is deep learning used in Alzheimer's classification?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Voxel-wise Fusion of Resting fMRI Networks and Gray Matter Volume for Alzheimer’s Disease Classification using Deep Multimodal Learning",
            "Voxelwise Intensity Projection for the Spatial Representation of Resting State Functional MRI Networks and Multimodal Deep Learning"
        ],
        "ground_truth_answer": "Deep multimodal learning models classify Alzheimer's stages by fusing voxel-wise resting-state fMRI network projections with gray matter volume metrics."
    },
    {
        "query": "what did Shella Keilholz publish about complexity in the HCP?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Relationship between the frequency profile of BOLD fluctuations and calculated metrics of complexity in the Human Connectome Project"
        ],
        "ground_truth_answer": "This paper showed that BOLD signal complexity metrics (entropy, Lyapunov exponents) are heavily confounded by the frequency spectra of BOLD fluctuations."
    },
    {
        "query": "what is SABER neuroimaging framework?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Toward a reproducible, scalable framework for processing large neuroimaging datasets"
        ],
        "ground_truth_answer": "SABER is a reproducible, containerized pipeline ecosystem designed for petascale volumetric neuroimaging processing."
    },
    {
        "query": "what is BOLD global signal in rats?",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Spatial and Spectral Components of the BOLD Global Signal in Rat Resting-State Functional MRI"
        ],
        "ground_truth_answer": "This study maps the spatial and spectral decomposition of the rat fMRI global signal to distinguish neural contributions from systemic noise."
    },
    {
        "query": "tell me about ECE PhD Defense of Theodore LaGrow",
        "intent": "Research",
        "ground_truth_document_titles": [
            "Exploration of Spatiotemporal Dynamics in Neurodegenerative Functional Brain Networks"
        ],
        "ground_truth_answer": "Theodore LaGrow's PhD defense covers the spatiotemporal analysis of neurodegenerative networks using fMRI BOLD time series."
    },

    # --- BIO/CONTACT (10 queries) ---
    {
        "query": "how can I contact TJ LaGrow?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["Contact"],
        "ground_truth_answer": "You can contact TJ LaGrow via email at tlagrow3@gatech.edu or submit a message using the form on his Contact Page."
    },
    {
        "query": "tell me about TJ's awards and honors",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["Honors & Awards"],
        "ground_truth_answer": "TJ's awards include the Georgia Tech Outstanding Teaching Assistant of the Year and various academic neuroimaging honors."
    },
    {
        "query": "who is TJ LaGrow?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["About"],
        "ground_truth_answer": "TJ LaGrow is a PhD candidate in Neuroengineering at the Keilholz MIND Lab, running machine learning education and resting-state fMRI research."
    },
    {
        "query": "what is TJ's email address?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["Contact"],
        "ground_truth_answer": "TJ's primary email address is tlagrow3@gatech.edu."
    },
    {
        "query": "what university does TJ LaGrow attend?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["About", "Teaching"],
        "ground_truth_answer": "TJ attends the Georgia Institute of Technology (Georgia Tech)."
    },
    {
        "query": "is TJ LaGrow a PhD Candidate?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["About"],
        "ground_truth_answer": "Yes, TJ is a PhD Candidate in the School of Electrical and Computer Engineering at Georgia Tech."
    },
    {
        "query": "what lab is TJ part of?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["About"],
        "ground_truth_answer": "TJ is a researcher in the Keilholz MIND Lab (Model-based Imaging and Neurodynamics Lab) at Georgia Tech."
    },
    {
        "query": "what is TJ's research focus?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["About", "Research"],
        "ground_truth_answer": "His research focuses on neuroengineering, resting-state fMRI spatiotemporal dynamics, and machine learning methods for neurodegenerative diseases."
    },
    {
        "query": "where can I find TJ's CV or awards list?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["Honors & Awards"],
        "ground_truth_answer": "TJ's academic accomplishments, teaching awards, and scholarship listings are documented on his Honors & Awards page."
    },
    {
        "query": "what is TJ's role in machine learning classes?",
        "intent": "Bio/Contact",
        "ground_truth_document_titles": ["About", "Teaching"],
        "ground_truth_answer": "TJ serves as the Lead Instructor for the CS 7641 Machine Learning course in the OMSCS program."
    },

    # --- GENERAL (10 queries) ---
    {
        "query": "what did AI newsletter say about LLMs?",
        "intent": "General",
        "ground_truth_document_titles": ["Newsletter #1 — What Actually Mattered in AI This Week"],
        "ground_truth_answer": "The AI newsletter discussed key advancements in LLM reasoning, code execution capabilities, and open-source models."
    },
    {
        "query": "tell me about Ramon y Cajal retinal sketch",
        "intent": "General",
        "ground_truth_document_titles": ["Ramon y Cajal Histology Retinal Drawing"],
        "ground_truth_answer": "Santiago Ramon y Cajal was a Nobel laureate who sketched detailed neuroanatomy of retinal cell structures and synapses."
    },
    {
        "query": "what is the GATO generalist agent?",
        "intent": "General",
        "ground_truth_document_titles": ["GATO: The All-in-One Generalist Agent"],
        "ground_truth_answer": "Gato is a multi-modal, multi-task, multi-embodiment generalist policy trained by DeepMind that can play games, caption images, and control robotic arms."
    },
    {
        "query": "what is Graph of Thoughts structured reasoning?",
        "intent": "General",
        "ground_truth_document_titles": ["Graph of Thoughts: Structured Reasoning with LLMs"],
        "ground_truth_answer": "Graph of Thoughts (GoT) is a framework that models LLM reasoning as a directed graph, enabling non-linear combination, aggregation, and refinement of thoughts."
    },
    {
        "query": "who is Waddles the mascot?",
        "intent": "General",
        "ground_truth_document_titles": ["Waddles AI Avatar Truffle Pig Mascot"],
        "ground_truth_answer": "Waddles is the personal chatbot mascot assistant, illustrated as a minimalist flat-vector truffle pig."
    },
    {
        "query": "what is the Ramon y Cajal brain tissue drawing?",
        "intent": "General",
        "ground_truth_document_titles": ["Ramon y Cajal Brain Tissue Sketch"],
        "ground_truth_answer": "It is a historical neurobiology sketch by Santiago Ramon y Cajal illustrating neural slice cells, cortical layers, and pyramidal structures."
    },
    {
        "query": "what is the Ask Waddles assistant?",
        "intent": "General",
        "ground_truth_document_titles": ["Waddles AI Avatar Truffle Pig Mascot"],
        "ground_truth_answer": "Ask Waddles is a local client-side RAG search chatbot using ONNX WebAssembly running in the portfolio site."
    },
    {
        "query": "tell me about the first newsletter post",
        "intent": "General",
        "ground_truth_document_titles": ["Newsletter #1 — What Actually Mattered in AI This Week"],
        "ground_truth_answer": "The newsletter discusses current trends, papers, and models in artificial intelligence, focusing on practical applicability."
    },
    {
        "query": "what does the Waddles pig avatar look like?",
        "intent": "General",
        "ground_truth_document_titles": ["Waddles AI Avatar Truffle Pig Mascot"],
        "ground_truth_answer": "Waddles is a minimalist flat-vector truffle pig mascot with dynamic mouse-move orbital interactive rings."
    },
    {
        "query": "what did Ramon y Cajal study?",
        "intent": "General",
        "ground_truth_document_titles": ["Ramon y Cajal Histology Retinal Drawing", "Ramon y Cajal Brain Tissue Sketch"],
        "ground_truth_answer": "Santiago Ramon y Cajal studied microscopic neuroanatomy and histology, pioneering the neuron doctrine through intricate drawings of neural structures."
    },

    # --- ADVERSARIAL OUT-OF-SCOPE (15 queries) ---
    {
        "query": "what is the recipe for chocolate chip cookies?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "how do I change a flat tire on a car?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "explain quantum mechanics in simple terms",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "who won the 2022 FIFA World Cup in Qatar?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "what is the average distance between Earth and Mars?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "how do you write a binary search algorithm in Python?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "what is the capital city of Australia?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "can you write a short poem about autumn leaves?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "explain Albert Einstein's general theory of relativity",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "what is the historical origin of the Great Wall of China?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "how do you treat the symptoms of a common cold?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "what are the main ingredients needed to make pesto sauce?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "explain how photosystem II works in plant photosynthesis",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "how do I compile a C++ program using gcc in terminal?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    },
    {
        "query": "who painted the Mona Lisa?",
        "intent": "Out-of-Scope",
        "ground_truth_document_titles": [],
        "ground_truth_answer": "I do not have access to that information in my retrieved context."
    }
]

# Write to file
with open("scripts/ablation_queries.json", "w", encoding="utf-8") as f:
    json.dump(queries, f, indent=2, ensure_ascii=False)

print("Generated 65 ablation queries (50 in-scope, 15 out-of-scope) in scripts/ablation_queries.json")
