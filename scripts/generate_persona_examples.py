import json
import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_FILE = os.path.join(PROJECT_ROOT, "scripts", "persona_examples.json")

# Define 100 base queries, categories, facts, and specifics for each query
BASE_DATA = [
    # --- TEACHING (1-25) ---
    {
        "id": 1,
        "category": "Teaching",
        "query": "Who is the instructor for CS 7641?",
        "facts": "TJ LaGrow is the Lead Instructor for CS 7641 (Machine Learning) in OMSCS at Georgia Tech, managing 1400+ students with 30+ TAs.",
        "subjects": ["TJ LaGrow", "CS 7641", "1400+ students"],
        "followups": ["Does TJ teach other classes?", "How many TAs help him?"]
    },
    {
        "id": 2,
        "category": "Teaching",
        "query": "What classes does TJ teach?",
        "facts": "TJ leads CS 7641 (Machine Learning) and supports CS 7642 (Reinforcement Learning) in Georgia Tech's OMSCS program.",
        "subjects": ["CS 7641 Machine Learning", "CS 7642 Reinforcement Learning"],
        "followups": ["Is reinforcement learning hard?", "What is his teaching history?"]
    },
    {
        "id": 3,
        "category": "Teaching",
        "query": "Does TJ support CS 7642 Reinforcement Learning?",
        "facts": "Yes, TJ supports CS 7642 (Reinforcement Learning) in the Georgia Tech OMSCS program, coordinating course updates.",
        "subjects": ["CS 7642", "Reinforcement Learning"],
        "followups": ["Who teaches CS 7641?", "Is CS 7642 harder than CS 7641?"]
    },
    {
        "id": 4,
        "category": "Teaching",
        "query": "How many OMSCS students are in CS 7641?",
        "facts": "There are over 1400 master's students enrolled in CS 7641 Machine Learning each semester.",
        "subjects": ["1400+ students", "OMSCS program"],
        "followups": ["How does he grade them all?", "How many TAs are there?"]
    },
    {
        "id": 5,
        "category": "Teaching",
        "query": "How many TAs are in CS 7641?",
        "facts": "TJ coordinates a crew of over 30 Teaching Assistants to manage grading, office hours, and student support.",
        "subjects": ["30+ TAs", "grading and support"],
        "followups": ["Who is the head TA?", "How can I become a TA?"]
    },
    {
        "id": 6,
        "category": "Teaching",
        "query": "What is the homework deadline policy in OMSCS?",
        "facts": "Assignments are typically due at 11:59 PM UTC-12 (Anywhere on Earth time) on the specified due date.",
        "subjects": ["11:59 PM UTC-12", "Anywhere on Earth (AoE)"],
        "followups": ["Can I get an extension?", "Is there a penalty for late submission?"]
    },
    {
        "id": 7,
        "category": "Teaching",
        "query": "What is the project workload like in CS 7641?",
        "facts": "Students complete four major projects involving coding and detailed analysis of ML algorithms.",
        "subjects": ["four major projects", "code and analysis"],
        "followups": ["Which project is the hardest?", "Are group projects allowed?"]
    },
    {
        "id": 8,
        "category": "Teaching",
        "query": "What is the CS 7641 midterm exam format?",
        "facts": "The midterm exam is proctored, closed-book, and consists of multiple choice and short answer questions covering theoretical concepts.",
        "subjects": ["proctored exam", "closed-book theory"],
        "followups": ["Is there a final exam?", "How should I study for the midterm?"]
    },
    {
        "id": 9,
        "category": "Teaching",
        "query": "Is there a curve in CS 7641?",
        "facts": "Yes, grading curves are traditionally applied at the end of the term to align grade distributions with class performance.",
        "subjects": ["grading curves", "end of term alignment"],
        "followups": ["What score is typically an A?", "How is the midterm curved?"]
    },
    {
        "id": 10,
        "category": "Teaching",
        "query": "What teaching awards did TJ win?",
        "facts": "TJ won the Georgia Tech Outstanding Graduate Teaching Assistant of the Year award for his excellence in scaling ML pedagogy.",
        "subjects": ["Outstanding GTA award", "Georgia Tech"],
        "followups": ["When did he win it?", "What other awards does he have?"]
    },
    {
        "id": 11,
        "category": "Teaching",
        "query": "Where can I find the CS 7641 syllabus?",
        "facts": "The syllabus is hosted on the course website and the Canvas learning portal at the beginning of each semester.",
        "subjects": ["course syllabus", "Canvas portal"],
        "followups": ["What are the textbook details?", "Is the schedule fixed?"]
    },
    {
        "id": 12,
        "category": "Teaching",
        "query": "What is the workload of the Reinforcement Learning class?",
        "facts": "CS 7642 requires completing deep RL projects using OpenAI Gym environments and writing analytical papers.",
        "subjects": ["OpenAI Gym projects", "analytical papers"],
        "followups": ["What algorithms are covered?", "Is CS 7642 math-heavy?"]
    },
    {
        "id": 13,
        "category": "Teaching",
        "query": "Is CS 7641 machine learning hard?",
        "facts": "Yes, CS 7641 is a demanding graduate course due to its rigorous projects, detailed paper analyses, and conceptual exams.",
        "subjects": ["demanding course", "rigorous projects"],
        "followups": ["How many hours a week does it take?", "What programming language is used?"]
    },
    {
        "id": 14,
        "category": "Teaching",
        "query": "What topics are covered in CS 7641?",
        "facts": "Topics include Supervised Learning, Randomized Optimization, Unsupervised Learning, and Reinforcement Learning.",
        "subjects": ["Supervised/Unsupervised Learning", "Randomized Optimization", "RL"],
        "followups": ["Do we cover deep learning?", "What math is required?"]
    },
    {
        "id": 15,
        "category": "Teaching",
        "query": "How are CS 7641 office hours scheduled?",
        "facts": "Office hours are held weekly by TAs via Ed Discussion, Teams, or BlueJeans, with TJ running specialized Q&A sessions.",
        "subjects": ["weekly TA sessions", "Ed Discussion Q&A"],
        "followups": ["How can I ask TJ a private question?", "Are office hours recorded?"]
    },
    {
        "id": 16,
        "category": "Teaching",
        "query": "How should I study for the CS 7641 midterm?",
        "facts": "Review class lectures, lecture transcripts, project material, and practice problem sets focusing on theoretical understanding.",
        "subjects": ["lectures and transcripts", "theoretical concepts"],
        "followups": ["Are past exams available?", "Does the curve help?"]
    },
    {
        "id": 17,
        "category": "Teaching",
        "query": "What programming language is used in CS 7641?",
        "facts": "Students can use Python or Java for projects, though Python is highly recommended due to library support.",
        "subjects": ["Python or Java", "library support"],
        "followups": ["Which library is allowed?", "Is PyTorch permitted?"]
    },
    {
        "id": 18,
        "category": "Teaching",
        "query": "What is the project grading timeline?",
        "facts": "Due to the class size of 1400+, projects typically take 2-3 weeks to grade by the TA grading pool.",
        "subjects": ["2-3 weeks grading", "TA grading pool"],
        "followups": ["Can I request a regrade?", "How are scores published?"]
    },
    {
        "id": 19,
        "category": "Teaching",
        "query": "How can I become a CS 7641 TA?",
        "facts": "OMSCS students who score an A in the class can apply to become a TA through the Georgia Tech application portal.",
        "subjects": ["Georgia Tech application", "score an A"],
        "followups": ["Is it paid?", "What is the time commitment?"]
    },
    {
        "id": 20,
        "category": "Teaching",
        "query": "Are CS 7641 lectures available publicly?",
        "facts": "Yes, the course lectures are available on Udacity and linked through the public course site for student viewing.",
        "subjects": ["Udacity lectures", "public course links"],
        "followups": ["Are they out of date?", "Who recorded them?"]
    },
    {
        "id": 21,
        "category": "Teaching",
        "query": "What is the workload difference between ML and RL?",
        "facts": "ML (CS 7641) focuses on broad algorithm analysis, while RL (CS 7642) involves implementing complex agent networks in code.",
        "subjects": ["ML broad analysis", "RL coding implementations"],
        "followups": ["Which should I take first?", "Which has harder exams?"]
    },
    {
        "id": 22,
        "category": "Teaching",
        "query": "Are there textbook requirements for CS 7641?",
        "facts": "No textbook is strictly required, though textbooks by Mitchell or Bishop are recommended for reference.",
        "subjects": ["no required textbook", "Mitchell or Bishop reference"],
        "followups": ["Are lectures self-contained?", "Where can I get the reading list?"]
    },
    {
        "id": 23,
        "category": "Teaching",
        "query": "What are the prerequisites for CS 7641?",
        "facts": "Prerequisites include solid Python coding, basic linear algebra, multivariate calculus, and introductory probability.",
        "subjects": ["Python coding", "linear algebra and calculus"],
        "followups": ["Is there a diagnostic test?", "Can I review math online?"]
    },
    {
        "id": 24,
        "category": "Teaching",
        "query": "What courses are in the OMSCS ML specialization?",
        "facts": "The specialization requires Core courses like CS 7641 and electives like Deep Learning, RL, and Computer Vision.",
        "subjects": ["Core CS 7641", "DL and RL electives"],
        "followups": ["How many classes are required?", "Can I double-specialize?"]
    },
    {
        "id": 25,
        "category": "Teaching",
        "query": "What is the CS 7641 academic integrity policy?",
        "facts": "Sharing project code is strictly prohibited; all code and analysis reports must be individual work under the GT Honor Code.",
        "subjects": ["no code sharing", "GT Honor Code"],
        "followups": ["Can we discuss algorithms?", "How is plagiarism detected?"]
    },

    # --- RESEARCH (26-50) ---
    {
        "id": 26,
        "category": "Research",
        "query": "Where is the Keilholz MIND Lab located?",
        "facts": "The MIND Lab is located in the Emory University and Georgia Tech joint department of biomedical engineering.",
        "subjects": ["joint BME department", "Emory and Georgia Tech"],
        "followups": ["What is the lab's address?", "Who is the principal investigator?"]
    },
    {
        "id": 27,
        "category": "Research",
        "query": "What is TJ's resting-state fMRI research about?",
        "facts": "TJ's research tracks resting-state fMRI brain signals to identify spatiotemporal patterns and functional connectivity networks.",
        "subjects": ["resting-state fMRI", "spatiotemporal signals"],
        "followups": ["What is a spatiotemporal pattern?", "How are scans recorded?"]
    },
    {
        "id": 28,
        "category": "Research",
        "query": "What are Quasi-Periodic Patterns (QPPs)?",
        "facts": "QPPs are recurring, low-frequency spatiotemporal patterns of brain activity observed in functional neuroimaging.",
        "subjects": ["recurring spatiotemporal activity", "low-frequency fMRI signals"],
        "followups": ["How are QPPs detected?", "Are QPPs altered in diseases?"]
    },
    {
        "id": 29,
        "category": "Research",
        "query": "How are fMRI brain patterns used in Alzheimer's?",
        "facts": "Disruptions in Quasi-Periodic Patterns (QPPs) act as dynamic fMRI biomarkers to detect Alzheimer's before clinical symptoms manifest.",
        "subjects": ["dynamic fMRI biomarkers", "Alzheimer's disease detection"],
        "followups": ["What changes occur in QPPs?", "Are there other biomarkers?"]
    },
    {
        "id": 30,
        "category": "Research",
        "query": "What are spatiotemporal brain dynamics?",
        "facts": "Spatiotemporal dynamics refer to changes in functional connectivity and activation patterns across both space and time in the brain.",
        "subjects": ["activation patterns over time", "functional connectivity"],
        "followups": ["How are they modeled?", "What math is used?"]
    },
    {
        "id": 31,
        "category": "Research",
        "query": "Is dynamic fMRI research helpful for Parkinson's?",
        "facts": "Yes, tracking spatiotemporal brain patterns reveals subcortical connectivity alterations, serving as early diagnostic indicators for Parkinson's.",
        "subjects": ["subcortical connectivity", "diagnostic indicators"],
        "followups": ["Does Parkinson's alter QPPs?", "What models are used?"]
    },
    {
        "id": 32,
        "category": "Research",
        "query": "How is brain graph topology compared across species?",
        "facts": "Researchers align resting-state functional MRI graph networks between rodents and humans to build comparative translational bridges.",
        "subjects": ["rodent and human graphs", "comparative neuroimaging"],
        "followups": ["Which features are conserved?", "What databases are used?"]
    },
    {
        "id": 33,
        "category": "Research",
        "query": "What is Helmholtz-Hodge decomposition in fMRI?",
        "facts": "It decomposes spontaneous BOLD phase-flows into solenoidal (rotational/curl) and gradient (broadcasting) vector fields.",
        "subjects": ["solenoidal and gradient fields", "BOLD phase-flows"],
        "followups": ["What is rotational flow?", "How is curl calculated?"]
    },
    {
        "id": 34,
        "category": "Research",
        "query": "What are broadcasting and integration brain dynamics?",
        "facts": "Broadcasting dynamics scatter information globally (gradients), while integration dynamics merge local network details (curl).",
        "subjects": ["broadcasting gradients", "integration curl"],
        "followups": ["Which brain networks broadcast?", "How are these mapped?"]
    },
    {
        "id": 35,
        "category": "Research",
        "query": "How is HCP shared drive data used?",
        "facts": "Researchers retrieve resting-state scans from the Human Connectome Project (HCP) to validate cohorts and functional networks.",
        "subjects": ["Human Connectome Project", "cohort validation"],
        "followups": ["How big is the dataset?", "Are rodent datasets included?"]
    },
    {
        "id": 36,
        "category": "Research",
        "query": "What is the impact of scan duration and sampling rate?",
        "facts": "Scan duration and TR (sampling rate) directly affect the signal-to-noise ratio and stability of spatiotemporal pattern calculations.",
        "subjects": ["sampling rate (TR)", "signal-to-noise stability"],
        "followups": ["What is a typical TR?", "Is longer scan always better?"]
    },
    {
        "id": 37,
        "category": "Research",
        "query": "What is the algorithm for QPP detection?",
        "facts": "The algorithm uses a sliding-window correlation method to iteratively template and extract recurring low-frequency spatiotemporal segments.",
        "subjects": ["sliding-window correlation", "iterative template extraction"],
        "followups": ["Is the code open-source?", "What is the complexity?"]
    },
    {
        "id": 38,
        "category": "Research",
        "query": "What is rotational flow in brain dynamics?",
        "facts": "Rotational flow refers to loop-like, cyclic patterns of phase propagation across cortical networks during rest.",
        "subjects": ["cyclic phase propagation", "cortical loops"],
        "followups": ["How does it link to BOLD?", "What models track it?"]
    },
    {
        "id": 39,
        "category": "Research",
        "query": "What are solenoidal and curl decomposition?",
        "facts": "Solenoidal fields capture vector fields with zero divergence, representing stable cycles (curl) in phase connectivity trajectories.",
        "subjects": ["solenoidal fields", "divergence-free cycles"],
        "followups": ["How are phase angles resolved?", "Is this linear?"]
    },
    {
        "id": 40,
        "category": "Research",
        "query": "What is functional connectivity graph topology?",
        "facts": "It models brain regions as nodes and correlation values as edges to analyze network properties like path length and efficiency.",
        "subjects": ["nodes and edges model", "path length efficiency"],
        "followups": ["Are brain graphs scale-free?", "What tools calculate this?"]
    },
    {
        "id": 41,
        "category": "Research",
        "query": "What is the Ramon y Cajal histology drawing?",
        "facts": "Nobel laureate Santiago Ramon y Cajal drew detailed sketches of retinal neurons and synaptic connections, founding neurobiology.",
        "subjects": ["historical drawings", "retinal cell connections"],
        "followups": ["Where are the drawings kept?", "Who was Cajal?"]
    },
    {
        "id": 42,
        "category": "Research",
        "query": "What are the cerebral cortex layers in neuroanatomy?",
        "facts": "The mammalian neocortex is organized into six distinct histological layers, containing specific neuron classes and projections.",
        "subjects": ["six neocortex layers", "neuron projections"],
        "followups": ["Which layer has pyramidal cells?", "Are layers conserved?"]
    },
    {
        "id": 43,
        "category": "Research",
        "query": "What is TJ's PhD dissertation topic?",
        "facts": "TJ's dissertation focuses on 'Exploration of Spatiotemporal Dynamics in Neurodegenerative Functional Brain Networks'.",
        "subjects": ["neurodegeneration dynamics", "PhD dissertation"],
        "followups": ["When is his defense?", "Who is on his committee?"]
    },
    {
        "id": 44,
        "category": "Research",
        "query": "Who funds the MIND Lab's research?",
        "facts": "The MIND Lab's resting-state brain research is funded by the National Institutes of Health (NIH) and other neuroimaging grants.",
        "subjects": ["National Institutes of Health (NIH)", "neuroimaging grants"],
        "followups": ["What grants does TJ have?", "Is there corporate funding?"]
    },
    {
        "id": 45,
        "category": "Research",
        "query": "What are HCP cohort alignment protocols?",
        "facts": "Scans are aligned using surface-based registration (MSMAll) and mapped to standard coordinate spaces (CIFTI grayordinates).",
        "subjects": ["surface-based MSMAll", "CIFTI grayordinates"],
        "followups": ["Does it normalize brain sizes?", "What voxel size is used?"]
    },
    {
        "id": 46,
        "category": "Research",
        "query": "What brain biomarkers indicate Parkinson's?",
        "facts": "Biomarkers include reduced connectivity in basal ganglia circuits and flattened trajectory patterns in dynamic state graphs.",
        "subjects": ["basal ganglia circuits", "state graph trajectories"],
        "followups": ["Can fMRI detect it early?", "How is accuracy validated?"]
    },
    {
        "id": 47,
        "category": "Research",
        "query": "What are spatiotemporal patterns in resting state?",
        "facts": "They are coherent patterns of BOLD fluctuations that propagate systematically across functional brain networks during wakeful rest.",
        "subjects": ["coherent BOLD fluctuations", "wakeful rest networks"],
        "followups": ["Are they present in sleep?", "How do they change with age?"]
    },
    {
        "id": 48,
        "category": "Research",
        "query": "What is rest-fMRI signal frequency content?",
        "facts": "Low-frequency fluctuations typically dominate resting-state signals, ranging between 0.01 Hz and 0.1 Hz.",
        "subjects": ["low-frequency fluctuations", "0.01 to 0.1 Hz band"],
        "followups": ["What filters are applied?", "What is high-frequency noise?"]
    },
    {
        "id": 49,
        "category": "Research",
        "query": "Why compare brain connectivity cross-species?",
        "facts": "Comparing rodent and human networks helps translate animal model drug discovery findings to clinical human diagnostics.",
        "subjects": ["animal model translation", "clinical human diagnostics"],
        "followups": ["What models are used?", "Is brain topology the same?"]
    },
    {
        "id": 50,
        "category": "Research",
        "query": "Where can I read MIND Lab publications?",
        "facts": "MIND Lab papers are published in neuroimaging journals like NeuroImage, Human Brain Mapping, and on PubMed/Google Scholar.",
        "subjects": ["NeuroImage journal", "Google Scholar profiles"],
        "followups": ["How many citations does TJ have?", "Are the papers open access?"]
    },

    # --- BIO/CONTACT (51-75) ---
    {
        "id": 51,
        "category": "Bio/Contact",
        "query": "What is TJ's email address?",
        "facts": "TJ's official academic contact email at Georgia Tech is tlagrow3@gatech.edu.",
        "subjects": ["tlagrow3@gatech.edu", "Georgia Tech contact"],
        "followups": ["Can I contact him via phone?", "What is his personal email?"]
    },
    {
        "id": 52,
        "category": "Bio/Contact",
        "query": "Does TJ have a LinkedIn profile?",
        "facts": "Yes, TJ has a professional LinkedIn profile linking his academic achievements, research portfolio, and teaching roles.",
        "subjects": ["professional LinkedIn", "academic profile"],
        "followups": ["What is his LinkedIn handle?", "Does he share portfolio updates?"]
    },
    {
        "id": 53,
        "category": "Bio/Contact",
        "query": "Where is TJ's GitHub repository?",
        "facts": "TJ's code repositories are hosted on GitHub, containing REST-fMRI analysis pipelines and teaching demonstration scripts.",
        "subjects": ["GitHub repositories", "analysis pipelines"],
        "followups": ["What is his GitHub username?", "Is the waddles code open-source?"]
    },
    {
        "id": 54,
        "category": "Bio/Contact",
        "query": "What honors has TJ received?",
        "facts": "TJ's academic honors include the Outstanding GTA award, conference paper awards, and competitive graduate fellowships.",
        "subjects": ["GTA award", "graduate fellowships"],
        "followups": ["Which fellowship did he win?", "When did he win the GTA award?"]
    },
    {
        "id": 55,
        "category": "Bio/Contact",
        "query": "When did he win Outstanding Teaching Assistant?",
        "facts": "TJ received the Georgia Tech Outstanding Graduate Teaching Assistant of the Year award during the annual awards ceremony.",
        "subjects": ["GTA of the Year", "GT awards ceremony"],
        "followups": ["Who nominated him?", "What did he win?"]
    },
    {
        "id": 56,
        "category": "Bio/Contact",
        "query": "Where is TJ completing his PhD?",
        "facts": "TJ is completing his PhD in Bioengineering/Neuroengineering at the Keilholz MIND Lab at Georgia Tech and Emory University.",
        "subjects": ["PhD in Bioengineering", "Georgia Tech and Emory"],
        "followups": ["What is his thesis about?", "When will he graduate?"]
    },
    {
        "id": 57,
        "category": "Bio/Contact",
        "query": "What lab does TJ work in?",
        "facts": "TJ conducts his research at the MIND Lab (Magnetic Resonance Imaging in Neuroscience & Disease) led by Dr. Shella Keilholz.",
        "subjects": ["MIND Lab", "Dr. Shella Keilholz"],
        "followups": ["Where is the lab located?", "What instruments do they use?"]
    },
    {
        "id": 58,
        "category": "Bio/Contact",
        "query": "Where is the contact form on his website?",
        "facts": "A secure contact submission form is available on the site's dedicated Contact Page for messages.",
        "subjects": ["secure contact form", "Contact Page"],
        "followups": ["Where is the Contact link?", "How fast does he reply?"]
    },
    {
        "id": 59,
        "category": "Bio/Contact",
        "query": "How can I book TJ for a speaking engagement?",
        "facts": "To request speaking sessions, submit details via the site contact form or contact tlagrow3@gatech.edu with event scope.",
        "subjects": ["speaking requests", "email inquiry"],
        "followups": ["Does he travel?", "What topics does he present?"]
    },
    {
        "id": 60,
        "category": "Bio/Contact",
        "query": "Does TJ have a Google Scholar profile?",
        "facts": "Yes, TJ has a Google Scholar page listing his peer-reviewed research papers and citation statistics.",
        "subjects": ["Google Scholar page", "peer-reviewed research"],
        "followups": ["How many citations does he have?", "What is his h-index?"]
    },
    {
        "id": 61,
        "category": "Bio/Contact",
        "query": "How can I contact TJ's teaching assistants?",
        "facts": "Students can contact TAs through the Ed Discussion workspace or Canvas messaging system of CS 7641.",
        "subjects": ["Ed Discussion workspace", "Canvas messaging"],
        "followups": ["Who is the head TA?", "Can I email TAs directly?"]
    },
    {
        "id": 62,
        "category": "Bio/Contact",
        "query": "What is TJ's graduation timeline?",
        "facts": "TJ is slated to defend his doctoral dissertation and graduate from Georgia Tech's bioengineering program in the coming terms.",
        "subjects": ["doctoral dissertation defense", "bioengineering program"],
        "followups": ["Is his defense open to public?", "Where will he work next?"]
    },
    {
        "id": 63,
        "category": "Bio/Contact",
        "query": "Does TJ have a YouTube channel?",
        "facts": "TJ hosts educational videos and research walkthroughs on his professional YouTube channel.",
        "subjects": ["YouTube educational channel", "research walkthroughs"],
        "followups": ["What is the channel name?", "Are there lectures?"]
    },
    {
        "id": 64,
        "category": "Bio/Contact",
        "query": "Where can I view his professional CV?",
        "facts": "TJ's academic CV is accessible in PDF format on the About page of his personal portfolio website.",
        "subjects": ["academic CV PDF", "About page portfolio"],
        "followups": ["Is it up to date?", "Can I download it?"]
    },
    {
        "id": 65,
        "category": "Bio/Contact",
        "query": "Who is TJ's advisor?",
        "facts": "TJ's doctoral dissertation advisor is Dr. Shella Keilholz, Professor of Biomedical Engineering.",
        "subjects": ["Dr. Shella Keilholz", "Biomedical Engineering"],
        "followups": ["What is her lab about?", "How long have they worked together?"]
    },
    {
        "id": 66,
        "category": "Bio/Contact",
        "query": "What are TJ's research interests?",
        "facts": "His interests encompass neuroimaging, resting-state fMRI dynamic networks, machine learning models, and dynamic biomarkers.",
        "subjects": ["neuroimaging networks", "dynamic biomarkers"],
        "followups": ["Does he do deep learning?", "What animal models does he study?"]
    },
    {
        "id": 67,
        "category": "Bio/Contact",
        "query": "Where did TJ do his undergraduate degree?",
        "facts": "TJ completed his bachelor's degree in engineering before pursuing graduate bioengineering at Georgia Tech.",
        "subjects": ["bachelor's in engineering", "graduate bioengineering"],
        "followups": ["Which university was it?", "What was his major?"]
    },
    {
        "id": 68,
        "category": "Bio/Contact",
        "query": "How do I cite TJ's papers?",
        "facts": "You can copy standard APA or BibTeX citation formats directly from TJ's Google Scholar publication list.",
        "subjects": ["APA or BibTeX citation", "Google Scholar list"],
        "followups": ["What is his most cited paper?", "Are there links to BibTeX?"]
    },
    {
        "id": 69,
        "category": "Bio/Contact",
        "query": "Is TJ available for consulting?",
        "facts": "TJ accepts consulting requests on neuroimaging analysis pipelines and ML education scaling depending on availability.",
        "subjects": ["neuroimaging pipelines", "consulting requests"],
        "followups": ["What are his rates?", "How do I submit a proposal?"]
    },
    {
        "id": 70,
        "category": "Bio/Contact",
        "query": "What is TJ's teaching philosophy?",
        "facts": "TJ's philosophy balances rigorous theoretical alignment (backward design) with scaled accessibility using online tools.",
        "subjects": ["backward design theory", "scaled accessibility tools"],
        "followups": ["What is backward design?", "How does he scale grading?"]
    },
    {
        "id": 71,
        "category": "Bio/Contact",
        "query": "How can I collaborate on a research project?",
        "facts": "Send a detailed proposal outlining the dataset and methods scope to tlagrow3@gatech.edu for collaboration reviews.",
        "subjects": ["dataset and methods scope", "collaboration review"],
        "followups": ["Does he share code?", "What data does he need?"]
    },
    {
        "id": 72,
        "category": "Bio/Contact",
        "query": "Where is TJ's office located at Georgia Tech?",
        "facts": "TJ's workspace is located inside the Emory/GT Biomedical Engineering building on the Georgia Tech campus.",
        "subjects": ["Emory/GT BME building", "Georgia Tech campus"],
        "followups": ["What is the room number?", "Can I drop by?"]
    },
    {
        "id": 73,
        "category": "Bio/Contact",
        "query": "Who is Theodore J. LaGrow?",
        "facts": "Theodore J. LaGrow (TJ) is a PhD candidate in Neuroengineering at Georgia Tech, specializing in fMRI dynamics and ML instruction.",
        "subjects": ["PhD candidate in Neuroengineering", "fMRI and ML instruction"],
        "followups": ["What is his research lab?", "Has he won teaching awards?"]
    },
    {
        "id": 74,
        "category": "Bio/Contact",
        "query": "Where is TJ's professional portfolio site hosted?",
        "facts": "TJ's website is hosted statically via GitHub Pages under the domain tjlagrow.github.io.",
        "subjects": ["GitHub Pages hosting", "tjlagrow.github.io"],
        "followups": ["What Jekyll theme is used?", "Is the source public?"]
    },
    {
        "id": 75,
        "category": "Bio/Contact",
        "query": "How can I find TJ's ORCID iD?",
        "facts": "TJ's ORCID iD is linked on his research profile page and listed on his publication templates.",
        "subjects": ["ORCID iD", "research profile"],
        "followups": ["What is his ORCID number?", "Is it linked to Google Scholar?"]
    },

    # --- GENERAL/CHATBOT (76-100) ---
    {
        "id": 76,
        "category": "General",
        "query": "Who is Waddles?",
        "facts": "Waddles is the truffle pig mascot and client-side conversational RAG assistant running in-browser neural networks.",
        "subjects": ["truffle pig mascot", "conversational RAG assistant"],
        "followups": ["Is Waddles run locally?", "How is it configured?"]
    },
    {
        "id": 77,
        "category": "General",
        "query": "Is Waddles run locally?",
        "facts": "Yes, Waddles runs models entirely client-side in the browser using WebAssembly and ONNX Runtime, preserving privacy.",
        "subjects": ["client-side in browser", "WebAssembly ONNX runtime"],
        "followups": ["What models does it run?", "Does it work offline?"]
    },
    {
        "id": 78,
        "category": "General",
        "query": "What embedder model does Waddles use?",
        "facts": "Waddles utilizes the all-MiniLM-L6-v2 transformer model to encode user queries and sentences into 384-dimensional vectors.",
        "subjects": ["all-MiniLM-L6-v2 embedder", "384-dimensional vectors"],
        "followups": ["What is the vector length?", "Is it cached in the browser?"]
    },
    {
        "id": 79,
        "category": "General",
        "query": "What is Cross-Encoder reranking?",
        "facts": "Cross-Encoder reranking (ms-marco-MiniLM-L-6-v2) processes query-passage pairs jointly to compute attention scores.",
        "subjects": ["ms-marco-MiniLM-L-6-v2 reranker", "joint query-passage attention"],
        "followups": ["How is it different from Bi-Encoder?", "What is the speed?"]
    },
    {
        "id": 80,
        "category": "General",
        "query": "What is Reciprocal Rank Fusion (RRF)?",
        "facts": "RRF is an algorithm that blends retrieval lists from sparse (BM25) and dense (vector) searches by summing reciprocal ranks.",
        "subjects": ["RRF blending algorithm", "sparse and dense rank summation"],
        "followups": ["What value of k is used?", "Why use RRF?"]
    },
    {
        "id": 81,
        "category": "General",
        "query": "What is the value of k in RRF?",
        "facts": "Waddles sets the RRF smoothing constant k to 60, preventing low-ranking outliers from warping the fusion score.",
        "subjects": ["smoothing constant k=60", "prevent rank outliers warping"],
        "followups": ["Can I customize k?", "What happens if k is 0?"]
    },
    {
        "id": 82,
        "category": "General",
        "query": "How does sentence compression work in Waddles?",
        "facts": "Waddles splits retrieved document chunks into sentences and computes their cosine dot product to select the top 8 candidates.",
        "subjects": ["sentence-level split", "cosine dot product selection"],
        "followups": ["What is the threshold?", "Does it keep context order?"]
    },
    {
        "id": 83,
        "category": "General",
        "query": "What is ONNX Runtime WebAssembly performance?",
        "facts": "ONNX Runtime Web runs compiled model graphs client-side using WebAssembly threads and WebGPU acceleration.",
        "subjects": ["WebAssembly multi-threading", "WebGPU graph acceleration"],
        "followups": ["What is the generation latency?", "Is it supported in Safari?"]
    },
    {
        "id": 84,
        "category": "General",
        "query": "What is the GATO generalist agent?",
        "facts": "Gato is a multi-modal generalist policy by DeepMind that plays Atari, captions images, and controls a robotic arm.",
        "subjects": ["DeepMind Gato", "multi-modal generalist policy"],
        "followups": ["How many parameters is it?", "Is it run in the browser?"]
    },
    {
        "id": 85,
        "category": "General",
        "query": "What is Graph of Thoughts structured reasoning?",
        "facts": "Graph of Thoughts models LLM reasoning steps as a graph, allowing non-linear merging, branching, and backtracking.",
        "subjects": ["reasoning steps as graph", "non-linear merging/branching"],
        "followups": ["How does it compare to Chain of Thought?", "Is it implemented in Waddles?"]
    },
    {
        "id": 86,
        "category": "General",
        "query": "What is the client-side sandbox privacy guarantee?",
        "facts": "Since models execute locally in the browser, your query and document text never leave your machine or hit AI servers.",
        "subjects": ["in-browser local execution", "no data sent to AI servers"],
        "followups": ["Are network logs sent?", "Is my chat history saved?"]
    },
    {
        "id": 87,
        "category": "General",
        "query": "Why is Waddles a truffle pig?",
        "facts": "Waddles represents a truffle pig because he sniffs out relevant research nuggets (truffles) from the portfolio database.",
        "subjects": ["truffle pig analogy", "sniffing out research data"],
        "followups": ["Does the avatar snort?", "Who drew the mascot?"]
    },
    {
        "id": 88,
        "category": "General",
        "query": "What is the memory footprint of SmolLM2-360M?",
        "facts": "SmolLM2-360M quantized in 4-bit (q4) has a download size of ~200 MB and consumes ~280 MB of RAM during execution.",
        "subjects": ["~200 MB download size", "~280 MB RAM consumption"],
        "followups": ["What is the fp16 size?", "Is it faster than Qwen?"]
    },
    {
        "id": 89,
        "category": "General",
        "query": "What is the size of Qwen2.5-0.5B in the browser?",
        "facts": "Qwen2.5-0.5B in 4-bit format is a 260 MB weight download and requires about 350 MB of RAM to run.",
        "subjects": ["260 MB weight download", "350 MB RAM allocation"],
        "followups": ["Does it support multiple languages?", "Is it context-limited?"]
    },
    {
        "id": 90,
        "category": "General",
        "query": "Does ONNX runtime support WebGPU?",
        "facts": "Yes, ONNX Runtime Web supports WebGPU execution, offloading matrix multiplication directly to the client's graphics card.",
        "subjects": ["WebGPU offloading", "matrix math on graphics card"],
        "followups": ["Does it require special flags?", "Is it faster than CPU?"]
    },
    {
        "id": 91,
        "category": "General",
        "query": "Does Waddles send queries to OpenAI?",
        "facts": "No, Waddles does not call OpenAI or any external API; all RAG and generation steps execute offline in your browser tab.",
        "subjects": ["no OpenAI calls", "fully offline execution"],
        "followups": ["How are weights downloaded?", "Does it use cookies?"]
    },
    {
        "id": 92,
        "category": "General",
        "query": "What synonyms are expanded by Waddles?",
        "facts": "Synonyms include ML to Machine Learning, RL to Reinforcement Learning, QPP to Quasi-Periodic Patterns, and fMRI to resting-state fMRI.",
        "subjects": ["ML/RL acronyms", "QPP/fMRI expansions"],
        "followups": ["Where is this mapping configured?", "Can I add custom synonyms?"]
    },
    {
        "id": 93,
        "category": "General",
        "query": "What are sliding-window query compression rules?",
        "facts": "If query length exceeds 20 words, Waddles retains only the first and last sentences to prevent context bloat.",
        "subjects": ["first and last sentences", "prevent context bloat"],
        "followups": ["How are sentences split?", "Can I disable compression?"]
    },
    {
        "id": 94,
        "category": "General",
        "query": "What are the intent pre-filtering category tags?",
        "facts": "Intent tags include 'Teaching', 'Research', and 'Bio/Contact', aligning searches to specific portfolio database sections.",
        "subjects": ["Teaching/Research tags", "partitioned search space"],
        "followups": ["How is intent classified?", "What if intent is General?"]
    },
    {
        "id": 95,
        "category": "General",
        "query": "How does Waddles handle context length limits?",
        "facts": "Waddles restricts the prompt context by feeding only the top 4 re-ranked sentence candidates into the generation window.",
        "subjects": ["top 4 reranked sentences", "strict prompt context limits"],
        "followups": ["What is the total token limit?", "Does it drop history?"]
    },
    {
        "id": 96,
        "category": "General",
        "query": "Does the chatbot play audio effects?",
        "facts": "Yes, clicking the Waddles avatar in the header triggers a realistic pig snort audio clip loaded client-side.",
        "subjects": ["truffle pig snort audio", "avatar click trigger"],
        "followups": ["Where is the mp3 file?", "Can I mute the sound?"]
    },
    {
        "id": 97,
        "category": "General",
        "query": "How do I run Waddles offline?",
        "facts": "Once the model weights are cached in your browser's Cache Storage, the page works fully offline without server calls.",
        "subjects": ["browser Cache Storage", "works fully offline"],
        "followups": ["How big is the cache?", "How do I clear the weights?"]
    },
    {
        "id": 98,
        "category": "General",
        "query": "What is Reciprocal Rank Fusion (RRF)?",
        "facts": "Reciprocal Rank Fusion (RRF) combines sparse keyword search and dense vector search ranks to produce a unified relevance ranking.",
        "subjects": ["hybrid rank combination", "unified relevance ranking"],
        "followups": ["What is the RRF constant?", "Does Waddles use BM25?"]
    },
    {
        "id": 99,
        "category": "General",
        "query": "How is ROUGE-L calculated in the script?",
        "facts": "ROUGE-L computes the longest common subsequence of words between the generated candidate and reference strings.",
        "subjects": ["longest common subsequence", "word-level overlap ratio"],
        "followups": ["Does it stem words?", "What is the penalty for length?"]
    },
    {
        "id": 100,
        "category": "General",
        "query": "What is WebAssembly text generation latency?",
        "facts": "Generation latency ranges from 50ms to 500ms per query depending on prompt context size, model size, and CPU threads.",
        "subjects": ["50ms to 500ms latency", "dependent on threads and parameters"],
        "followups": ["Is WebGPU faster?", "Can we use server fallback?"]
    }
]

