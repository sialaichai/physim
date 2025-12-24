let animationsData = {};

// 1. Load Data
fetch('simulations.json')
    .then(response => response.json())
    .then(data => {
        animationsData = data;
        initSidebar(); 
    });

// 2. Initialize Sidebar (Dropdown & Listeners)
function initSidebar() {
    const topicSelect = document.getElementById('topicSelect');
    
    // A. Populate Dropdown with Topics
    Object.keys(animationsData).forEach(topic => {
        const option = document.createElement("option");
        option.value = topic;
        option.textContent = topic;
        topicSelect.appendChild(option);
    });

    // B. Listener for Topic Change
    topicSelect.addEventListener('change', (e) => {
        renderSimulationList(e.target.value);
    });

    // C. Listener for Search Filter
    document.getElementById('searchInput').addEventListener('input', (e) => {
        renderSimulationList(topicSelect.value, e.target.value);
    });

    // D. Initial Render (First topic, first sim)
    const firstTopic = Object.keys(animationsData)[0];
    renderSimulationList(firstTopic);
    
    // Auto-load the very first simulation
    const firstSim = Object.keys(animationsData[firstTopic])[0];
    loadSimulation(firstTopic, firstSim);
}

// 3. Render List of Simulations (Based on Topic)
function renderSimulationList(topic, filterText = "") {
    const navMenu = document.getElementById('navMenu');
    navMenu.innerHTML = ""; // Clear list

    const sims = animationsData[topic];
    if (!sims) return;

    Object.keys(sims).forEach(simName => {
        // Filter logic (case insensitive)
        if (simName.toLowerCase().includes(filterText.toLowerCase())) {
            const item = document.createElement("div");
            item.className = "nav-item";
            item.textContent = simName;
            
            // Click Event
            item.onclick = () => {
                // Highlight active item
                document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
                item.classList.add('active');
                
                // Load Content
                loadSimulation(topic, simName);
                
                // Optional: On mobile, auto-close sidebar after selection
                if (window.innerWidth < 768) toggleSidebar();
            };
            navMenu.appendChild(item);
        }
    });
}

// 4. Content Loading Logic (Same as before)
function loadSimulation(topic, simName) {
    const data = animationsData[topic][simName];

    document.getElementById('categoryTag').textContent = `Category: ${topic}`;
    document.getElementById('simTitle').textContent = simName;
    document.getElementById('simDescription').innerHTML = data.description;

    // Image Handling
    const imgContainer = document.getElementById('imageContainer');
    imgContainer.innerHTML = "";
    if (data.image) {
        const img = document.createElement("img");
        img.src = data.image;
        img.className = "diagram";
        imgContainer.appendChild(img);
    }

    document.getElementById('simFrame').src = data.url;

    // Questions Handling
    const qContainer = document.getElementById('questionsContainer');
    const qList = document.getElementById('questionsList');
    qList.innerHTML = "";
    
    if (data.questions && data.questions.length > 0 && data.questions[0] !== "") {
        qContainer.style.display = "block";
        data.questions.forEach((q, index) => {
            const p = document.createElement("p");
            p.innerHTML = `<strong>${index + 1}.</strong> ${q}`;
            qList.appendChild(p);
        });
    } else {
        qContainer.style.display = "none";
    }
}

// 5. Toggle Sidebar Logic
const toggleBtn = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');

toggleBtn.addEventListener('click', toggleSidebar);

function toggleSidebar() {
    sidebar.classList.toggle('closed');
    mainContent.classList.toggle('expanded');
}