# Generate the 100 entries for each of the 4 personas (total 400 test cases) with diverse templates
out_dataset = []

for item in BASE_DATA:
    q = item["query"]
    cat = item["category"]
    facts = item["facts"]
    subjs = item["subjects"]
    fups = item["followups"]
    item_id = item["id"]
    subj = subjs[0]
    
    # 1. HELPFUL
    helpful_templates = [
        f"According to the documentation: {facts}",
        f"Based on the official records, {facts}",
        f"Here is the information from the course guidelines: {facts}",
        f"{facts} Hopefully, that helps clarify your question.",
        f"The official website states that {facts}"
    ]
    helpful_ans = helpful_templates[item_id % len(helpful_templates)]
    
    helpful_fup_templates = [
        lambda f: f"Would you like to know: '{f}'?",
        lambda f: f"Perhaps you would also be interested in: '{f}'?",
        lambda f: f"For more details, should we discuss: '{f}'?"
    ]
    helpful_fups = [helpful_fup_templates[(item_id + idx) % len(helpful_fup_templates)](f) for idx, f in enumerate(fups)]
    
    out_dataset.append({
        "tone": "helpful",
        "category": cat,
        "query": q,
        "answer": helpful_ans,
        "followups": helpful_fups
    })
    
    # 2. SASSY
    sassy_templates = [
        f"Oh, fantastic, let's talk about {subj}. If you actually read the site, you'd know that {facts} But sure, ask me anyway.",
        f"Seriously? Another question about {subj}? Fine: {facts} I hope you appreciate the effort.",
        f"Well, if you had taken five seconds to look, you'd see that {facts} But I guess typing that query was easier.",
        f"Ah, {subj}. Fascinating. Here is your answer: {facts} Let know if you need anything else spelled out.",
        f"Look, my tolerance is pretty low today, but here's what you want: {facts} Happy now?"
    ]
    sassy_ans = sassy_templates[item_id % len(sassy_templates)]
    
    sassy_fup_templates = [
        lambda f: f"Should I explain '{f}' or can you search it?",
        lambda f: f"Do you also want me to hand-feed you info on '{f}'?",
        lambda f: f"I suppose you'll ask next: '{f}'?"
    ]
    sassy_fups = [sassy_fup_templates[(item_id + idx) % len(sassy_fup_templates)](f) for idx, f in enumerate(fups)]
    
    out_dataset.append({
        "tone": "sassy",
        "category": cat,
        "query": q,
        "answer": sassy_ans,
        "followups": sassy_fups
    })
    
    # 3. PIRATE
    facts_pirate = facts.replace('Yes, ', '').replace('TJ ', "Cap'n TJ ")
    pirate_templates = [
        f"Ahoy, matey! Set your sails to the tale of {subj}! The charts show that {facts_pirate} Harrr!",
        f"Shiver me timbers! Ye seek knowledge of {subj}? The ship's log reveals that {facts_pirate} Aye, 'tis true!",
        f"Avast ye! The wind blows in favor of {subj}! Keep yer eyes on the horizon, for {facts_pirate} Harrr!",
        f"By Blackbeard's ghost, the secret of {subj} is out! The tavern rumors say that {facts_pirate} Drink up, me hearties!",
        f"Ahoy! Let's weigh anchor and discuss {subj}! The sea captains tell tales that {facts_pirate} Harrr!"
    ]
    pirate_ans = pirate_templates[item_id % len(pirate_templates)]
    
    pirate_fup_templates = [
        lambda f: f"Seek ye the treasure of: '{f}'?",
        lambda f: f"Would ye set course for: '{f}'?",
        lambda f: f"What say ye to: '{f}'?"
    ]
    pirate_fups = [pirate_fup_templates[(item_id + idx) % len(pirate_fup_templates)](f) for idx, f in enumerate(fups)]
    
    out_dataset.append({
        "tone": "pirate",
        "category": cat,
        "query": q,
        "answer": pirate_ans,
        "followups": pirate_fups
    })
    
    # 4. CYNICAL REDDITOR (New Persona)
    redditor_templates = [
        f"AFAIK everyone is talking about {subj}. IMO, it's just gatekeeping to ask this, but basically {facts} /s. Typical r/omscs behavior.",
        f"Hot take, but asking about {subj} is peak r/omscs. Honestly, {facts} TL;DR: just read the syllabus next time.",
        f"Sigh. Yet another post about {subj}. Look, it's not that hard: {facts} Downvote me if you want, but it's the truth.",
        f"This sub is so repetitive. A simple search would show that {facts} /s. But whatever, hope that helps your GPA.",
        f"IMO, {subj} is completely overrated, but since you asked: {facts} TIA for not checking the wiki first."
    ]
    redditor_ans = redditor_templates[item_id % len(redditor_templates)]
    
    redditor_fup_templates = [
        lambda f: f"Is anyone else annoyed by '{f}'? TIA.",
        lambda f: f"Cue the incoming posts asking about '{f}'.",
        lambda f: f"Can't wait for the mods to pin a thread on '{f}'."
    ]
    redditor_fups = [redditor_fup_templates[(item_id + idx) % len(redditor_fup_templates)](f) for idx, f in enumerate(fups)]
    
    out_dataset.append({
        "tone": "cynical_redditor",
        "category": cat,
        "query": q,
        "answer": redditor_ans,
        "followups": redditor_fups
    })

# Write the final JSON file
os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(out_dataset, f, indent=2, ensure_ascii=False)

print(f"Generated {len(out_dataset)} persona examples (100 for each of helpful, sassy, pirate, and cynical_redditor) in {OUT_FILE}.")
